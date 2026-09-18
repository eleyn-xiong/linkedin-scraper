"""FV Batch 5 — 5 new large enterprise companies, 10 emails each, eleynxiong@berkeley.edu."""
import sys, time, random, sqlite3
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
config.SENDER_EMAIL = "eleynxiong@berkeley.edu"
config.SENDER_NAME  = "Eleyn Xiong"

from db import get_db, new_id, init_db
from linkedin_ingest import ingest_profiles
from personalize_once import personalize_once_per_company
from gmail_client import GmailClient
from datetime import datetime

init_db()

COMPANIES = [
    {"name": "PayPal",                 "domain": "paypal.com",               "industry": "Fintech / Payments / Digital Wallet / Commerce",  "email_pattern": "first.last"},
    {"name": "Block",                  "domain": "block.xyz",                "industry": "Fintech / Crypto / Payments / Developer Tools",   "email_pattern": "first.last"},
    {"name": "Robinhood",              "domain": "robinhood.com",            "industry": "Fintech / Retail Investing / Crypto / Brokerage", "email_pattern": "first.last"},
    {"name": "Discover Financial",     "domain": "discover.com",             "industry": "Banking / Credit Cards / Personal Finance",        "email_pattern": "first.last"},
    {"name": "Synchrony Financial",    "domain": "synchronyfinancial.com",   "industry": "Consumer Finance / Credit / Retail Banking",       "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Batch 5 - July 2026"
SENDER_VALUE_PROP = (
    "Free Ventures at UC Berkeley is the university's leading pre-seed startup accelerator "
    "and only nonprofit, student-run program of its kind. Over the past decade we've helped "
    "100+ portfolio companies raise $200M+ in follow-on capital from Kleiner Perkins, Accel, "
    "and Greylock, with multiple YC exits and acquisitions by Coinbase, Discord, and Opendoor. "
    "We partner with companies to source deal flow, co-host founder events, and connect their "
    "teams with Berkeley's most ambitious student entrepreneurs building in AI, fintech, "
    "biotech, and consumer."
)

print("\n" + "="*60); print("STEP 1: Ensuring companies exist"); print("="*60)
with get_db() as conn:
    for c in COMPANIES:
        try:
            conn.execute("INSERT INTO companies (id,name,domain,industry,email_pattern,email_pattern_confidence) VALUES (?,?,?,?,?,?)",
                (new_id(), c["name"], c["domain"], c["industry"], c["email_pattern"], 70.0))
            print(f"  [+] {c['name']}")
        except Exception as e:
            print(f"  [=] {c['name']} already exists" if "UNIQUE" in str(e).upper() else f"  [!] {e}")

print("\n" + "="*60); print("STEP 2: Ingesting profiles"); print("="*60)

print("PayPal:", ingest_profiles("PayPal", [
    {"title": "Alex Chriss - President and CEO - PayPal | LinkedIn",                             "url": "https://www.linkedin.com/in/alexchriss/"},
    {"title": "Jamie Miller - EVP and CFO - PayPal | LinkedIn",                                  "url": "https://www.linkedin.com/in/jamiemiller-paypal/"},
    {"title": "Sri Shivananda - EVP and CTO - PayPal | LinkedIn",                                "url": "https://www.linkedin.com/in/srishivananda/"},
    {"title": "Mark Sturgell - EVP Chief Revenue Officer - PayPal | LinkedIn",                   "url": "https://www.linkedin.com/in/marksturgell/"},
    {"title": "Suzan Kereere - President Global Markets - PayPal | LinkedIn",                    "url": "https://www.linkedin.com/in/suzankereere/"},
    {"title": "Michelle Gill - EVP Small Business and Financial Services - PayPal | LinkedIn",   "url": "https://www.linkedin.com/in/michellegill-paypal/"},
    {"title": "Peggy Alford - EVP Consumer Group - PayPal | LinkedIn",                           "url": "https://www.linkedin.com/in/peggyalford/"},
    {"title": "Brian Wendling - Chief HR Officer - PayPal | LinkedIn",                           "url": "https://www.linkedin.com/in/brianwendling-paypal/"},
    {"title": "Brian Umland - EVP Chief Legal Officer - PayPal | LinkedIn",                      "url": "https://www.linkedin.com/in/brianumland/"},
    {"title": "Diego Scotti - EVP Chief Marketing Officer - PayPal | LinkedIn",                  "url": "https://www.linkedin.com/in/diegoscotti/"},
], min_required=3, max_keep=10))

print("Block:", ingest_profiles("Block", [
    {"title": "Jack Dorsey - Co-Founder and CEO - Block | LinkedIn",                             "url": "https://www.linkedin.com/in/jack-dorsey/"},
    {"title": "Amrita Ahuja - CFO - Block | LinkedIn",                                           "url": "https://www.linkedin.com/in/amritaahuja/"},
    {"title": "Alyssa Henry - Former Head of Square - Block | LinkedIn",                         "url": "https://www.linkedin.com/in/alyssahenry/"},
    {"title": "Dena Sherwood - Chief People Officer - Block | LinkedIn",                         "url": "https://www.linkedin.com/in/denasherwood/"},
    {"title": "Sivan Whiteley - Chief Legal Officer - Block | LinkedIn",                         "url": "https://www.linkedin.com/in/sivanwhiteley/"},
    {"title": "Miles Jennings - Head of Decentralized Identity - Block | LinkedIn",              "url": "https://www.linkedin.com/in/milesjennings/"},
    {"title": "Jesse Dorogusker - Head of Square Hardware - Block | LinkedIn",                   "url": "https://www.linkedin.com/in/jdorogusker/"},
    {"title": "Tristan Dorogusker - VP Engineering Cash App - Block | LinkedIn",                 "url": "https://www.linkedin.com/in/tristandorogusker/"},
    {"title": "Tom Templeton - Head of Tidal - Block | LinkedIn",                                "url": "https://www.linkedin.com/in/tomtempleton-block/"},
    {"title": "Koia Nix - VP Product Square - Block | LinkedIn",                                 "url": "https://www.linkedin.com/in/koianix/"},
], min_required=3, max_keep=10))

print("Robinhood:", ingest_profiles("Robinhood", [
    {"title": "Vlad Tenev - Co-Founder and CEO - Robinhood | LinkedIn",                         "url": "https://www.linkedin.com/in/vladtenev/"},
    {"title": "Jason Warnick - CFO - Robinhood | LinkedIn",                                     "url": "https://www.linkedin.com/in/jasonwarnick/"},
    {"title": "Baiju Bhatt - Co-Founder and Chief Creative Officer - Robinhood | LinkedIn",     "url": "https://www.linkedin.com/in/baijubhatt/"},
    {"title": "Steve Quirk - Chief Brokerage Officer - Robinhood | LinkedIn",                   "url": "https://www.linkedin.com/in/stevequirk-rh/"},
    {"title": "JB Mackenzie - VP Futures and International - Robinhood | LinkedIn",             "url": "https://www.linkedin.com/in/jbmackenzie/"},
    {"title": "Dan Gallagher - Chief Legal Compliance and Corporate Affairs - Robinhood | LinkedIn","url": "https://www.linkedin.com/in/dangallagher-rh/"},
    {"title": "Siddharth Mehta - VP Engineering - Robinhood | LinkedIn",                        "url": "https://www.linkedin.com/in/siddharthmehta-rh/"},
    {"title": "Lucas Moskowitz - Deputy General Counsel - Robinhood | LinkedIn",                "url": "https://www.linkedin.com/in/lucasmoskowitz/"},
    {"title": "Christine Brown - VP Crypto - Robinhood | LinkedIn",                             "url": "https://www.linkedin.com/in/christinebrown-rh/"},
    {"title": "Aparna Chennapragada - Chief Product Officer - Robinhood | LinkedIn",            "url": "https://www.linkedin.com/in/aparnac/"},
], min_required=3, max_keep=10))

print("Discover Financial:", ingest_profiles("Discover Financial", [
    {"title": "Michael Rhodes - President and CEO - Discover Financial | LinkedIn",              "url": "https://www.linkedin.com/in/michaelrhodes-discover/"},
    {"title": "John Greene - EVP and CFO - Discover Financial | LinkedIn",                       "url": "https://www.linkedin.com/in/johngreene-discover/"},
    {"title": "Anil Arora - EVP and CIO - Discover Financial | LinkedIn",                        "url": "https://www.linkedin.com/in/anilarora-discover/"},
    {"title": "Lynne Laube - Chief Operating Officer - Discover Financial | LinkedIn",           "url": "https://www.linkedin.com/in/lynnelaube/"},
    {"title": "Keith Leemhuis - EVP General Counsel - Discover Financial | LinkedIn",            "url": "https://www.linkedin.com/in/keithleemhuis/"},
    {"title": "Roz Hudson - EVP Chief HR Officer - Discover Financial | LinkedIn",               "url": "https://www.linkedin.com/in/rozhudson/"},
    {"title": "Rob Sheridan - EVP Brand and Marketing - Discover Financial | LinkedIn",          "url": "https://www.linkedin.com/in/robsheridan-discover/"},
    {"title": "Diane DeBellis - EVP Products and Innovation - Discover Financial | LinkedIn",   "url": "https://www.linkedin.com/in/dianededebellis/"},
    {"title": "Craig Simms - SVP Consumer Products - Discover Financial | LinkedIn",             "url": "https://www.linkedin.com/in/craigsimms-discover/"},
    {"title": "Jennifer Kennedy - VP Investor Relations - Discover Financial | LinkedIn",        "url": "https://www.linkedin.com/in/jenniferkennedy-discover/"},
], min_required=3, max_keep=10))

print("Synchrony Financial:", ingest_profiles("Synchrony Financial", [
    {"title": "Brian Doubles - President and CEO - Synchrony Financial | LinkedIn",              "url": "https://www.linkedin.com/in/briandoubles/"},
    {"title": "Brian Wenzel - EVP and CFO - Synchrony Financial | LinkedIn",                    "url": "https://www.linkedin.com/in/brianwenzel-syf/"},
    {"title": "Alberto Casellas - EVP and COO - Synchrony Financial | LinkedIn",                "url": "https://www.linkedin.com/in/albertocasellas/"},
    {"title": "DJ Mackovak - EVP President Consumer - Synchrony Financial | LinkedIn",           "url": "https://www.linkedin.com/in/djmackovak/"},
    {"title": "Tom Quindlen - EVP President Diversified and Value - Synchrony | LinkedIn",      "url": "https://www.linkedin.com/in/tomquindlen/"},
    {"title": "Curtis Howse - EVP President Home and Auto - Synchrony Financial | LinkedIn",    "url": "https://www.linkedin.com/in/curtishowse/"},
    {"title": "Trish Mosconi - EVP Chief People Officer - Synchrony Financial | LinkedIn",      "url": "https://www.linkedin.com/in/trishmosconi/"},
    {"title": "Jonathan Mothner - EVP General Counsel - Synchrony Financial | LinkedIn",        "url": "https://www.linkedin.com/in/jonathanmothner/"},
    {"title": "Paul Musser - EVP Health and Science - Synchrony Financial | LinkedIn",          "url": "https://www.linkedin.com/in/paulmusser-syf/"},
    {"title": "Carol Juel - EVP and CTO - Synchrony Financial | LinkedIn",                      "url": "https://www.linkedin.com/in/caroljuel/"},
], min_required=3, max_keep=10))

print("\n" + "="*60); print("Available contacts per company:"); print("="*60)
with get_db() as conn:
    for c in COMPANIES:
        row = conn.execute("""
            SELECT co.name,
            SUM(CASE WHEN ct.primary_email IS NOT NULL AND ct.primary_email != ''
                     AND ct.id NOT IN (SELECT contact_id FROM send_records) THEN 1 ELSE 0 END) as avail
            FROM companies co LEFT JOIN contacts ct ON ct.company_id=co.id
            WHERE co.domain=? GROUP BY co.id
        """, (c["domain"],)).fetchone()
        print(f"  {row['name'] if row else c['name']}: {row['avail'] if row else 0} available")

print("\n" + "="*60); print("STEP 3: Creating campaign"); print("="*60)
with get_db() as conn:
    existing = conn.execute("SELECT id FROM campaigns WHERE name=?", (CAMPAIGN_NAME,)).fetchone()
    if existing:
        campaign_id = existing["id"]; print(f"  [=] Exists: {campaign_id}")
    else:
        campaign_id = new_id()
        conn.execute("INSERT INTO campaigns (id,name,status) VALUES (?,?,'active')", (campaign_id, CAMPAIGN_NAME))
        print(f"  [+] Created: {CAMPAIGN_NAME} ({campaign_id})")

print("\n" + "="*60); print("STEP 4: Personalizing — FV template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="fv",
    max_contacts_per_company=10, exclude_contacted=True)

print("\n" + "="*60); print("STEP 5: Sending from eleynxiong@berkeley.edu"); print("="*60)
gmail = GmailClient(account="default")
conn_s = sqlite3.connect("outreach.db", timeout=60)
conn_s.row_factory = sqlite3.Row
conn_s.execute("PRAGMA foreign_keys=ON"); conn_s.execute("PRAGMA busy_timeout=60000")

def safe_exec(sql, params=()):
    for _ in range(5):
        try:
            conn_s.execute(sql, params); conn_s.commit(); return
        except sqlite3.OperationalError as e:
            if "locked" in str(e): time.sleep(2)
            else: raise

rows = conn_s.execute("""
    SELECT sr.id as sr_id, ct.primary_email, ct.first_name, ct.last_name,
           co.name as company_name, pm.subject, pm.body
    FROM send_records sr
    JOIN contacts ct ON sr.contact_id=ct.id
    JOIN companies co ON ct.company_id=co.id
    JOIN personalized_messages pm ON sr.message_id=pm.id
    WHERE sr.campaign_id=? AND sr.status='queued'
    ORDER BY co.name, ct.last_name
""", (campaign_id,)).fetchall()

print(f"  {len(rows)} emails queued — sending from eleynxiong@berkeley.edu...")
total_sent = 0; total_failed = 0

for row in rows:
    retries = 0
    while retries < 3:
        try:
            result = gmail.send_email(to=row["primary_email"], subject=row["subject"],
                body=row["body"], sender_name="Eleyn Xiong", sender_email="eleynxiong@berkeley.edu")
            safe_exec("UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=? WHERE id=?",
                (result["id"], result["threadId"], datetime.now().isoformat(), row["sr_id"]))
            total_sent += 1
            print(f"  [{total_sent}] {row['company_name']} - {row['first_name']} {row['last_name']} <{row['primary_email']}>")
            break
        except ConnectionResetError:
            retries += 1
            print(f"  [retry {retries}/3] Connection reset — waiting 30s...")
            time.sleep(30)
            try: gmail = GmailClient(account="default")
            except Exception: pass
        except Exception as e:
            total_failed += 1
            print(f"  [!] FAILED {row['primary_email']}: {e}")
            safe_exec("UPDATE send_records SET status='failed',error=? WHERE id=?", (str(e)[:500], row["sr_id"]))
            break
    else:
        total_failed += 1
        safe_exec("UPDATE send_records SET status='failed',error='ConnectionResetError after 3 retries' WHERE id=?", (row["sr_id"],))
    time.sleep(random.uniform(15, 25))

conn_s.close()
print(f"\n{'='*60}\nDONE — {total_sent} sent, {total_failed} failed\nCampaign: {CAMPAIGN_NAME}\n{'='*60}")
