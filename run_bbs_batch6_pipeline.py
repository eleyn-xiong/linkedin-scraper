"""BBS Batch 6 — 5 new Fortune 500 companies, 10 emails each, eleynxiong@berkeley.edu."""
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
    {"name": "Northrop Grumman",   "domain": "northropgrumman.com", "industry": "Defense / Aerospace / Cyber / Space",             "email_pattern": "first.last"},
    {"name": "Colgate-Palmolive",  "domain": "colgatepalmolive.com","industry": "Consumer Goods / Oral Care / Personal Care",       "email_pattern": "first.last"},
    {"name": "Sherwin-Williams",   "domain": "sherwin.com",         "industry": "Coatings / Paints / Industrial Materials",         "email_pattern": "first.last"},
    {"name": "Linde",              "domain": "linde.com",           "industry": "Industrial Gases / Clean Energy / Engineering",    "email_pattern": "first.last"},
    {"name": "Carrier Global",     "domain": "carrier.com",         "industry": "HVAC / Building Tech / Refrigeration / Climate",  "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 6 - July 2026"
SENDER_VALUE_PROP = (
    "Berkeley Business Society is UC Berkeley's oldest and most selective consulting club, "
    "founded in 1999. Our alumni have gone on to lead at McKinsey, Bain, BCG, Goldman Sachs, "
    "Google, Apple, and hundreds of venture-backed startups. We work with companies on "
    "semester-long consulting engagements — market research, growth strategy, product analysis, "
    "and go-to-market planning — delivering Fortune 500-quality work from Berkeley's top "
    "analytical and business talent."
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

print("Northrop Grumman:", ingest_profiles("Northrop Grumman", [
    {"title": "Kathy Warden - Chairman President and CEO - Northrop Grumman | LinkedIn",         "url": "https://www.linkedin.com/in/kathywarden/"},
    {"title": "Dave Keffer - CFO - Northrop Grumman | LinkedIn",                                 "url": "https://www.linkedin.com/in/davekeffer/"},
    {"title": "Tom Jones - President Space Systems - Northrop Grumman | LinkedIn",               "url": "https://www.linkedin.com/in/tomjones-ng/"},
    {"title": "Janis Pamiljans - President Aeronautics Systems - Northrop Grumman | LinkedIn",   "url": "https://www.linkedin.com/in/janispamiljans/"},
    {"title": "Mike Hardesty - President Mission Systems - Northrop Grumman | LinkedIn",         "url": "https://www.linkedin.com/in/mikehardesty-ng/"},
    {"title": "Mark Caylor - President Defense Systems - Northrop Grumman | LinkedIn",           "url": "https://www.linkedin.com/in/markcaylor/"},
    {"title": "Shawn Purvis - President Enterprise Services - Northrop Grumman | LinkedIn",      "url": "https://www.linkedin.com/in/shawnpurvis/"},
    {"title": "Shawn Black - SVP General Counsel - Northrop Grumman | LinkedIn",                 "url": "https://www.linkedin.com/in/shawnblack-ng/"},
    {"title": "Aprille Ericsson - VP Research and Technology - Northrop Grumman | LinkedIn",     "url": "https://www.linkedin.com/in/aprillericsson/"},
    {"title": "Denise Peppard - SVP Chief HR Officer - Northrop Grumman | LinkedIn",             "url": "https://www.linkedin.com/in/denisepeppard/"},
], min_required=3, max_keep=10))

print("Colgate-Palmolive:", ingest_profiles("Colgate-Palmolive", [
    {"title": "Noel Wallace - Chairman President and CEO - Colgate-Palmolive | LinkedIn",        "url": "https://www.linkedin.com/in/noelwallace/"},
    {"title": "Stan Sutula - EVP and CFO - Colgate-Palmolive | LinkedIn",                        "url": "https://www.linkedin.com/in/stansutula/"},
    {"title": "Prabha Parameswaran - President Asia Pacific - Colgate-Palmolive | LinkedIn",     "url": "https://www.linkedin.com/in/prabhaparameswaran/"},
    {"title": "Mukul Deoras - President North America - Colgate-Palmolive | LinkedIn",           "url": "https://www.linkedin.com/in/mukuldeoras/"},
    {"title": "Diana Toche - EVP Chief Growth and Strategy Officer - Colgate | LinkedIn",        "url": "https://www.linkedin.com/in/dianatoche/"},
    {"title": "Jennifer Daniels - EVP General Counsel - Colgate-Palmolive | LinkedIn",           "url": "https://www.linkedin.com/in/jenniferdaniels-colgate/"},
    {"title": "Patricia Verduin - SVP and CTO - Colgate-Palmolive | LinkedIn",                   "url": "https://www.linkedin.com/in/patriciaverduin/"},
    {"title": "Eleni Kosmas - EVP Chief HR Officer - Colgate-Palmolive | LinkedIn",              "url": "https://www.linkedin.com/in/elenikosmas/"},
    {"title": "Brigitte King - Chief Digital Officer - Colgate-Palmolive | LinkedIn",            "url": "https://www.linkedin.com/in/brigitteking/"},
    {"title": "Marc Rosen - President Europe - Colgate-Palmolive | LinkedIn",                    "url": "https://www.linkedin.com/in/marcrosen-colgate/"},
], min_required=3, max_keep=10))

print("Sherwin-Williams:", ingest_profiles("Sherwin-Williams", [
    {"title": "Heidi Petz - President and CEO - Sherwin-Williams | LinkedIn",                    "url": "https://www.linkedin.com/in/heidipetz/"},
    {"title": "Al Mistysyn - SVP Finance and CFO - Sherwin-Williams | LinkedIn",                 "url": "https://www.linkedin.com/in/almistysyn/"},
    {"title": "Justin Binns - President Paint Stores Group - Sherwin-Williams | LinkedIn",       "url": "https://www.linkedin.com/in/justinbinns-sw/"},
    {"title": "Dave Sewell - President Consumer Brands Group - Sherwin-Williams | LinkedIn",     "url": "https://www.linkedin.com/in/davesewell-sw/"},
    {"title": "Todd Rea - President Performance Coatings Group - Sherwin-Williams | LinkedIn",   "url": "https://www.linkedin.com/in/toddrea-sw/"},
    {"title": "Karl Jorgenrud - SVP Strategy - Sherwin-Williams | LinkedIn",                     "url": "https://www.linkedin.com/in/karljorgenrud/"},
    {"title": "Steven Mezger - SVP General Counsel - Sherwin-Williams | LinkedIn",               "url": "https://www.linkedin.com/in/stevenmezger/"},
    {"title": "Jane Chronister - SVP HR - Sherwin-Williams | LinkedIn",                          "url": "https://www.linkedin.com/in/janechronister/"},
    {"title": "Tom Gillette - President Latin America Group - Sherwin-Williams | LinkedIn",      "url": "https://www.linkedin.com/in/tomgillette-sw/"},
    {"title": "Bryan Young - VP Investor Relations - Sherwin-Williams | LinkedIn",               "url": "https://www.linkedin.com/in/bryanyoung-sw/"},
], min_required=3, max_keep=10))

print("Linde:", ingest_profiles("Linde", [
    {"title": "Sanjiv Lamba - CEO - Linde | LinkedIn",                                           "url": "https://www.linkedin.com/in/sanjivlamba/"},
    {"title": "Matt White - EVP and CFO - Linde | LinkedIn",                                     "url": "https://www.linkedin.com/in/mattwhite-linde/"},
    {"title": "Christian Bruch - Former CEO Linde - Linde | LinkedIn",                           "url": "https://www.linkedin.com/in/christianbruch/"},
    {"title": "Bernd Eulitz - EVP Americas - Linde | LinkedIn",                                  "url": "https://www.linkedin.com/in/brndeulitz/"},
    {"title": "Anne Quart - EVP EMEA - Linde | LinkedIn",                                        "url": "https://www.linkedin.com/in/annequart/"},
    {"title": "Vivek Mehta - EVP APAC - Linde | LinkedIn",                                       "url": "https://www.linkedin.com/in/vivekmehta-linde/"},
    {"title": "Mark Vreporting - EVP Global Sales - Linde | LinkedIn",                            "url": "https://www.linkedin.com/in/markvreporting/"},
    {"title": "Simon Wandke - Chief HR Officer - Linde | LinkedIn",                              "url": "https://www.linkedin.com/in/simonwandke/"},
    {"title": "Kevin Murphy - SVP General Counsel - Linde | LinkedIn",                           "url": "https://www.linkedin.com/in/kevinmurphy-linde/"},
    {"title": "Juan Carlos Gonzalez - VP Strategy - Linde | LinkedIn",                           "url": "https://www.linkedin.com/in/juancarlosgonzalez-linde/"},
], min_required=3, max_keep=10))

print("Carrier Global:", ingest_profiles("Carrier Global", [
    {"title": "David Gitlin - Chairman and CEO - Carrier Global | LinkedIn",                     "url": "https://www.linkedin.com/in/davidgitlin/"},
    {"title": "Patrick Goris - SVP and CFO - Carrier Global | LinkedIn",                         "url": "https://www.linkedin.com/in/patrickgoris/"},
    {"title": "Jurgen Timperman - President Carrier Americas - Carrier Global | LinkedIn",        "url": "https://www.linkedin.com/in/jurgentimperman/"},
    {"title": "Tim White - President Carrier EMEA - Carrier Global | LinkedIn",                  "url": "https://www.linkedin.com/in/timwhite-carrier/"},
    {"title": "John Mandyck - Chief Sustainability Officer - Carrier Global | LinkedIn",         "url": "https://www.linkedin.com/in/johnmandyck/"},
    {"title": "Kyle Crockett - SVP and Chief HR Officer - Carrier Global | LinkedIn",            "url": "https://www.linkedin.com/in/kylecrockett-carrier/"},
    {"title": "Ajay Agrawal - President Carrier Asia Pacific - Carrier Global | LinkedIn",       "url": "https://www.linkedin.com/in/ajayagrawal-carrier/"},
    {"title": "Mark Alles - SVP General Counsel - Carrier Global | LinkedIn",                    "url": "https://www.linkedin.com/in/markalles-carrier/"},
    {"title": "Stephen Tusa - VP Investor Relations - Carrier Global | LinkedIn",                "url": "https://www.linkedin.com/in/stephentusa/"},
    {"title": "Virginia Trischitta - VP Communications - Carrier Global | LinkedIn",             "url": "https://www.linkedin.com/in/virginiatrischitta/"},
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

print("\n" + "="*60); print("STEP 4: Personalizing — BBS template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="bbs",
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
