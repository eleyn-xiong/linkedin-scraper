"""FV Mentorship — Fast mode (CSV input, skip LinkedIn scraping).

Reads a CSV file of contacts, inserts them into the DB if not already present,
personalizes using the fv_mentorship template, and sends emails from Aadith.

Usage:
  venv/Scripts/python run_fv_mentorship_send_only.py --csv contacts.csv
  venv/Scripts/python run_fv_mentorship_send_only.py --csv contacts.csv --dry-run

Required CSV columns (header row mandatory):
  Company, Domain, First Name, Last Name, Title, Email

Optional columns:
  LinkedIn URL   — stored in contacts.linkedin_url if present
  Industry       — stored in companies.industry if present

Example CSV row:
  8VC,8vc.com,Jane,Doe,General Partner,jane@8vc.com,https://linkedin.com/in/janedoe,Venture Capital
"""

import sys, csv, random, time, sqlite3, argparse
from schedule_utils import check_send_window
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import config
config.SENDER_EMAIL   = "aadith@freeventures.org"
config.SENDER_NAME    = "Aadith"
config.SENDER_TITLE   = "Program Lead"
config.SENDER_COMPANY = "Free Ventures"

from db import get_db, new_id, init_db
from personalize_once import personalize_once_per_company
from gmail_client import GmailClient

CAMPAIGN_NAME = "FV Mentorship Batch 1 - Fall 2026"
GMAIL_ACCOUNT = "fv_mentorship"
SENDER_EMAIL  = "aadith@freeventures.org"
SENDER_NAME   = "Aadith"

MIN_DELAY = 15
MAX_DELAY = 25

REQUIRED_COLS = {"Company", "Domain", "First Name", "Last Name", "Title", "Email"}


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


def load_csv(csv_path: str) -> list[dict]:
    path = Path(csv_path)
    if not path.exists():
        print(f"ERROR: CSV file not found: {csv_path}")
        sys.exit(1)

    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = set(reader.fieldnames or [])
        missing = REQUIRED_COLS - headers
        if missing:
            print(f"ERROR: CSV is missing required columns: {', '.join(sorted(missing))}")
            print(f"  Found columns: {', '.join(sorted(headers))}")
            sys.exit(1)
        for row in reader:
            rows.append(dict(row))

    print(f"Loaded {len(rows)} rows from {csv_path}")
    return rows


def insert_contacts(rows: list[dict]) -> tuple[list[str], int, int]:
    """Insert companies + contacts from CSV rows.

    Returns (company_domains, new_companies, new_contacts).
    Skips rows with missing email.
    """
    new_companies = 0
    new_contacts  = 0
    company_domains = []

    with get_db() as conn:
        for row in rows:
            email = (row.get("Email") or "").strip().lower()
            if not email:
                print(f"  Skipping {row.get('First Name')} {row.get('Last Name')} — no email")
                continue

            domain   = (row.get("Domain") or "").strip().lower()
            company  = (row.get("Company") or "").strip()
            industry = (row.get("Industry") or "").strip()

            # Upsert company
            existing_co = conn.execute(
                "SELECT id FROM companies WHERE domain=?", (domain,)
            ).fetchone()
            if existing_co:
                company_id = existing_co["id"]
            else:
                company_id = new_id()
                safe_exec(
                    conn,
                    "INSERT INTO companies (id, name, domain, industry) VALUES (?,?,?,?)",
                    (company_id, company, domain, industry or None),
                )
                new_companies += 1

            if domain not in company_domains:
                company_domains.append(domain)

            # Skip contact if email already in DB
            existing_ct = conn.execute(
                "SELECT id FROM contacts WHERE primary_email=?", (email,)
            ).fetchone()
            if existing_ct:
                continue

            first_name   = (row.get("First Name") or "").strip()
            last_name    = (row.get("Last Name") or "").strip()
            title        = (row.get("Title") or "").strip()
            linkedin_url = (row.get("LinkedIn URL") or "").strip()

            safe_exec(
                conn,
                """INSERT INTO contacts
                   (id, company_id, first_name, last_name, title, linkedin_url, primary_email, email_confidence)
                   VALUES (?,?,?,?,?,?,?,1.0)""",
                (new_id(), company_id, first_name, last_name, title, linkedin_url or None, email),
            )
            new_contacts += 1

    print(f"  Inserted: {new_companies} new companies, {new_contacts} new contacts")
    return company_domains, new_companies, new_contacts


