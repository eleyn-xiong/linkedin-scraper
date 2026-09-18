"""FV Mentorship Batch 1 — Full mode (VC partner profiles + send).

Sends from aadith@freeventures.org via the fv_mentorship Gmail account.
Run auth once before first use:
  venv/Scripts/python gmail_client.py auth fv_mentorship

1 contact per VC firm (max_contacts_per_company=1, exclude_contacted=True).
Template: fv_mentorship — only the 1-line hook is LLM-generated.
"""

import sys, time, random, sqlite3
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
config.SENDER_EMAIL   = "aadith@freeventures.org"
config.SENDER_NAME    = "Aadith"
config.SENDER_TITLE   = "Program Lead"
config.SENDER_COMPANY = "Free Ventures"

from db import get_db, new_id, init_db
from linkedin_ingest import ingest_profiles
from personalize_once import personalize_once_per_company
from gmail_client import GmailClient

CAMPAIGN_NAME = "FV Mentorship Batch 1 - Fall 2026"
GMAIL_ACCOUNT = "fv_mentorship"
SENDER_EMAIL  = "aadith@freeventures.org"
SENDER_NAME   = "Aadith"

SENDER_VALUE_PROP = (
    "Free Ventures is UC Berkeley's leading pre-seed startup accelerator and the university's "
    "only nonprofit, student-run program of its kind. We help the most promising Berkeley founders "
    "raise their first checks and build scalable companies — and we're recruiting mentors from the "
    "VC and founder community for our upcoming Fall 2026 batch (Oct 6 – Nov 10)."
)

VC_FIRMS = [
    {"name": "8VC",                   "domain": "8vc.com",                "industry": "Venture Capital / Deep Tech / Defense / Healthcare", "email_pattern": "first.last"},
    {"name": "Pear VC",               "domain": "pear.vc",                "industry": "Venture Capital / Early Stage / Consumer / Enterprise", "email_pattern": "first.last"},
    {"name": "Andreessen Horowitz",   "domain": "a16z.com",               "industry": "Venture Capital / Technology / Crypto / Bio", "email_pattern": "first.last"},
    {"name": "Sequoia Capital",       "domain": "sequoiacap.com",         "industry": "Venture Capital / Global / Growth / Seed", "email_pattern": "first.last"},
    {"name": "Kleiner Perkins",       "domain": "kleinerperkins.com",     "industry": "Venture Capital / Enterprise / Consumer / Healthcare", "email_pattern": "first.last"},
    {"name": "Greylock",              "domain": "greylock.com",           "industry": "Venture Capital / Enterprise / Consumer / AI", "email_pattern": "first.last"},
    {"name": "Lightspeed Venture Partners", "domain": "lsvp.com",        "industry": "Venture Capital / Enterprise / Consumer / Fintech", "email_pattern": "first.last"},
    {"name": "NEA",                   "domain": "nea.com",                "industry": "Venture Capital / Healthcare / Technology / Growth", "email_pattern": "first.last"},
    {"name": "Accel",                 "domain": "accel.com",              "industry": "Venture Capital / SaaS / Infrastructure / Security", "email_pattern": "first.last"},
    {"name": "Foundation Capital",    "domain": "foundationcap.com",      "industry": "Venture Capital / AI / Enterprise / Fintech", "email_pattern": "first.last"},
    {"name": "General Catalyst",      "domain": "generalcatalyst.com",    "industry": "Venture Capital / AI / Health / Climate", "email_pattern": "first.last"},
    {"name": "Initialized Capital",   "domain": "initialized.com",        "industry": "Venture Capital / Seed / Consumer / B2B", "email_pattern": "first.last"},
    {"name": "Redpoint Ventures",     "domain": "redpoint.com",           "industry": "Venture Capital / Infrastructure / SaaS / Data", "email_pattern": "first.last"},
    {"name": "Precursor Ventures",    "domain": "precursorvc.com",        "industry": "Venture Capital / Pre-Seed / Underrepresented Founders", "email_pattern": "first.last"},
    {"name": "Founders Fund",         "domain": "foundersfund.com",       "industry": "Venture Capital / Deep Tech / AI / Defense", "email_pattern": "first.last"},
]

