"""Send step-2 follow-up emails to contacts who have not replied.

Eligibility criteria (per contact × campaign):
  • step_number = 1 AND status = 'sent'
  • sent_at is at least DAYS_WAIT days ago
  • reply_detected_at IS NULL  (no reply detected)
  • bounced_at IS NULL AND status != 'bounced'
  • No existing step-2 send_record for this contact in this campaign

Sender account:
  • Campaign name contains "mentorship" → aadith@freeventures.org  (fv_mentorship account)
  • All other campaigns              → eleynxiong@berkeley.edu     (default account)
"""

import sys, json, random, time, sqlite3, argparse
from datetime import datetime, timedelta, timezone

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import config
from db import get_db, new_id, init_db
from gmail_client import GmailClient
from claude_client import ClaudeClient

DAYS_WAIT = 21
MIN_DELAY = 15
MAX_DELAY = 25


def safe_exec(conn, sql, params=()):
    for attempt in range(5):
        try:
            conn.execute(sql, params)
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < 4:
                time.sleep(2 ** attempt)
            else:
                raise


def _account_for_campaign(campaign_name: str):
    """Return (account_key, sender_email, sender_name, sender_org)."""
    if "mentorship" in campaign_name.lower():
        return "fv_mentorship", "aadith@freeventures.org", "Aadith", "Free Ventures"
    if "fv" in campaign_name.lower() or "free ventures" in campaign_name.lower():
        return "default", "eleynxiong@berkeley.edu", "Eleyn Xiong", "Free Ventures"
    if "vo" in campaign_name.lower() or "venture out" in campaign_name.lower():
        return "default", "eleynxiong@berkeley.edu", "Eleyn Xiong", "Venture Out"
    return "default", "eleynxiong@berkeley.edu", "Eleyn Xiong", "Berkeley Business Society"


def _build_followup_body(
    first_name: str,
    company_name: str,
    original_subject: str,
    sender_name: str,
    sender_org: str,
    is_mentorship: bool,
    claude: ClaudeClient,
) -> str:
    if is_mentorship:
        tone = (
            "Warm, brief (3-4 sentences before sign-off). Circling-back energy — not pushy. "
            "Mention the Free Ventures mentorship batch (Oct 6 – Nov 10) and acknowledge timing might be tight. "
            "Low-pressure close ('totally understand if it's not a fit right now'). "
            f"Sign off exactly as:\n{sender_name}\nhttps://www.freeventures.org/"
        )
    else:
        tone = (
            "Warm, brief (3-4 sentences before sign-off). "
            "Open with 'Hope you're doing well' (not 'I hope this finds you well'). "
            "Mention circling back on your earlier note. "
            "One-sentence reminder of the value prop / what you lead. "
            "Low-pressure close — offer to share past work samples if helpful. "
            f"Sign off exactly as:\n{sender_name} | 858-371-9042\n{sender_org}\nUC Berkeley"
        )

    prompt = (
        f"Write a brief follow-up cold email.\n\n"
        f"Recipient: {first_name} at {company_name}\n"
        f"Sender: {sender_name} from {sender_org}\n"
        f"Original subject: {original_subject}\n"
        f"Days since first email: ~{DAYS_WAIT}\n\n"
        f"Tone / structure:\n{tone}\n\n"
        f"RULES:\n"
        f"- 3-4 sentences in the body (before sign-off)\n"
        f"- Do NOT repitch in detail — just 'circling back'\n"
        f"- Return ONLY valid JSON: {{\"body\": \"...\"}}\n"
        f"- Do NOT include the subject — just the email body text\n"
    )

    try:
        raw = claude._complete(prompt, max_tokens=400)
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        last = text.rfind("}")
        if last != -1:
            text = text[: last + 1]
        data = json.loads(text)
        return data.get("body", "")
    except Exception as e:
        print(f"  [LLM] follow-up generation failed: {e}. Using fallback.")

    # Fallback if LLM fails
    if is_mentorship:
        return (
            f"Hi {first_name},\n\n"
            "Hope you're doing well — just circling back on my note about the Free Ventures mentorship batch "
            "(Oct 6 – Nov 10). Wanted to make sure it didn't get buried.\n\n"
            "Totally understand if timing is off, but if there's any interest in connecting with Berkeley's "
            "top early-stage founders, I'd love to find a time.\n\n"
            f"Best,\n{sender_name}\nhttps://www.freeventures.org/"
        )
    return (
        f"Hi {first_name},\n\n"
        f"Hope you're doing well. Just circling back on my earlier note about {sender_org} — "
        "wanted to make sure it didn't get buried.\n\n"
        "Still think there could be a strong fit. Happy to share past work samples if helpful.\n\n"
        f"Best,\n{sender_name} | 858-371-9042\n{sender_org}\nUC Berkeley"
    )