def main():
    parser = argparse.ArgumentParser(description="FV Mentorship fast mode — CSV → personalize → send")
    parser.add_argument("--csv", required=True, help="Path to the contacts CSV file")
    parser.add_argument("--dry-run", action="store_true", help="Insert contacts and personalize, but do not send")
    args = parser.parse_args()

    init_db()

    # ── Step 1: Load CSV ─────────────────────────────────────────────────
    print("=" * 60)
    print("Step 1: Loading contacts from CSV")
    print("=" * 60)
    rows = load_csv(args.csv)

    # ── Step 2: Insert into DB ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 2: Inserting into database")
    print("=" * 60)
    company_domains, _, _ = insert_contacts(rows)

    if not company_domains:
        print("No valid contacts found. Exiting.")
        sys.exit(0)

    # ── Step 3: Create / reuse campaign ─────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 3: Campaign setup")
    print("=" * 60)
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM campaigns WHERE name=?", (CAMPAIGN_NAME,)
        ).fetchone()
        if existing:
            campaign_id = existing["id"]
            print(f"  Reusing campaign: {CAMPAIGN_NAME} ({campaign_id})")
        else:
            campaign_id = new_id()
            safe_exec(
                conn,
                "INSERT INTO campaigns (id, name, status) VALUES (?,?,'active')",
                (campaign_id, CAMPAIGN_NAME),
            )
            print(f"  Created campaign: {CAMPAIGN_NAME} ({campaign_id})")

    # ── Step 4: Personalize ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Step 4: Personalizing (1 call per person, fv_mentorship template)")
    print("=" * 60)
    personalize_once_per_company(
        campaign_id=campaign_id,
        sender_value_prop=(
            "Free Ventures is Berkeley's leading pre-seed startup accelerator. "
            "We connect Berkeley's top early-stage founders with mentors from the VC and founder community."
        ),
        num_steps=1,
        template="fv_mentorship",
        max_contacts_per_company=1,
        exclude_contacted=True,
        company_domains=company_domains,
    )

    # ── Step 5: Send (or dry-run preview) ───────────────────────────────
    print("\n" + "=" * 60)
    print("Step 5: Sending emails" + (" [DRY RUN — no sends]" if args.dry_run else ""))
    print("=" * 60)

    with get_db() as conn:
        queued = conn.execute(
            """SELECT sr.id, sr.contact_id, sr.message_id,
                      ct.first_name, ct.last_name, ct.primary_email,
                      co.name AS company_name,
                      pm.subject, pm.body
               FROM send_records sr
               JOIN contacts              ct ON sr.contact_id = ct.id
               JOIN companies             co ON ct.company_id = co.id
               JOIN personalized_messages pm ON sr.message_id = pm.id
               WHERE sr.campaign_id=? AND sr.status='queued'
               ORDER BY co.name""",
            (campaign_id,),
        ).fetchall()

    print(f"  {len(queued)} emails queued\n")

    if args.dry_run:
        for row in queued:
            print(f"  WOULD SEND → {row['first_name']} {row['last_name']} <{row['primary_email']}> @ {row['company_name']}")
            print(f"    Subject: {row['subject']}")
        print("\nDry run complete. No emails sent.")
        return

    if not check_send_window(campaign_id=campaign_id):
        return

    gmail = None
    for attempt in range(3):
        try:
            gmail = GmailClient(account=GMAIL_ACCOUNT)
            break
        except Exception as e:
            if attempt < 2:
                print(f"  GmailClient init failed (attempt {attempt + 1}): {e}. Retrying in 30s...")
                time.sleep(30)
            else:
                raise

    sent_count = 0
    for i, row in enumerate(queued):
        print(f"  [{i + 1}/{len(queued)}] {row['first_name']} {row['last_name']} @ {row['company_name']}")

        for attempt in range(3):
            try:
                result = gmail.send_email(
                    to=row["primary_email"],
                    subject=row["subject"],
                    body=row["body"],
                    sender_name=SENDER_NAME,
                    sender_email=SENDER_EMAIL,
                )
                break
            except ConnectionResetError:
                if attempt < 2:
                    print(f"    ConnectionResetError (attempt {attempt + 1}). Retrying in 30s...")
                    time.sleep(30)
                    gmail = GmailClient(account=GMAIL_ACCOUNT)
                else:
                    raise

        sent_time = datetime.now(timezone.utc).isoformat()
        with get_db() as conn:
            safe_exec(
                conn,
                """UPDATE send_records
                   SET status='sent', sent_at=?, gmail_message_id=?, gmail_thread_id=?
                   WHERE id=?""",
                (sent_time, result["id"], result["threadId"], row["id"]),
            )

        sent_count += 1
        print(f"    [OK] Sent → {row['primary_email']}")

        if i < len(queued) - 1:
            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"    Waiting {delay:.0f}s...")
            time.sleep(delay)

    print(f"\nDone — {sent_count} emails sent from {SENDER_EMAIL}")


if __name__ == "__main__":
    main()