# 3 profiles per firm — ingest_profiles keeps up to 3; personalize_once picks
# the first one not already contacted (exclude_contacted=True, max_contacts_per_company=1).
VC_PROFILES = {
    "8VC": [
        {"title": "Joe Lonsdale - Co-Founder and Managing Partner - 8VC | LinkedIn",            "url": "https://www.linkedin.com/in/jlonsdale/"},
        {"title": "Jake Medwell - General Partner - 8VC | LinkedIn",                            "url": "https://www.linkedin.com/in/jakemedwell/"},
        {"title": "Ali Reza Akhlaghi - Partner - 8VC | LinkedIn",                               "url": "https://www.linkedin.com/in/alirezaakhlaghi/"},
    ],
    "Pear VC": [
        {"title": "Pejman Nozad - Co-Founding Managing Partner - Pear VC | LinkedIn",           "url": "https://www.linkedin.com/in/pejmannozad/"},
        {"title": "Mar Hershenson - Co-Founding Managing Partner - Pear VC | LinkedIn",         "url": "https://www.linkedin.com/in/marhershenson/"},
        {"title": "Ajay Royan - Partner - Pear VC | LinkedIn",                                  "url": "https://www.linkedin.com/in/ajayroyan/"},
    ],
    "Andreessen Horowitz": [
        {"title": "Martin Casado - General Partner - Andreessen Horowitz | LinkedIn",            "url": "https://www.linkedin.com/in/martincasado/"},
        {"title": "Andrew Chen - General Partner - Andreessen Horowitz | LinkedIn",              "url": "https://www.linkedin.com/in/andrewchen/"},
        {"title": "Sriram Krishnan - General Partner - Andreessen Horowitz | LinkedIn",          "url": "https://www.linkedin.com/in/sriramk/"},
    ],
    "Sequoia Capital": [
        {"title": "Roelof Botha - Managing Partner - Sequoia Capital | LinkedIn",                "url": "https://www.linkedin.com/in/roelofbotha/"},
        {"title": "Alfred Lin - Partner - Sequoia Capital | LinkedIn",                           "url": "https://www.linkedin.com/in/alfredlin/"},
        {"title": "Jess Lee - Partner - Sequoia Capital | LinkedIn",                             "url": "https://www.linkedin.com/in/jessylee/"},
    ],
    "Kleiner Perkins": [
        {"title": "Ilya Fischman - Partner - Kleiner Perkins | LinkedIn",                        "url": "https://www.linkedin.com/in/ilyafischman/"},
        {"title": "Noah Knauf - Partner - Kleiner Perkins | LinkedIn",                           "url": "https://www.linkedin.com/in/noahknauf/"},
        {"title": "Wen Hsieh - Partner - Kleiner Perkins | LinkedIn",                            "url": "https://www.linkedin.com/in/wenhsieh/"},
    ],
    "Greylock": [
        {"title": "Sarah Guo - Partner - Greylock | LinkedIn",                                   "url": "https://www.linkedin.com/in/sarahguo/"},
        {"title": "Asheem Chandna - Partner - Greylock | LinkedIn",                              "url": "https://www.linkedin.com/in/asheemchandna/"},
        {"title": "Reid Christian - Partner - Greylock | LinkedIn",                              "url": "https://www.linkedin.com/in/reidchristian/"},
    ],
    "Lightspeed Venture Partners": [
        {"title": "Jeremy Liew - Partner - Lightspeed Venture Partners | LinkedIn",              "url": "https://www.linkedin.com/in/jeremyliew/"},
        {"title": "Ravi Mhatre - Founding Managing Partner - Lightspeed Venture Partners | LinkedIn", "url": "https://www.linkedin.com/in/ravimhatre/"},
        {"title": "Alex Taussig - Partner - Lightspeed Venture Partners | LinkedIn",             "url": "https://www.linkedin.com/in/alextaussig/"},
    ],
    "NEA": [
        {"title": "Scott Sandell - Managing General Partner - NEA | LinkedIn",                   "url": "https://www.linkedin.com/in/scottsandell/"},
        {"title": "Ali Behbahani - General Partner - NEA | LinkedIn",                            "url": "https://www.linkedin.com/in/alibehbahani/"},
        {"title": "Tony Florence - General Partner - NEA | LinkedIn",                            "url": "https://www.linkedin.com/in/tonyflorence/"},
    ],
    "Accel": [
        {"title": "Andrew Braccia - Partner - Accel | LinkedIn",                                 "url": "https://www.linkedin.com/in/andrewbraccia/"},
        {"title": "Sameer Gandhi - Partner - Accel | LinkedIn",                                  "url": "https://www.linkedin.com/in/sameergandhi/"},
        {"title": "Ping Li - Partner - Accel | LinkedIn",                                        "url": "https://www.linkedin.com/in/pingli/"},
    ],
    "Foundation Capital": [
        {"title": "Ashu Garg - General Partner - Foundation Capital | LinkedIn",                 "url": "https://www.linkedin.com/in/ashugarg/"},
        {"title": "Steve Vassallo - General Partner - Foundation Capital | LinkedIn",             "url": "https://www.linkedin.com/in/stevevassallo/"},
        {"title": "Charles Moldow - General Partner - Foundation Capital | LinkedIn",             "url": "https://www.linkedin.com/in/charlesmoldow/"},
    ],
    "General Catalyst": [
        {"title": "Hemant Taneja - Managing Director - General Catalyst | LinkedIn",             "url": "https://www.linkedin.com/in/hrtaneja/"},
        {"title": "Deep Nishar - Managing Director - General Catalyst | LinkedIn",               "url": "https://www.linkedin.com/in/deepnishar/"},
        {"title": "Niko Bonatsos - Managing Director - General Catalyst | LinkedIn",             "url": "https://www.linkedin.com/in/nikobonatsos/"},
    ],
    "Initialized Capital": [
        {"title": "Garry Tan - Partner - Initialized Capital | LinkedIn",                        "url": "https://www.linkedin.com/in/garrytan/"},
        {"title": "Alexis Ohanian - Partner - Initialized Capital | LinkedIn",                   "url": "https://www.linkedin.com/in/alexisohanian/"},
        {"title": "Kim-Mai Cutler - Partner - Initialized Capital | LinkedIn",                   "url": "https://www.linkedin.com/in/kimmaicutler/"},
    ],
    "Redpoint Ventures": [
        {"title": "Tomasz Tunguz - Managing Director - Redpoint Ventures | LinkedIn",            "url": "https://www.linkedin.com/in/tomasztunguz/"},
        {"title": "Satish Dharmaraj - Managing Director - Redpoint Ventures | LinkedIn",         "url": "https://www.linkedin.com/in/satishdharmaraj/"},
        {"title": "Annie Kadavy - Partner - Redpoint Ventures | LinkedIn",                       "url": "https://www.linkedin.com/in/anniekadavy/"},
    ],
    "Precursor Ventures": [
        {"title": "Charles Hudson - Managing Partner - Precursor Ventures | LinkedIn",           "url": "https://www.linkedin.com/in/charleshudson/"},
        {"title": "Lita Nelsen - Partner - Precursor Ventures | LinkedIn",                       "url": "https://www.linkedin.com/in/litanelsen/"},
        {"title": "Sophie Bakalar - Partner - Precursor Ventures | LinkedIn",                    "url": "https://www.linkedin.com/in/sophiebakalar/"},
    ],
    "Founders Fund": [
        {"title": "Brian Singerman - Partner - Founders Fund | LinkedIn",                        "url": "https://www.linkedin.com/in/briansingerman/"},
        {"title": "Trae Stephens - Partner - Founders Fund | LinkedIn",                          "url": "https://www.linkedin.com/in/traestephens/"},
        {"title": "Napoleon Ta - Partner - Founders Fund | LinkedIn",                            "url": "https://www.linkedin.com/in/napoleonta/"},
    ],
}


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


