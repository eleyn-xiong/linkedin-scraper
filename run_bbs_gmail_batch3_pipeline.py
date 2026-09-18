"""BBS Gmail Batch 3 — 30 new companies, eleynxiong@gmail.com."""
import sys, time, random, sqlite3
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
config.SENDER_EMAIL = "eleynxiong@gmail.com"
config.SENDER_NAME  = "Eleyn Xiong"

from db import get_db, new_id, init_db
from linkedin_ingest import ingest_profiles
from personalize_once import personalize_once_per_company
from gmail_client import GmailClient
from datetime import datetime

init_db()

COMPANIES = [
    {"name": "Google DeepMind",    "domain": "deepmind.google",      "industry": "AI Research / Safety",                   "email_pattern": "first.last"},
    {"name": "LinkedIn",           "domain": "linkedin.com",          "industry": "Professional Networking / SaaS",          "email_pattern": "first.last"},
    {"name": "xAI",                "domain": "x.ai",                  "industry": "AI / Large Language Models",              "email_pattern": "first.last"},
    {"name": "SpaceX",             "domain": "spacex.com",            "industry": "Aerospace / Rocket / Satellite",          "email_pattern": "first.last"},
    {"name": "Applied Materials",  "domain": "appliedmaterials.com",  "industry": "Semiconductor Equipment / Materials",     "email_pattern": "first.last"},
    {"name": "Arm",                "domain": "arm.com",               "industry": "Semiconductor IP / CPU Architecture",     "email_pattern": "first.last"},
    {"name": "Akamai",             "domain": "akamai.com",            "industry": "CDN / Cloud Security / Edge Computing",   "email_pattern": "first.last"},
    {"name": "Equinix",            "domain": "equinix.com",           "industry": "Data Centers / Colocation / Cloud",       "email_pattern": "first.last"},
    {"name": "Fortinet",           "domain": "fortinet.com",          "industry": "Network Security / Firewalls",            "email_pattern": "first.last"},
    {"name": "Elastic",            "domain": "elastic.co",            "industry": "Search / Observability / Security SaaS",  "email_pattern": "first.last"},
    {"name": "Roche",              "domain": "roche.com",             "industry": "Pharma / Diagnostics / Biotech",          "email_pattern": "first.last"},
    {"name": "ASML",               "domain": "asml.com",              "industry": "Semiconductor Lithography / EUV",         "email_pattern": "first.last"},
    {"name": "Genentech",          "domain": "gene.com",              "industry": "Biotech / Oncology / Drug Discovery",     "email_pattern": "first.last"},
    {"name": "Moderna",            "domain": "modernatx.com",         "industry": "Biotech / mRNA / Vaccines",               "email_pattern": "first.last"},
    {"name": "Airbus",             "domain": "airbus.com",            "industry": "Aerospace / Defense / Aviation",          "email_pattern": "first.last"},
    {"name": "Northrop Grumman",   "domain": "northropgrumman.com",   "industry": "Defense / Aerospace / Cyber",             "email_pattern": "first.last"},
    {"name": "Boston Dynamics",    "domain": "bostondynamics.com",    "industry": "Robotics / AI / Automation",              "email_pattern": "first.last"},
    {"name": "ByteDance",          "domain": "bytedance.com",         "industry": "Social Media / AI / Content",             "email_pattern": "first.last"},
    {"name": "Micron",             "domain": "micron.com",            "industry": "Memory / DRAM / NAND / Semiconductors",   "email_pattern": "first.last"},
    {"name": "Electronic Arts",    "domain": "ea.com",                "industry": "Gaming / Interactive Entertainment",      "email_pattern": "first.last"},
    {"name": "Robinhood",          "domain": "robinhood.com",         "industry": "Fintech / Retail Investing / Crypto",     "email_pattern": "first.last"},
    {"name": "Marvell",            "domain": "marvell.com",           "industry": "Semiconductors / Data Infrastructure",    "email_pattern": "first.last"},
    {"name": "Fivetran",           "domain": "fivetran.com",          "industry": "Data Integration / ETL / Cloud",          "email_pattern": "first.last"},
    {"name": "dbt Labs",           "domain": "getdbt.com",            "industry": "Data Transformation / Analytics Eng",    "email_pattern": "first.last"},
    {"name": "Box",                "domain": "box.com",               "industry": "Cloud Content Management / Enterprise",   "email_pattern": "first.last"},
    {"name": "Dataiku",            "domain": "dataiku.com",           "industry": "AI / Data Science Platform / MLOps",     "email_pattern": "first.last"},
    {"name": "Celonis",            "domain": "celonis.com",           "industry": "Process Mining / ERP Analytics",          "email_pattern": "first.last"},
    {"name": "Cloudera",           "domain": "cloudera.com",          "industry": "Data Platform / Hadoop / Cloud",          "email_pattern": "first.last"},
    {"name": "Southwest Airlines", "domain": "southwest.com",         "industry": "Aviation / Low-Cost Carrier",             "email_pattern": "first.last"},
    {"name": "Alaska Airlines",    "domain": "alaskaair.com",         "industry": "Aviation / Travel / Loyalty",             "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Gmail Batch 3 - June 2026"
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

print("Google DeepMind:", ingest_profiles("Google DeepMind", [
    {"title": "Demis Hassabis - CEO - Google DeepMind | LinkedIn",                        "url": "https://www.linkedin.com/in/demishassabis/"},
    {"title": "Shane Legg - Chief AGI Scientist - Google DeepMind | LinkedIn",            "url": "https://www.linkedin.com/in/shanelegg/"},
    {"title": "Koray Kavukcuoglu - VP Research - Google DeepMind | LinkedIn",             "url": "https://www.linkedin.com/in/korayk/"},
    {"title": "Lila Ibrahim - COO - Google DeepMind | LinkedIn",                          "url": "https://www.linkedin.com/in/lilaibrahim/"},
    {"title": "Pushmeet Kohli - VP Research - Google DeepMind | LinkedIn",                "url": "https://www.linkedin.com/in/pushmeetkohli/"},
    {"title": "Jeff Dean - Chief Scientist Google - Google DeepMind | LinkedIn",          "url": "https://www.linkedin.com/in/jeffdean/"},
    {"title": "Oriol Vinyals - VP Research - Google DeepMind | LinkedIn",                 "url": "https://www.linkedin.com/in/oriol-vinyals/"},
    {"title": "David Silver - Principal Research Scientist - Google DeepMind | LinkedIn", "url": "https://www.linkedin.com/in/davidsilver-deepmind/"},
    {"title": "Raia Hadsell - VP Research Robotics - Google DeepMind | LinkedIn",        "url": "https://www.linkedin.com/in/raiahadsell/"},
    {"title": "Karen Simonyan - VP Research - Google DeepMind | LinkedIn",                "url": "https://www.linkedin.com/in/karensimonyan/"},
], min_required=3, max_keep=10))

print("LinkedIn:", ingest_profiles("LinkedIn", [
    {"title": "Ryan Roslansky - CEO - LinkedIn | LinkedIn",                               "url": "https://www.linkedin.com/in/ryanroslansky/"},
    {"title": "Tomer Cohen - Chief Product Officer - LinkedIn | LinkedIn",                "url": "https://www.linkedin.com/in/tomercohen/"},
    {"title": "Mohak Shroff - SVP Engineering - LinkedIn | LinkedIn",                     "url": "https://www.linkedin.com/in/mohakshroff/"},
    {"title": "Erran Berger - VP Engineering - LinkedIn | LinkedIn",                      "url": "https://www.linkedin.com/in/erranberger/"},
    {"title": "Gyanda Sachdeva - VP Product - LinkedIn | LinkedIn",                       "url": "https://www.linkedin.com/in/gyandasachdeva/"},
    {"title": "Britney Schultz - Chief Marketing Officer - LinkedIn | LinkedIn",          "url": "https://www.linkedin.com/in/britneyschultz/"},
    {"title": "Feon Ang - VP APAC - LinkedIn | LinkedIn",                                 "url": "https://www.linkedin.com/in/feonang/"},
    {"title": "Shishir Gupta - VP Sales Solutions - LinkedIn | LinkedIn",                 "url": "https://www.linkedin.com/in/shishirgupta/"},
    {"title": "Alice Xiong - VP Trust and Safety - LinkedIn | LinkedIn",                  "url": "https://www.linkedin.com/in/alicexiong/"},
    {"title": "Belinda Wong - VP China - LinkedIn | LinkedIn",                            "url": "https://www.linkedin.com/in/belindawong/"},
], min_required=3, max_keep=10))

print("xAI:", ingest_profiles("xAI", [
    {"title": "Elon Musk - Founder - xAI | LinkedIn",                                     "url": "https://www.linkedin.com/in/elonmusk/"},
    {"title": "Greg Yang - Co-Founder - xAI | LinkedIn",                                  "url": "https://www.linkedin.com/in/gregyang-xai/"},
    {"title": "Igor Babuschkin - Co-Founder - xAI | LinkedIn",                            "url": "https://www.linkedin.com/in/igorbabuschkin/"},
    {"title": "Tony Wu - Co-Founder - xAI | LinkedIn",                                    "url": "https://www.linkedin.com/in/tonywu-xai/"},
    {"title": "Kyle Kosic - Co-Founder - xAI | LinkedIn",                                 "url": "https://www.linkedin.com/in/kylekosic/"},
    {"title": "Jimmy Ba - Co-Founder - xAI | LinkedIn",                                   "url": "https://www.linkedin.com/in/jimmylba/"},
    {"title": "Yuhuai Wu - Co-Founder - xAI | LinkedIn",                                  "url": "https://www.linkedin.com/in/yuhuaiwu/"},
    {"title": "Zihang Dai - Research Scientist - xAI | LinkedIn",                         "url": "https://www.linkedin.com/in/zihangdai/"},
    {"title": "Eric Wallace - Research Scientist - xAI | LinkedIn",                       "url": "https://www.linkedin.com/in/ericwallace-xai/"},
    {"title": "Jared Kaplan - Research Lead - xAI | LinkedIn",                            "url": "https://www.linkedin.com/in/jaredkaplan-xai/"},
], min_required=3, max_keep=10))

print("SpaceX:", ingest_profiles("SpaceX", [
    {"title": "Elon Musk - CEO - SpaceX | LinkedIn",                                      "url": "https://www.linkedin.com/in/elonmusk/"},
    {"title": "Gwynne Shotwell - President and COO - SpaceX | LinkedIn",                  "url": "https://www.linkedin.com/in/gwynneshortwell/"},
    {"title": "Tom Mueller - Former VP Propulsion - SpaceX | LinkedIn",                   "url": "https://www.linkedin.com/in/tommueller-spacex/"},
    {"title": "Mark Juncosa - VP Vehicle Engineering - SpaceX | LinkedIn",                "url": "https://www.linkedin.com/in/markjuncosa/"},
    {"title": "Brian Bjelde - VP Human Resources - SpaceX | LinkedIn",                    "url": "https://www.linkedin.com/in/brianbjelde/"},
    {"title": "Lauren Lyons - VP Finance - SpaceX | LinkedIn",                            "url": "https://www.linkedin.com/in/laurenlyons-spacex/"},
    {"title": "Chris Kemp - Former CTO - SpaceX | LinkedIn",                              "url": "https://www.linkedin.com/in/chriskemp/"},
    {"title": "Phil Kassouf - VP Starlink Sales - SpaceX | LinkedIn",                     "url": "https://www.linkedin.com/in/philkassouf/"},
    {"title": "Jessica Jensen - VP Customer Operations - SpaceX | LinkedIn",              "url": "https://www.linkedin.com/in/jessicajensen-spacex/"},
    {"title": "William Gerstenmaier - VP Build and Flight Reliability - SpaceX | LinkedIn","url": "https://www.linkedin.com/in/williamgerstenmaier/"},
], min_required=3, max_keep=10))

print("Applied Materials:", ingest_profiles("Applied Materials", [
    {"title": "Gary Dickerson - President and CEO - Applied Materials | LinkedIn",         "url": "https://www.linkedin.com/in/garydickerson/"},
    {"title": "Brice Hill - CFO - Applied Materials | LinkedIn",                          "url": "https://www.linkedin.com/in/bricehill/"},
    {"title": "Prabu Raja - President Semiconductor Products - Applied Materials | LinkedIn","url": "https://www.linkedin.com/in/prabusraja/"},
    {"title": "Om Nalamasu - CTO - Applied Materials | LinkedIn",                         "url": "https://www.linkedin.com/in/omnalamasu/"},
    {"title": "Ali Sanat - President Display and Flexible Technology - Applied Materials | LinkedIn","url": "https://www.linkedin.com/in/alisanat/"},
    {"title": "Teri Little - Chief Legal Officer - Applied Materials | LinkedIn",         "url": "https://www.linkedin.com/in/terilittleamat/"},
    {"title": "Tom Larkins - VP HR - Applied Materials | LinkedIn",                       "url": "https://www.linkedin.com/in/tomlarkins/"},
    {"title": "David Xu - VP Strategy - Applied Materials | LinkedIn",                    "url": "https://www.linkedin.com/in/davidxu-amat/"},
    {"title": "Sundar Ramamurthy - VP Etch Products - Applied Materials | LinkedIn",      "url": "https://www.linkedin.com/in/sundarramamurthy/"},
    {"title": "Steve Ghanayem - SVP Metals Deposition - Applied Materials | LinkedIn",   "url": "https://www.linkedin.com/in/steveghanayem/"},
], min_required=3, max_keep=10))

print("Arm:", ingest_profiles("Arm", [
    {"title": "Rene Haas - CEO - Arm | LinkedIn",                                         "url": "https://www.linkedin.com/in/renehaas/"},
    {"title": "Inder Singh - CFO - Arm | LinkedIn",                                       "url": "https://www.linkedin.com/in/indersingh-arm/"},
    {"title": "Chris Bergey - SVP Client Line of Business - Arm | LinkedIn",              "url": "https://www.linkedin.com/in/chrisbergey/"},
    {"title": "Mohamed Awad - SVP Infrastructure Line of Business - Arm | LinkedIn",      "url": "https://www.linkedin.com/in/mohamedawad/"},
    {"title": "Paul Williamson - SVP IoT - Arm | LinkedIn",                               "url": "https://www.linkedin.com/in/paulwilliamson-arm/"},
    {"title": "Dipti Vachani - SVP Automotive - Arm | LinkedIn",                          "url": "https://www.linkedin.com/in/diptivachani/"},
    {"title": "Mark Hambleton - VP Open Source Software - Arm | LinkedIn",                "url": "https://www.linkedin.com/in/markhambleton/"},
    {"title": "Andrea Rip - Chief People Officer - Arm | LinkedIn",                       "url": "https://www.linkedin.com/in/andrearip/"},
    {"title": "Ian Smythe - VP Marketing - Arm | LinkedIn",                               "url": "https://www.linkedin.com/in/iansmythe-arm/"},
    {"title": "Tim Whitfield - VP Solutions Engineering - Arm | LinkedIn",                "url": "https://www.linkedin.com/in/timwhitfield-arm/"},
], min_required=3, max_keep=10))

print("Akamai:", ingest_profiles("Akamai", [
    {"title": "Tom Leighton - CEO - Akamai | LinkedIn",                                   "url": "https://www.linkedin.com/in/tomleighton/"},
    {"title": "Ed McGowan - CFO - Akamai | LinkedIn",                                     "url": "https://www.linkedin.com/in/edmcgowan/"},
    {"title": "Robert Blumofe - EVP and CTO - Akamai | LinkedIn",                         "url": "https://www.linkedin.com/in/rblumofe/"},
    {"title": "Kim Salem-Jackson - CMO - Akamai | LinkedIn",                              "url": "https://www.linkedin.com/in/kimsalemjackson/"},
    {"title": "Paul Joseph - EVP Global Sales - Akamai | LinkedIn",                       "url": "https://www.linkedin.com/in/pauljoseph-akamai/"},
    {"title": "Mani Sundaram - EVP Global Services - Akamai | LinkedIn",                  "url": "https://www.linkedin.com/in/manisundaram/"},
    {"title": "Adam Karon - President Cloud Computing - Akamai | LinkedIn",               "url": "https://www.linkedin.com/in/adamkaron/"},
    {"title": "Reuven Cohen - CTO Emerging Technology - Akamai | LinkedIn",              "url": "https://www.linkedin.com/in/reuvencohen/"},
    {"title": "Lisa Hammitt - Chief People Officer - Akamai | LinkedIn",                  "url": "https://www.linkedin.com/in/lisahammitt/"},
    {"title": "Patrick Sullivan - SVP Security Strategy - Akamai | LinkedIn",             "url": "https://www.linkedin.com/in/patricksullivan-akamai/"},
], min_required=3, max_keep=10))

print("Equinix:", ingest_profiles("Equinix", [
    {"title": "Charles Meyers - CEO - Equinix | LinkedIn",                                "url": "https://www.linkedin.com/in/charlesmeyers/"},
    {"title": "Keith Taylor - CFO - Equinix | LinkedIn",                                  "url": "https://www.linkedin.com/in/keithtaylor-equinix/"},
    {"title": "Sara Baack - Chief Product Officer - Equinix | LinkedIn",                  "url": "https://www.linkedin.com/in/sarabaack/"},
    {"title": "Brandi Galvin Morandi - General Counsel - Equinix | LinkedIn",             "url": "https://www.linkedin.com/in/brandigalvinmorandi/"},
    {"title": "Eric Schwartz - President Americas - Equinix | LinkedIn",                  "url": "https://www.linkedin.com/in/ericschwartz-equinix/"},
    {"title": "Jeremy Deutsch - President EMEA - Equinix | LinkedIn",                     "url": "https://www.linkedin.com/in/jeremydeutsch/"},
    {"title": "Samuel Lee - President Asia Pacific - Equinix | LinkedIn",                 "url": "https://www.linkedin.com/in/samuellee-equinix/"},
    {"title": "Milind Wagle - Chief Information Officer - Equinix | LinkedIn",            "url": "https://www.linkedin.com/in/milindwagle/"},
    {"title": "Lahav Gil - Chief Strategy Officer - Equinix | LinkedIn",                  "url": "https://www.linkedin.com/in/lahavgil/"},
    {"title": "Randi Lyn Corbin - Chief People Officer - Equinix | LinkedIn",             "url": "https://www.linkedin.com/in/randilyn/"},
], min_required=3, max_keep=10))

print("Fortinet:", ingest_profiles("Fortinet", [
    {"title": "Ken Xie - Founder and CEO - Fortinet | LinkedIn",                          "url": "https://www.linkedin.com/in/kenxie/"},
    {"title": "Michael Xie - Co-Founder and CTO - Fortinet | LinkedIn",                  "url": "https://www.linkedin.com/in/michaelxie-fortinet/"},
    {"title": "Keith Jensen - CFO - Fortinet | LinkedIn",                                 "url": "https://www.linkedin.com/in/keithjensen-fortinet/"},
    {"title": "John Maddison - CMO and EVP Products - Fortinet | LinkedIn",               "url": "https://www.linkedin.com/in/johnmaddison/"},
    {"title": "Patrice Perche - SVP International Sales - Fortinet | LinkedIn",           "url": "https://www.linkedin.com/in/patriceperche/"},
    {"title": "Amit Singh - President Google Cloud - Fortinet | LinkedIn",                "url": "https://www.linkedin.com/in/amitsingh-fortinet/"},
    {"title": "Sherri Liebo - Chief People Officer - Fortinet | LinkedIn",                "url": "https://www.linkedin.com/in/sherriliebo/"},
    {"title": "Derek Manky - Chief Security Strategist - Fortinet | LinkedIn",            "url": "https://www.linkedin.com/in/derekmanky/"},
    {"title": "Rob Rashotte - VP Global Training - Fortinet | LinkedIn",                  "url": "https://www.linkedin.com/in/robrashotte/"},
    {"title": "Nirav Shah - SVP Products and Solutions - Fortinet | LinkedIn",            "url": "https://www.linkedin.com/in/niravshah-fortinet/"},
], min_required=3, max_keep=10))

print("Elastic:", ingest_profiles("Elastic", [
    {"title": "Ash Kulkarni - CEO - Elastic | LinkedIn",                                  "url": "https://www.linkedin.com/in/ashkulkarni/"},
    {"title": "Janesh Moorjani - CFO - Elastic | LinkedIn",                               "url": "https://www.linkedin.com/in/janeshmoorjani/"},
    {"title": "Ken Exner - Chief Product Officer - Elastic | LinkedIn",                   "url": "https://www.linkedin.com/in/kenexner/"},
    {"title": "Shay Banon - Founder and CTO - Elastic | LinkedIn",                        "url": "https://www.linkedin.com/in/kimchy/"},
    {"title": "Gareth Simons - Chief Revenue Officer - Elastic | LinkedIn",               "url": "https://www.linkedin.com/in/garethsimons/"},
    {"title": "Dov Dorin - VP Engineering - Elastic | LinkedIn",                          "url": "https://www.linkedin.com/in/dovdorin/"},
    {"title": "Julie Rae - Chief People Officer - Elastic | LinkedIn",                    "url": "https://www.linkedin.com/in/julierae-elastic/"},
    {"title": "Nate Taber - VP Marketing - Elastic | LinkedIn",                           "url": "https://www.linkedin.com/in/natetaber/"},
    {"title": "Jean-Denis Greze - VP Engineering - Elastic | LinkedIn",                   "url": "https://www.linkedin.com/in/jeandenisgreze/"},
    {"title": "Steve Kearns - VP Product Security - Elastic | LinkedIn",                  "url": "https://www.linkedin.com/in/stevekearns-elastic/"},
], min_required=3, max_keep=10))

print("Roche:", ingest_profiles("Roche", [
    {"title": "Thomas Schinecker - CEO - Roche | LinkedIn",                               "url": "https://www.linkedin.com/in/thomasschinecker/"},
    {"title": "Alan Hippe - CFO - Roche | LinkedIn",                                      "url": "https://www.linkedin.com/in/alanhippe/"},
    {"title": "Matt Sause - CEO Roche Diagnostics - Roche | LinkedIn",                   "url": "https://www.linkedin.com/in/mattsause/"},
    {"title": "Levi Garraway - Chief Medical Officer - Roche | LinkedIn",                 "url": "https://www.linkedin.com/in/levigarraway/"},
    {"title": "Jessica Federer - Chief Digital Officer - Roche | LinkedIn",               "url": "https://www.linkedin.com/in/jessicafederer/"},
    {"title": "James Sabry - SVP Global Partnering - Roche | LinkedIn",                   "url": "https://www.linkedin.com/in/jamessabry/"},
    {"title": "Severin Schwan - Former CEO - Roche | LinkedIn",                           "url": "https://www.linkedin.com/in/severinschwan/"},
    {"title": "Michael Heuer - CEO Roche Diagnostics Americas | LinkedIn",                "url": "https://www.linkedin.com/in/michaelheuer/"},
    {"title": "Carolyn Slaski - EVP People - Roche | LinkedIn",                          "url": "https://www.linkedin.com/in/carolynslaski/"},
    {"title": "Hans Clevers - Head of Pharma Research - Roche | LinkedIn",                "url": "https://www.linkedin.com/in/hansclevers/"},
], min_required=3, max_keep=10))

print("ASML:", ingest_profiles("ASML", [
    {"title": "Peter Wennink - CEO - ASML | LinkedIn",                                    "url": "https://www.linkedin.com/in/peterwennink/"},
    {"title": "Roger Dassen - CFO - ASML | LinkedIn",                                     "url": "https://www.linkedin.com/in/rogerdassen/"},
    {"title": "Martin van den Brink - President and CTO - ASML | LinkedIn",               "url": "https://www.linkedin.com/in/martinvandenbrink/"},
    {"title": "Frits van Hout - EVP Chief Strategy Officer - ASML | LinkedIn",            "url": "https://www.linkedin.com/in/fritsvanout/"},
    {"title": "Christophe Fouquet - CEO - ASML | LinkedIn",                               "url": "https://www.linkedin.com/in/christophefouquet/"},
    {"title": "Wayne Allan - EVP Customer Support - ASML | LinkedIn",                     "url": "https://www.linkedin.com/in/wayneallan/"},
    {"title": "Muriël Laane - Chief Legal Officer - ASML | LinkedIn",                     "url": "https://www.linkedin.com/in/muriellaane/"},
    {"title": "Ji-Young Chang - VP Korea - ASML | LinkedIn",                              "url": "https://www.linkedin.com/in/jiyoungchang-asml/"},
    {"title": "Tammy Lowry - Chief People Officer - ASML | LinkedIn",                     "url": "https://www.linkedin.com/in/tammylowry/"},
    {"title": "Skip Miller - VP Americas Sales - ASML | LinkedIn",                        "url": "https://www.linkedin.com/in/skipmiller-asml/"},
], min_required=3, max_keep=10))

print("Genentech:", ingest_profiles("Genentech", [
    {"title": "Alexander Hardy - CEO - Genentech | LinkedIn",                             "url": "https://www.linkedin.com/in/alexanderhardy/"},
    {"title": "Levi Garraway - Chief Medical Officer - Genentech | LinkedIn",             "url": "https://www.linkedin.com/in/levigarraway/"},
    {"title": "Andrew Schlessinger - Chief Scientific Officer - Genentech | LinkedIn",    "url": "https://www.linkedin.com/in/andrewschlessinger/"},
    {"title": "Dietmar Berger - CMO Oncology - Genentech | LinkedIn",                    "url": "https://www.linkedin.com/in/dietmarberger/"},
    {"title": "Carole Ho - VP Clinical Development - Genentech | LinkedIn",               "url": "https://www.linkedin.com/in/caroleho/"},
    {"title": "Dan O'Day - Former CEO - Genentech | LinkedIn",                            "url": "https://www.linkedin.com/in/danoday/"},
    {"title": "Quita Highsmith - VP Chief Diversity Officer - Genentech | LinkedIn",     "url": "https://www.linkedin.com/in/quitahighsmith/"},
    {"title": "Evan Rachlin - VP Commercial - Genentech | LinkedIn",                     "url": "https://www.linkedin.com/in/evanrachlin/"},
    {"title": "Sophie Kornowski - CMO - Genentech | LinkedIn",                            "url": "https://www.linkedin.com/in/sophiekornowski/"},
    {"title": "Marc Tessier-Lavigne - SVP Research - Genentech | LinkedIn",              "url": "https://www.linkedin.com/in/marctessierlavigne/"},
], min_required=3, max_keep=10))

print("Moderna:", ingest_profiles("Moderna", [
    {"title": "Stephane Bancel - CEO - Moderna | LinkedIn",                               "url": "https://www.linkedin.com/in/stephanebancel/"},
    {"title": "James Mock - CFO - Moderna | LinkedIn",                                    "url": "https://www.linkedin.com/in/jamesmock/"},
    {"title": "Arpa Garay - CMO - Moderna | LinkedIn",                                    "url": "https://www.linkedin.com/in/arparagaray/"},
    {"title": "Stephen Hoge - President - Moderna | LinkedIn",                            "url": "https://www.linkedin.com/in/stephenhoge/"},
    {"title": "Noubar Afeyan - Co-Founder and Chairman - Moderna | LinkedIn",             "url": "https://www.linkedin.com/in/noubarafeyan/"},
    {"title": "Tal Zaks - Former CMO - Moderna | LinkedIn",                               "url": "https://www.linkedin.com/in/talzaks/"},
    {"title": "Shannon Thyme Klinger - Chief Legal and Compliance Officer - Moderna | LinkedIn","url": "https://www.linkedin.com/in/shannonthymeklinger/"},
    {"title": "Tracey Franklin - Chief People Officer - Moderna | LinkedIn",              "url": "https://www.linkedin.com/in/traceyfranklin/"},
    {"title": "Lavanya Mahendran - VP Commercial Strategy - Moderna | LinkedIn",          "url": "https://www.linkedin.com/in/lavanyamahendran/"},
    {"title": "Kyle Hurst - VP Global Manufacturing - Moderna | LinkedIn",                "url": "https://www.linkedin.com/in/kylehurst-moderna/"},
], min_required=3, max_keep=10))

print("Airbus:", ingest_profiles("Airbus", [
    {"title": "Guillaume Faury - CEO - Airbus | LinkedIn",                                "url": "https://www.linkedin.com/in/guillaumefaury/"},
    {"title": "Thomas Toepfer - CFO - Airbus | LinkedIn",                                 "url": "https://www.linkedin.com/in/thomastoepfer/"},
    {"title": "Christian Scherer - Chief Commercial Officer - Airbus | LinkedIn",         "url": "https://www.linkedin.com/in/christianscherer/"},
    {"title": "Michael Schoellhorn - CEO Defence and Space - Airbus | LinkedIn",          "url": "https://www.linkedin.com/in/michaelschoellhorn/"},
    {"title": "Rob Dewar - VP Engineering Helicopters - Airbus | LinkedIn",               "url": "https://www.linkedin.com/in/robdewar-airbus/"},
    {"title": "Julie Kitcher - EVP Communications - Airbus | LinkedIn",                   "url": "https://www.linkedin.com/in/juliekitcher/"},
    {"title": "Jean-Brice Dumont - EVP Engineering - Airbus | LinkedIn",                  "url": "https://www.linkedin.com/in/jeanbrice-dumont/"},
    {"title": "Sabine Klauke - CTO - Airbus | LinkedIn",                                  "url": "https://www.linkedin.com/in/sabineklauke/"},
    {"title": "Thierry Baril - Chief HR Officer - Airbus | LinkedIn",                     "url": "https://www.linkedin.com/in/thierrybaril/"},
    {"title": "Philippe Mhun - EVP Programs - Airbus | LinkedIn",                         "url": "https://www.linkedin.com/in/philippemhun/"},
], min_required=3, max_keep=10))

print("Northrop Grumman:", ingest_profiles("Northrop Grumman", [
    {"title": "Kathy Warden - CEO - Northrop Grumman | LinkedIn",                         "url": "https://www.linkedin.com/in/kathywarden/"},
    {"title": "Dave Keffer - CFO - Northrop Grumman | LinkedIn",                          "url": "https://www.linkedin.com/in/davekeffer/"},
    {"title": "Tom Jones - President Aeronautics Systems - Northrop Grumman | LinkedIn",  "url": "https://www.linkedin.com/in/tomjones-northrop/"},
    {"title": "Mary Petryszyn - President Defense Systems - Northrop Grumman | LinkedIn", "url": "https://www.linkedin.com/in/marypetryszyn/"},
    {"title": "Blake Larson - President Mission Systems - Northrop Grumman | LinkedIn",   "url": "https://www.linkedin.com/in/blakelarson/"},
    {"title": "Roshan Roeder - VP Strategy - Northrop Grumman | LinkedIn",                "url": "https://www.linkedin.com/in/roshanroeder/"},
    {"title": "Lesley Kalan - VP Communications - Northrop Grumman | LinkedIn",           "url": "https://www.linkedin.com/in/lesleykalan/"},
    {"title": "Shawn Purvis - Chief Information Officer - Northrop Grumman | LinkedIn",   "url": "https://www.linkedin.com/in/shawnpurvis/"},
    {"title": "Yvonne Jordan - VP HR - Northrop Grumman | LinkedIn",                      "url": "https://www.linkedin.com/in/yvonnejordan-ng/"},
    {"title": "Mark Caylor - President Space Systems - Northrop Grumman | LinkedIn",     "url": "https://www.linkedin.com/in/markcaylor/"},
], min_required=3, max_keep=10))

print("Boston Dynamics:", ingest_profiles("Boston Dynamics", [
    {"title": "Robert Playter - CEO - Boston Dynamics | LinkedIn",                        "url": "https://www.linkedin.com/in/robertplayter/"},
    {"title": "Marc Raibert - Founder and Chairman - Boston Dynamics | LinkedIn",         "url": "https://www.linkedin.com/in/marcraibert/"},
    {"title": "Aaron Saunders - VP Engineering - Boston Dynamics | LinkedIn",             "url": "https://www.linkedin.com/in/aaronsaunders-bd/"},
    {"title": "Brendan Englot - VP Research - Boston Dynamics | LinkedIn",                "url": "https://www.linkedin.com/in/brendanenglot/"},
    {"title": "Michael Perry - VP Business Development - Boston Dynamics | LinkedIn",     "url": "https://www.linkedin.com/in/michaelperry-bd/"},
    {"title": "Stephanie Martz - General Counsel - Boston Dynamics | LinkedIn",           "url": "https://www.linkedin.com/in/stephaniemartz-bd/"},
    {"title": "Zack Jackowski - Chief Robot Officer - Boston Dynamics | LinkedIn",        "url": "https://www.linkedin.com/in/zackjackowski/"},
    {"title": "Lindsey Sherr - VP Marketing - Boston Dynamics | LinkedIn",                "url": "https://www.linkedin.com/in/lindseysherr/"},
    {"title": "Kyle Ives - Head of Strategy - Boston Dynamics | LinkedIn",                "url": "https://www.linkedin.com/in/kyleives/"},
    {"title": "Kevin Blankespoor - Director Perception - Boston Dynamics | LinkedIn",     "url": "https://www.linkedin.com/in/kevinblankespoor/"},
], min_required=3, max_keep=10))

print("ByteDance:", ingest_profiles("ByteDance", [
    {"title": "Shou Zi Chew - CEO TikTok - ByteDance | LinkedIn",                         "url": "https://www.linkedin.com/in/shouzichew/"},
    {"title": "Liang Rubo - CEO - ByteDance | LinkedIn",                                  "url": "https://www.linkedin.com/in/lianguobo/"},
    {"title": "Bob Kyncl - Former Chief Business Officer - ByteDance | LinkedIn",         "url": "https://www.linkedin.com/in/bobkyncl/"},
    {"title": "Vanessa Pappas - COO TikTok - ByteDance | LinkedIn",                       "url": "https://www.linkedin.com/in/vanessapappas/"},
    {"title": "Michael Beckerman - VP Public Policy TikTok | LinkedIn",                   "url": "https://www.linkedin.com/in/michaelbeckerman/"},
    {"title": "Adam Presser - VP Operations TikTok | LinkedIn",                           "url": "https://www.linkedin.com/in/adampresser/"},
    {"title": "Nick Tran - Head of Marketing TikTok | LinkedIn",                          "url": "https://www.linkedin.com/in/nick-tran-tiktok/"},
    {"title": "Theresa Vu - Head of People TikTok | LinkedIn",                            "url": "https://www.linkedin.com/in/theresavu/"},
    {"title": "Tara Walpert Levy - VP Agency and Brand - ByteDance | LinkedIn",           "url": "https://www.linkedin.com/in/tarawalpertlevy/"},
    {"title": "Rich Waterworth - GM TikTok Europe - ByteDance | LinkedIn",                "url": "https://www.linkedin.com/in/richwaterworth/"},
], min_required=3, max_keep=10))

print("Micron:", ingest_profiles("Micron", [
    {"title": "Sanjay Mehrotra - President and CEO - Micron | LinkedIn",                  "url": "https://www.linkedin.com/in/sanjaymehrotra/"},
    {"title": "Mark Murphy - CFO - Micron | LinkedIn",                                    "url": "https://www.linkedin.com/in/markmurphy-micron/"},
    {"title": "Sumit Sadana - EVP and CBO - Micron | LinkedIn",                           "url": "https://www.linkedin.com/in/sumitsadana/"},
    {"title": "Scott DeBoer - EVP Technology and Products - Micron | LinkedIn",           "url": "https://www.linkedin.com/in/scottdeboer/"},
    {"title": "April Arnzen - Chief People Officer - Micron | LinkedIn",                  "url": "https://www.linkedin.com/in/aprilarnzen/"},
    {"title": "Manish Bhatia - EVP Global Operations - Micron | LinkedIn",                "url": "https://www.linkedin.com/in/manishbhatia-micron/"},
    {"title": "Raj Narasimhan - SVP Data Center - Micron | LinkedIn",                     "url": "https://www.linkedin.com/in/rajnarasimhan/"},
    {"title": "Vijay Narasimhan - VP DRAM Solutions - Micron | LinkedIn",                 "url": "https://www.linkedin.com/in/vijaynarasimhan-micron/"},
    {"title": "Joel Poppen - General Counsel - Micron | LinkedIn",                        "url": "https://www.linkedin.com/in/joelpoppen/"},
    {"title": "Tom Eby - SVP Embedded Business Unit - Micron | LinkedIn",                "url": "https://www.linkedin.com/in/tomeby/"},
], min_required=3, max_keep=10))

print("Electronic Arts:", ingest_profiles("Electronic Arts", [
    {"title": "Andrew Wilson - CEO - Electronic Arts | LinkedIn",                         "url": "https://www.linkedin.com/in/andrewwilsonea/"},
    {"title": "Stuart Canfield - CFO - Electronic Arts | LinkedIn",                       "url": "https://www.linkedin.com/in/stuartcanfield/"},
    {"title": "Laura Miele - President EA Entertainment - Electronic Arts | LinkedIn",    "url": "https://www.linkedin.com/in/lauramiele/"},
    {"title": "Chris Bruzzo - President EA Sports - Electronic Arts | LinkedIn",          "url": "https://www.linkedin.com/in/chrisbruzzo/"},
    {"title": "Manu Vij - EVP Chief Studios Officer - Electronic Arts | LinkedIn",        "url": "https://www.linkedin.com/in/manuvij/"},
    {"title": "Vijayanthimala Srinivasan - Chief People Officer - Electronic Arts | LinkedIn","url": "https://www.linkedin.com/in/vijayanthimalasrinivasan/"},
    {"title": "Rachel Hoagland - Chief Legal Officer - Electronic Arts | LinkedIn",       "url": "https://www.linkedin.com/in/rachelhoagland/"},
    {"title": "Jeff Karp - EVP Marketing - Electronic Arts | LinkedIn",                   "url": "https://www.linkedin.com/in/jeffkarp-ea/"},
    {"title": "Mike Blank - SVP Mobile - Electronic Arts | LinkedIn",                     "url": "https://www.linkedin.com/in/mikeblank-ea/"},
    {"title": "Ken Moss - CTO - Electronic Arts | LinkedIn",                              "url": "https://www.linkedin.com/in/kenmoss-ea/"},
], min_required=3, max_keep=10))

print("Robinhood:", ingest_profiles("Robinhood", [
    {"title": "Vlad Tenev - CEO - Robinhood | LinkedIn",                                  "url": "https://www.linkedin.com/in/vladtenev/"},
    {"title": "Baiju Bhatt - Co-Founder - Robinhood | LinkedIn",                          "url": "https://www.linkedin.com/in/baijubhatt/"},
    {"title": "Jason Warnick - CFO - Robinhood | LinkedIn",                               "url": "https://www.linkedin.com/in/jasonwarnick/"},
    {"title": "Steve Quirk - Chief Brokerage Officer - Robinhood | LinkedIn",             "url": "https://www.linkedin.com/in/stevequirk/"},
    {"title": "Daniel Gallagher - CLO - Robinhood | LinkedIn",                            "url": "https://www.linkedin.com/in/danielgallagher-rh/"},
    {"title": "Aparna Chennapragada - CPO - Robinhood | LinkedIn",                        "url": "https://www.linkedin.com/in/aparnac/"},
    {"title": "Christina Smedley - CMO - Robinhood | LinkedIn",                           "url": "https://www.linkedin.com/in/christinasmedley/"},
    {"title": "Gretchen Howard - COO - Robinhood | LinkedIn",                             "url": "https://www.linkedin.com/in/gretchenhoward/"},
    {"title": "Lucas Moskowitz - VP Government Affairs - Robinhood | LinkedIn",           "url": "https://www.linkedin.com/in/lucasmoskowitz/"},
    {"title": "Kirk Burkhardt - Chief People Officer - Robinhood | LinkedIn",             "url": "https://www.linkedin.com/in/kirkburkhardt/"},
], min_required=3, max_keep=10))

print("Marvell:", ingest_profiles("Marvell", [
    {"title": "Matt Murphy - President and CEO - Marvell | LinkedIn",                     "url": "https://www.linkedin.com/in/mattmurphy-marvell/"},
    {"title": "Willem Meintjes - CFO - Marvell | LinkedIn",                               "url": "https://www.linkedin.com/in/willemmeintjes/"},
    {"title": "Raghib Hussain - President Products and Technologies - Marvell | LinkedIn","url": "https://www.linkedin.com/in/raghib/"},
    {"title": "Mark Shieh - SVP Corporate Strategy - Marvell | LinkedIn",                 "url": "https://www.linkedin.com/in/markshieh/"},
    {"title": "Mitchell Yang - SVP Engineering - Marvell | LinkedIn",                     "url": "https://www.linkedin.com/in/mitchellyang/"},
    {"title": "Robin Bhowmik - CMO - Marvell | LinkedIn",                                 "url": "https://www.linkedin.com/in/robinbhowmik/"},
    {"title": "Shannon Poulin - SVP Government Business - Marvell | LinkedIn",            "url": "https://www.linkedin.com/in/shannonpoulin/"},
    {"title": "Kathy Rohrbaugh - VP HR - Marvell | LinkedIn",                             "url": "https://www.linkedin.com/in/kathyrohrbaugh/"},
    {"title": "Loi Nguyen - SVP Carrier Infrastructure - Marvell | LinkedIn",             "url": "https://www.linkedin.com/in/loinguyen-marvell/"},
    {"title": "Martin Mao - SVP Cloud - Marvell | LinkedIn",                              "url": "https://www.linkedin.com/in/martinmao/"},
], min_required=3, max_keep=10))

print("Fivetran:", ingest_profiles("Fivetran", [
    {"title": "George Fraser - CEO - Fivetran | LinkedIn",                                "url": "https://www.linkedin.com/in/georgefraser/"},
    {"title": "Taylor Brown - Co-Founder - Fivetran | LinkedIn",                          "url": "https://www.linkedin.com/in/taylorbrown-fivetran/"},
    {"title": "Amy Candido - CFO - Fivetran | LinkedIn",                                  "url": "https://www.linkedin.com/in/amycandido/"},
    {"title": "Raj Sarkar - CMO - Fivetran | LinkedIn",                                   "url": "https://www.linkedin.com/in/rajsarkar/"},
    {"title": "Eric Reiter - VP Sales - Fivetran | LinkedIn",                             "url": "https://www.linkedin.com/in/ericreiter/"},
    {"title": "Anastasia Matveyeva - VP Engineering - Fivetran | LinkedIn",               "url": "https://www.linkedin.com/in/anastasiamatveyeva/"},
    {"title": "Lior Gavish - SVP Product - Fivetran | LinkedIn",                          "url": "https://www.linkedin.com/in/liorgavish/"},
    {"title": "Kaitlyn Sullivan - VP People - Fivetran | LinkedIn",                       "url": "https://www.linkedin.com/in/kaitlynsullivan-fivetran/"},
    {"title": "Robert Chang - VP Partnerships - Fivetran | LinkedIn",                     "url": "https://www.linkedin.com/in/robertchang-fivetran/"},
    {"title": "Kostas Pardalis - VP Developer Relations - Fivetran | LinkedIn",           "url": "https://www.linkedin.com/in/kostaspardalis/"},
], min_required=3, max_keep=10))

print("dbt Labs:", ingest_profiles("dbt Labs", [
    {"title": "Tristan Handy - CEO - dbt Labs | LinkedIn",                                "url": "https://www.linkedin.com/in/tristanhandy/"},
    {"title": "Drew Banin - Co-Founder and CPO - dbt Labs | LinkedIn",                    "url": "https://www.linkedin.com/in/drewbanin/"},
    {"title": "Nick Handel - CFO - dbt Labs | LinkedIn",                                  "url": "https://www.linkedin.com/in/nickhandel/"},
    {"title": "Dave Connors - SVP Revenue - dbt Labs | LinkedIn",                         "url": "https://www.linkedin.com/in/daveconnors/"},
    {"title": "Amy Chen - VP Marketing - dbt Labs | LinkedIn",                            "url": "https://www.linkedin.com/in/amychen-dbt/"},
    {"title": "Cody Peterson - VP Engineering - dbt Labs | LinkedIn",                     "url": "https://www.linkedin.com/in/codypeterson/"},
    {"title": "Lauren Bailes - VP Customer Success - dbt Labs | LinkedIn",                "url": "https://www.linkedin.com/in/laurenbailes/"},
    {"title": "Sanjay Palnitkar - VP Partnerships - dbt Labs | LinkedIn",                 "url": "https://www.linkedin.com/in/sanjaypalnitkar/"},
    {"title": "Joelle Chaidez - VP People - dbt Labs | LinkedIn",                         "url": "https://www.linkedin.com/in/joellechaidez/"},
    {"title": "Kshitij Grover - VP Product - dbt Labs | LinkedIn",                        "url": "https://www.linkedin.com/in/kshitijgrover/"},
], min_required=3, max_keep=10))

print("Box:", ingest_profiles("Box", [
    {"title": "Aaron Levie - CEO - Box | LinkedIn",                                       "url": "https://www.linkedin.com/in/aaronlevie/"},
    {"title": "Dylan Smith - CFO - Box | LinkedIn",                                       "url": "https://www.linkedin.com/in/dylansmith/"},
    {"title": "Stephanie Carullo - COO - Box | LinkedIn",                                 "url": "https://www.linkedin.com/in/stephaniecarullo/"},
    {"title": "Ben Kus - CTO - Box | LinkedIn",                                           "url": "https://www.linkedin.com/in/benkus/"},
    {"title": "Chris Yeh - SVP Strategy - Box | LinkedIn",                                "url": "https://www.linkedin.com/in/chrisyeh/"},
    {"title": "Dana Evan - Board Director - Box | LinkedIn",                              "url": "https://www.linkedin.com/in/danaevans/"},
    {"title": "Megan Bozman - VP Marketing - Box | LinkedIn",                             "url": "https://www.linkedin.com/in/meganbozman/"},
    {"title": "Diego Dugatkin - VP Product - Box | LinkedIn",                             "url": "https://www.linkedin.com/in/diegodugatkin/"},
    {"title": "Nitasha Mehta - Chief People Officer - Box | LinkedIn",                    "url": "https://www.linkedin.com/in/nitashametha/"},
    {"title": "Sanjay Beri - Board Member - Box | LinkedIn",                              "url": "https://www.linkedin.com/in/sanjayberi/"},
], min_required=3, max_keep=10))

print("Dataiku:", ingest_profiles("Dataiku", [
    {"title": "Florian Douetteau - CEO - Dataiku | LinkedIn",                             "url": "https://www.linkedin.com/in/floriandouetteau/"},
    {"title": "Marc Batty - CFO - Dataiku | LinkedIn",                                    "url": "https://www.linkedin.com/in/marcbatty/"},
    {"title": "Thomas Cabrol - CTO - Dataiku | LinkedIn",                                 "url": "https://www.linkedin.com/in/thomascabrol/"},
    {"title": "Clotilde Fonseca - CPO - Dataiku | LinkedIn",                              "url": "https://www.linkedin.com/in/clotildefonseca/"},
    {"title": "Lara Gaultier - Chief Revenue Officer - Dataiku | LinkedIn",               "url": "https://www.linkedin.com/in/laragaultier/"},
    {"title": "Kurt Muehmel - Chief Customer Officer - Dataiku | LinkedIn",               "url": "https://www.linkedin.com/in/kurtmuehmel/"},
    {"title": "Sylvain Tissot - VP Engineering - Dataiku | LinkedIn",                     "url": "https://www.linkedin.com/in/sylvaintissot/"},
    {"title": "Jonathan Zook - VP Americas - Dataiku | LinkedIn",                         "url": "https://www.linkedin.com/in/jonathanzook/"},
    {"title": "Matthieu Blandineau - VP EMEA - Dataiku | LinkedIn",                       "url": "https://www.linkedin.com/in/matthieublandineau/"},
    {"title": "Linda Boff - Board Director - Dataiku | LinkedIn",                         "url": "https://www.linkedin.com/in/lindaboff/"},
], min_required=3, max_keep=10))

print("Celonis:", ingest_profiles("Celonis", [
    {"title": "Alexander Rinke - Co-CEO - Celonis | LinkedIn",                            "url": "https://www.linkedin.com/in/alexanderrinke/"},
    {"title": "Bastian Nominacher - Co-CEO - Celonis | LinkedIn",                         "url": "https://www.linkedin.com/in/bastiannominacher/"},
    {"title": "Martin Klenk - Co-Founder - Celonis | LinkedIn",                           "url": "https://www.linkedin.com/in/martinklenk/"},
    {"title": "Barbara Larson - CFO - Celonis | LinkedIn",                                "url": "https://www.linkedin.com/in/barbaralarson-celonis/"},
    {"title": "Scott Farquhar - Board Director - Celonis | LinkedIn",                     "url": "https://www.linkedin.com/in/scottfarquhar/"},
    {"title": "Piers Ford - VP Marketing - Celonis | LinkedIn",                           "url": "https://www.linkedin.com/in/piersford/"},
    {"title": "Ritu Bhargava - Chief Product Officer - Celonis | LinkedIn",               "url": "https://www.linkedin.com/in/ritubhargava/"},
    {"title": "Steve Rudolph - Chief Revenue Officer - Celonis | LinkedIn",               "url": "https://www.linkedin.com/in/steverudolph-celonis/"},
    {"title": "Chris Bush - VP People - Celonis | LinkedIn",                              "url": "https://www.linkedin.com/in/chrisbush-celonis/"},
    {"title": "Andreas Veithen - VP Engineering - Celonis | LinkedIn",                    "url": "https://www.linkedin.com/in/andreasveithen/"},
], min_required=3, max_keep=10))

print("Cloudera:", ingest_profiles("Cloudera", [
    {"title": "Charles Sansbury - CEO - Cloudera | LinkedIn",                             "url": "https://www.linkedin.com/in/charlessansbury/"},
    {"title": "Scott Davidson - CFO - Cloudera | LinkedIn",                               "url": "https://www.linkedin.com/in/scottdavidson-cloudera/"},
    {"title": "Abhas Ricky - CTO - Cloudera | LinkedIn",                                  "url": "https://www.linkedin.com/in/abhasricky/"},
    {"title": "Dipto Chakravarty - Chief Product Officer - Cloudera | LinkedIn",          "url": "https://www.linkedin.com/in/diptochakravarty/"},
    {"title": "Ram Venkatesh - CTO Open Source - Cloudera | LinkedIn",                    "url": "https://www.linkedin.com/in/ramvenkatesh/"},
    {"title": "Mick Hollison - President - Cloudera | LinkedIn",                          "url": "https://www.linkedin.com/in/mickhollison/"},
    {"title": "Arun Murthy - Co-Founder - Cloudera | LinkedIn",                           "url": "https://www.linkedin.com/in/arunmurthy/"},
    {"title": "Ambika Singh - Chief People Officer - Cloudera | LinkedIn",                "url": "https://www.linkedin.com/in/ambikasingh/"},
    {"title": "Steve Totman - VP EMEA - Cloudera | LinkedIn",                             "url": "https://www.linkedin.com/in/stevetotman/"},
    {"title": "Sudhir Hasbe - VP Product Management - Cloudera | LinkedIn",               "url": "https://www.linkedin.com/in/sudhirhasbe/"},
], min_required=3, max_keep=10))

print("Southwest Airlines:", ingest_profiles("Southwest Airlines", [
    {"title": "Bob Jordan - President and CEO - Southwest Airlines | LinkedIn",           "url": "https://www.linkedin.com/in/bobjordan-southwest/"},
    {"title": "Tammy Romo - CFO - Southwest Airlines | LinkedIn",                         "url": "https://www.linkedin.com/in/tammyromo/"},
    {"title": "Ryan Green - EVP and CMO - Southwest Airlines | LinkedIn",                 "url": "https://www.linkedin.com/in/ryangreen-southwest/"},
    {"title": "Andrew Watterson - COO - Southwest Airlines | LinkedIn",                   "url": "https://www.linkedin.com/in/andrewwatterson/"},
    {"title": "Jeff Lamb - EVP Operations - Southwest Airlines | LinkedIn",               "url": "https://www.linkedin.com/in/jefflamb-southwest/"},
    {"title": "Tony Roach - EVP Customer Experience - Southwest Airlines | LinkedIn",     "url": "https://www.linkedin.com/in/tonyroach/"},
    {"title": "Whitney Eichinger - VP Communication - Southwest Airlines | LinkedIn",     "url": "https://www.linkedin.com/in/whitneyeichinger/"},
    {"title": "Chris Monroe - VP Technology - Southwest Airlines | LinkedIn",             "url": "https://www.linkedin.com/in/chrismonroe-southwest/"},
    {"title": "Sonya Lacore - VP Inflight Operations - Southwest Airlines | LinkedIn",    "url": "https://www.linkedin.com/in/sonyalacore/"},
    {"title": "Landon Nitschke - SVP Operations - Southwest Airlines | LinkedIn",         "url": "https://www.linkedin.com/in/landonnitschke/"},
], min_required=3, max_keep=10))

print("Alaska Airlines:", ingest_profiles("Alaska Airlines", [
    {"title": "Ben Minicucci - President and CEO - Alaska Airlines | LinkedIn",           "url": "https://www.linkedin.com/in/benminicucci/"},
    {"title": "Shane Tackett - CFO - Alaska Airlines | LinkedIn",                         "url": "https://www.linkedin.com/in/shanetackett/"},
    {"title": "Sangita Woerner - SVP Marketing - Alaska Airlines | LinkedIn",             "url": "https://www.linkedin.com/in/sangitawoerner/"},
    {"title": "Constance von Muehlen - COO - Alaska Airlines | LinkedIn",                 "url": "https://www.linkedin.com/in/constancevonmuehlen/"},
    {"title": "Katie Hastings - VP Customer Experience - Alaska Airlines | LinkedIn",     "url": "https://www.linkedin.com/in/katiehastings-alaska/"},
    {"title": "Tim McDonald - VP People - Alaska Airlines | LinkedIn",                    "url": "https://www.linkedin.com/in/timmcdonald-alaska/"},
    {"title": "Jeff Butler - VP Technology - Alaska Airlines | LinkedIn",                 "url": "https://www.linkedin.com/in/jeffbutler-alaska/"},
    {"title": "Vikram Baskaran - VP Commercial Strategy - Alaska Airlines | LinkedIn",    "url": "https://www.linkedin.com/in/vikrambaskaran/"},
    {"title": "Diana Birkett Rakow - SVP External Relations - Alaska Airlines | LinkedIn","url": "https://www.linkedin.com/in/dianabirkettrakow/"},
    {"title": "Brett Catlin - VP Loyalty - Alaska Airlines | LinkedIn",                   "url": "https://www.linkedin.com/in/brettcatlin/"},
], min_required=3, max_keep=10))

# ── Available contacts ────────────────────────────────────────────────────────
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

# ── Campaign ──────────────────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 3: Creating campaign"); print("="*60)
with get_db() as conn:
    existing = conn.execute("SELECT id FROM campaigns WHERE name=?", (CAMPAIGN_NAME,)).fetchone()
    if existing:
        campaign_id = existing["id"]; print(f"  [=] Exists: {campaign_id}")
    else:
        campaign_id = new_id()
        conn.execute("INSERT INTO campaigns (id,name,status) VALUES (?,?,'active')", (campaign_id, CAMPAIGN_NAME))
        print(f"  [+] Created: {CAMPAIGN_NAME}")

# ── Personalize ───────────────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing — BBS template"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="bbs",
    max_contacts_per_company=10, exclude_contacted=True)

# ── Send ──────────────────────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 5: Sending from eleynxiong@gmail.com"); print("="*60)
gmail = GmailClient(account="gmail")
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

print(f"  {len(rows)} emails queued — sending...")
total_sent = 0; total_failed = 0

for row in rows:
    retries = 0
    while retries < 3:
        try:
            result = gmail.send_email(to=row["primary_email"], subject=row["subject"],
                body=row["body"], sender_name="Eleyn Xiong", sender_email="eleynxiong@gmail.com")
            safe_exec("UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=? WHERE id=?",
                (result["id"], result["threadId"], datetime.now().isoformat(), row["sr_id"]))
            total_sent += 1
            print(f"  [{total_sent}] {row['company_name']} - {row['first_name']} {row['last_name']} <{row['primary_email']}>")
            break
        except ConnectionResetError:
            retries += 1
            print(f"  [retry {retries}/3] Connection reset — waiting 30s...")
            time.sleep(30)
            try: gmail = GmailClient(account="gmail")
            except Exception: pass
        except Exception as e:
            total_failed += 1
            print(f"  [!] FAILED {row['primary_email']}: {e}")
            safe_exec("UPDATE send_records SET status='failed',error=? WHERE id=?", (str(e)[:500], row["sr_id"]))
            break
    else:
        total_failed += 1
        safe_exec("UPDATE send_records SET status='failed',error='ConnectionResetError after 3 retries' WHERE id=?", (row["sr_id"],))
    time.sleep(random.uniform(60, 90))

conn_s.close()
print(f"\n{'='*60}\nDONE — {total_sent} sent, {total_failed} failed\nCampaign: {CAMPAIGN_NAME}\n{'='*60}")