def run_followups(dry_run: bool = False, campaign_filter: str = None):
    init_db()
    claude = ClaudeClient()

    cutoff = (datetime.now(timezone.utc) - timedelta(days=DAYS_WAIT)).isoformat()

    with get_db() as conn:
        query = """
            SELECT
                sr.id               AS sr_id,
                sr.contact_id,
                sr.campaign_id,
                sr.gmail_thread_id,
                sr.gmail_message_id,
                sr.sent_at,
                pm.subject          AS original_subject,
                ct.first_name,
                ct.last_name,
                ct.primary_email,
                co.name             AS company_name,
                c.name              AS campaign_name
            FROM send_records sr
            JOIN personalized_messages pm ON sr.message_id = pm.id
            JOIN contacts              ct ON sr.contact_id  = ct.id
            JOIN companies             co ON ct.company_id  = co.id
            JOIN campaigns             c  ON sr.campaign_id = c.id
            WHERE sr.step_number = 1
              AND sr.status = 'sent'
              AND sr.sent_at <= ?
              AND sr.reply_detected_at IS NULL
              AND sr.bounced_at IS NULL
              AND sr.status != 'bounced'
              AND NOT EXISTS (
                  SELECT 1 FROM send_records sr2
                  WHERE sr2.contact_id  = sr.contact_id
                    AND sr2.campaign_id = sr.campaign_id
                    AND sr2.step_number = 2
              )
        """
        params = [cutoff]
        if campaign_filter:
            query += " AND c.name LIKE ?"
            params.append(f"%{campaign_filter}%")
        query += " ORDER BY c.name, co.name, sr.sent_at"

        eligible = conn.execute(query, params).fetchall()

    print(f"Contacts eligible for follow-up: {len(eligible)}")
    if campaign_filter:
        print(f"  Campaign filter: '{campaign_filter}'")
    print()

    if not eligible:
        print("Nothing to do.")
        return

    if dry_run:
        print("DRY RUN — no emails will be sent:\n")
        for row in eligible:
            _, sender_email, _, _ = _account_for_campaign(row["campaign_name"])
            print(
                f"  [{row['campaign_name']}] "
                f"{row['first_name']} {row['last_name']} <{row['primary_email']}> "
                f"@ {row['company_name']}"
            )
            print(f"    Sent {str(row['sent_at'])[:10]} → follow-up from {sender_email}")
        return

    sent_count = 0
    error_count = 0
    current_account = None
    gmail = None

    for i, row in enumerate(eligible):
        account, sender_email, sender_name, sender_org = _account_for_campaign(row["campaign_name"])
        is_mentorship = "mentorship" in row["campaign_name"].lower()

        # Rebuild GmailClient only on account switch
        if account != current_account:
            print(f"\n── Switching to account: {sender_email} ──")
            for attempt in range(3):
                try:
                    gmail = GmailClient(account=account)
                    current_account = account
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f"  GmailClient init failed (attempt {attempt + 1}): {e}. Retrying in 30s...")
                        time.sleep(30)
                    else:
                        raise

        print(
            f"\n[{i + 1}/{len(eligible)}] {row['first_name']} {row['last_name']}"
            f" @ {row['company_name']}"
        )
        print(f"  Campaign: {row['campaign_name']} | Step-1 sent: {str(row['sent_at'])[:10]}")

        followup_body = _build_followup_body(
            first_name=row["first_name"],
            company_name=row["company_name"],
            original_subject=row["original_subject"],
            sender_name=sender_name,
            sender_org=sender_org,
            is_mentorship=is_mentorship,
            claude=claude,
        )

        followup_subject = f"Re: {row['original_subject']}"
        print(f"  Subject: {followup_subject}")

        try:
            for attempt in range(3):
                try:
                    result = gmail.send_email(
                        to=row["primary_email"],
                        subject=followup_subject,
                        body=followup_body,
                        sender_name=sender_name,
                        sender_email=sender_email,
                        thread_id=row["gmail_thread_id"] or None,
                        in_reply_to=row["gmail_message_id"] or None,
                    )
                    break
                except ConnectionResetError:
                    if attempt < 2:
                        print(f"  ConnectionResetError (attempt {attempt + 1}). Retrying in 30s...")
                        time.sleep(30)
                        gmail = GmailClient(account=account)
                    else:
                        raise

            sent_time = datetime.now(timezone.utc).isoformat()

            with get_db() as conn:
                msg_id = new_id()
                safe_exec(
                    conn,
                    "INSERT INTO personalized_messages "
                    "(id, contact_id, campaign_id, step_number, subject, body) "
                    "VALUES (?,?,?,?,?,?)",
                    (msg_id, row["contact_id"], row["campaign_id"], 2, followup_subject, followup_body),
                )
                safe_exec(
                    conn,
                    "INSERT INTO send_records "
                    "(id, campaign_id, contact_id, message_id, step_number, status, "
                    "gmail_message_id, gmail_thread_id, sent_at) "
                    "VALUES (?,?,?,?,2,'sent',?,?,?)",
                    (
                        new_id(),
                        row["campaign_id"],
                        row["contact_id"],
                        msg_id,
                        result["id"],
                        result["threadId"],
                        sent_time,
                    ),
                )

            sent_count += 1
            print(f"  [OK] Sent → thread {result['threadId']}")

        except Exception as e:
            error_count += 1
            print(f"  [ERROR] {e}")

        if i < len(eligible) - 1:
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"  Waiting {delay:.0f}s...")
            time.sleep(delay)

    print(f"\n{'=' * 50}")
    print(f"Follow-up run complete: {sent_count} sent, {error_count} errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send step-2 follow-up emails")
    parser.add_argument("--dry-run", action="store_true", help="Preview eligible contacts without sending")
    parser.add_argument("--campaign", default=None, help="Filter by campaign name substring")
    args = parser.parse_args()

    run_followups(dry_run=args.dry_run, campaign_filter=args.campaign)