def main():
    init_db()

    # ── Step 1: Insert VC firms ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 1: Ensuring VC firms exist in DB")
    print("=" * 60)
    with get_db() as conn:
        for firm in VC_FIRMS:
            try:
                conn.execute(
                    "INSERT INTO companies (id,name,domain,industry,email_pattern,email_pattern_confidence) "
                    "VALUES (?,?,?,?,?,?)",
                    (new_id(), firm["name"], firm["domain"], firm["industry"],
                     firm["email_pattern"], 60.0),
                )
                print(f"  [+] {firm['name']}")
            except Exception as e:
                if "UNIQUE" in str(e).upper():
                    print(f"  [=] {firm['name']} already exists")
                else:
                    print(f"  [!] {firm['name']}: {e}")

    # ── Step 2: Ingest profiles ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 2: Ingesting VC partner profiles")
    print("=" * 60)
    company_domains = []
    for firm in VC_FIRMS:
        profiles = VC_PROFILES.get(firm["name"], [])
        if not profiles:
            print(f"  [SKIP] {firm['name']} — no profiles defined")
            continue
        ingest_profiles(firm["name"], profiles, min_required=1, max_keep=3)
        company_domains.append(firm["domain"])

    # ── Step 3: Create campaign ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 3: Creating campaign")
    print("=" * 60)
    with get_db() as conn:
        existing = conn.execute(
            "SELECT id FROM campaigns WHERE name=?", (CAMPAIGN_NAME,)
        ).fetchone()
        if existing:
            campaign_id = existing["id"]
            print(f"  [=] Exists: {campaign_id}")
        else:
            campaign_id = new_id()
            safe_exec(
                conn,
                "INSERT INTO campaigns (id,name,status) VALUES (?,?,'active')",
                (campaign_id, CAMPAIGN_NAME),
            )
            print(f"  [+] Created: {CAMPAIGN_NAME} ({campaign_id})")

    # ── Step 4: Personalize ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 4: Personalizing — fv_mentorship template, 1 per firm")
    print("=" * 60)
    personalize_once_per_company(
        campaign_id=campaign_id,
        sender_value_prop=SENDER_VALUE_PROP,
        num_steps=1,
        template="fv_mentorship",
        max_contacts_per_company=1,
        exclude_contacted=True,
        company_domains=company_domains,
    )

    # ── Step 5: Send ────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 5: Sending from aadith@freeventures.org")
    print("=" * 60)

    conn_s = sqlite3.connect("outreach.db", timeout=60)
    conn_s.row_factory = sqlite3.Row
    conn_s.execute("PRAGMA foreign_keys=ON")
    conn_s.execute("PRAGMA busy_timeout=60000")

    rows = conn_s.execute(
        """SELECT sr.id as sr_id, ct.primary_email, ct.first_name, ct.last_name,
                  co.name as company_name, pm.subject, pm.body
           FROM send_records sr
           JOIN contacts              ct ON sr.contact_id = ct.id
           JOIN companies             co ON ct.company_id = co.id
           JOIN personalized_messages pm ON sr.message_id = pm.id
           WHERE sr.campaign_id=? AND sr.status='queued'
           ORDER BY co.name, ct.last_name""",
        (campaign_id,),
    ).fetchall()

    print(f"  {len(rows)} emails queued — sending from {SENDER_EMAIL}...")

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

    total_sent = 0
    total_failed = 0

    for row in rows:
        retries = 0
        while retries < 3:
            try:
                result = gmail.send_email(
                    to=row["primary_email"],
                    subject=row["subject"],
                    body=row["body"],
                    sender_name=SENDER_NAME,
                    sender_email=SENDER_EMAIL,
                )

                def _upd(sql, params=()):
                    for _ in range(5):
                        try:
                            conn_s.execute(sql, params)
                            conn_s.commit()
                            return
                        except sqlite3.OperationalError as e:
                            if "locked" in str(e).lower():
                                time.sleep(2)
                            else:
                                raise

                _upd(
                    "UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=? WHERE id=?",
                    (result["id"], result["threadId"], datetime.now(timezone.utc).isoformat(), row["sr_id"]),
                )
                total_sent += 1
                print(f"  [{total_sent}] {row['company_name']} — {row['first_name']} {row['last_name']} <{row['primary_email']}>")
                break

            except ConnectionResetError:
                retries += 1
                print(f"  [retry {retries}/3] Connection reset — waiting 30s...")
                time.sleep(30)
                try:
                    gmail = GmailClient(account=GMAIL_ACCOUNT)
                except Exception:
                    pass

            except Exception as e:
                total_failed += 1
                print(f"  [!] FAILED {row['primary_email']}: {e}")
                conn_s.execute(
                    "UPDATE send_records SET status='failed',error=? WHERE id=?",
                    (str(e)[:500], row["sr_id"]),
                )
                conn_s.commit()
                break

        else:
            total_failed += 1
            conn_s.execute(
                "UPDATE send_records SET status='failed',error='ConnectionResetError after 3 retries' WHERE id=?",
                (row["sr_id"],),
            )
            conn_s.commit()

        time.sleep(random.uniform(15, 25))

    conn_s.close()
    print(f"\n{'=' * 60}")
    print(f"DONE — {total_sent} sent, {total_failed} failed")
    print(f"Campaign: {CAMPAIGN_NAME}")
    print("=" * 60)


if __name__ == "__main__":
    main()
