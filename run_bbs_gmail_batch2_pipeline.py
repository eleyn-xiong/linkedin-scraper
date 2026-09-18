"""
BBS Gmail Batch 2 — Berkeley Business Society template, sent from eleynxiong@gmail.com.
15 companies not previously in any BBS campaign.
exclude_contacted=True ensures zero overlap with any prior campaign.
"""
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
    {"name": "Tesla",          "domain": "tesla.com",          "industry": "Electric Vehicles / Energy / AI",        "email_pattern": "first.last"},
    {"name": "AMD",            "domain": "amd.com",            "industry": "Semiconductors / CPUs / GPUs",           "email_pattern": "first.last"},
    {"name": "Broadcom",       "domain": "broadcom.com",       "industry": "Semiconductors / Networking / Software",  "email_pattern": "first.last"},
    {"name": "SAP",            "domain": "sap.com",            "industry": "Enterprise Software / ERP / Cloud",       "email_pattern": "first.last"},
    {"name": "Marriott",       "domain": "marriott.com",       "industry": "Hospitality / Hotels / Travel",           "email_pattern": "first.last"},
    {"name": "Coinbase",       "domain": "coinbase.com",       "industry": "Crypto / Fintech / Web3",                 "email_pattern": "first.last"},
    {"name": "Qualcomm",       "domain": "qualcomm.com",       "industry": "Semiconductors / Wireless / Mobile",      "email_pattern": "first.last"},
    {"name": "Reddit",         "domain": "reddit.com",         "industry": "Social Media / Community Platform",       "email_pattern": "first.last"},
    {"name": "Samsung",        "domain": "samsung.com",        "industry": "Consumer Electronics / Semiconductors",   "email_pattern": "first.last"},
    {"name": "CrowdStrike",    "domain": "crowdstrike.com",    "industry": "Cybersecurity / Endpoint Protection",     "email_pattern": "first.last"},
    {"name": "Datadog",        "domain": "datadoghq.com",      "industry": "Observability / Cloud Monitoring / SaaS", "email_pattern": "first.last"},
    {"name": "Confluent",      "domain": "confluent.io",       "industry": "Data Streaming / Kafka / Cloud",          "email_pattern": "first.last"},
    {"name": "Zscaler",        "domain": "zscaler.com",        "industry": "Cloud Security / Zero Trust",             "email_pattern": "first.last"},
    {"name": "Hugging Face",   "domain": "huggingface.co",     "industry": "AI / Open Source ML / Developer Tools",   "email_pattern": "first.last"},
    {"name": "Lam Research",   "domain": "lamresearch.com",    "industry": "Semiconductor Equipment / Wafer Fab",     "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Gmail Batch 2 - June 2026"
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
            conn.execute(
                "INSERT INTO companies (id,name,domain,industry,email_pattern,email_pattern_confidence) VALUES (?,?,?,?,?,?)",
                (new_id(), c["name"], c["domain"], c["industry"], c["email_pattern"], 70.0)
            )
            print(f"  [+] {c['name']}")
        except Exception as e:
            print(f"  [=] {c['name']} already exists" if "UNIQUE" in str(e).upper() else f"  [!] {e}")

print("\n" + "="*60); print("STEP 2: Ingesting fresh profiles"); print("="*60)

# Tesla
print("Tesla:", ingest_profiles("Tesla", [
    {"title": "Elon Musk - CEO - Tesla | LinkedIn",                                      "url": "https://www.linkedin.com/in/elonmusk/"},
    {"title": "Vaibhav Taneja - CFO - Tesla | LinkedIn",                                 "url": "https://www.linkedin.com/in/vaibhavtaneja/"},
    {"title": "Tom Zhu - SVP Automotive - Tesla | LinkedIn",                             "url": "https://www.linkedin.com/in/tomzhu-tesla/"},
    {"title": "Zachary Kirkhorn - Former CFO - Tesla | LinkedIn",                        "url": "https://www.linkedin.com/in/zacharykirkhorn/"},
    {"title": "Drew Baglino - SVP Powertrain and Energy - Tesla | LinkedIn",             "url": "https://www.linkedin.com/in/drewbaglino/"},
    {"title": "Rohan Patel - VP Public Policy - Tesla | LinkedIn",                       "url": "https://www.linkedin.com/in/rohanpatel-tesla/"},
    {"title": "Grace Tao - VP Communications - Tesla | LinkedIn",                        "url": "https://www.linkedin.com/in/gracetao/"},
    {"title": "Omead Afshar - VP Operations - Tesla | LinkedIn",                         "url": "https://www.linkedin.com/in/omeadafshar/"},
    {"title": "Felicia Mayo - Chief People Officer - Tesla | LinkedIn",                  "url": "https://www.linkedin.com/in/feliciamayo/"},
    {"title": "Lars Moravy - VP Vehicle Engineering - Tesla | LinkedIn",                 "url": "https://www.linkedin.com/in/larsmorаvy/"},
], min_required=3, max_keep=10))

# AMD
print("AMD:", ingest_profiles("AMD", [
    {"title": "Lisa Su - Chair and CEO - AMD | LinkedIn",                                "url": "https://www.linkedin.com/in/lisa-su/"},
    {"title": "Jean Hu - CFO - AMD | LinkedIn",                                          "url": "https://www.linkedin.com/in/jean-hu-amd/"},
    {"title": "Victor Peng - President - AMD | LinkedIn",                                "url": "https://www.linkedin.com/in/victorpeng/"},
    {"title": "Forrest Norrod - EVP Data Center and Embedded - AMD | LinkedIn",          "url": "https://www.linkedin.com/in/forreststn/"},
    {"title": "Mark Papermaster - CTO - AMD | LinkedIn",                                 "url": "https://www.linkedin.com/in/markpapermaster/"},
    {"title": "Darla Smith - Chief People Officer - AMD | LinkedIn",                     "url": "https://www.linkedin.com/in/darlasmith-amd/"},
    {"title": "Alyssa Simpson Rochwerger - VP AI - AMD | LinkedIn",                      "url": "https://www.linkedin.com/in/alyssasimpsonrochwerger/"},
    {"title": "David McAfee - VP Client Channel Sales - AMD | LinkedIn",                 "url": "https://www.linkedin.com/in/davidmcafee-amd/"},
    {"title": "Sandeep Dattathreya - VP Marketing - AMD | LinkedIn",                    "url": "https://www.linkedin.com/in/sandeepdattathreya/"},
    {"title": "Vamsi Boppana - SVP AI - AMD | LinkedIn",                                 "url": "https://www.linkedin.com/in/vamsiboppana/"},
], min_required=3, max_keep=10))

# Broadcom
print("Broadcom:", ingest_profiles("Broadcom", [
    {"title": "Hock Tan - President and CEO - Broadcom | LinkedIn",                      "url": "https://www.linkedin.com/in/hocktan/"},
    {"title": "Kirsten Spears - CFO - Broadcom | LinkedIn",                              "url": "https://www.linkedin.com/in/kirstenspears/"},
    {"title": "Tom Krause - President Software - Broadcom | LinkedIn",                   "url": "https://www.linkedin.com/in/tomkrause-broadcom/"},
    {"title": "Charlie Kawwas - President Semiconductor Solutions - Broadcom | LinkedIn","url": "https://www.linkedin.com/in/charliekawwas/"},
    {"title": "Mark Davidson - VP Operations - Broadcom | LinkedIn",                     "url": "https://www.linkedin.com/in/markdavidson-broadcom/"},
    {"title": "Andy Nallappan - CTO - Broadcom Software | LinkedIn",                     "url": "https://www.linkedin.com/in/andynallappan/"},
    {"title": "Jas Sood - Chief People Officer - Broadcom | LinkedIn",                   "url": "https://www.linkedin.com/in/jassood/"},
    {"title": "Ji-Yoon Kim - VP Strategy - Broadcom | LinkedIn",                         "url": "https://www.linkedin.com/in/jiyoonkim/"},
    {"title": "Dan Carpenter - VP Marketing - Broadcom | LinkedIn",                      "url": "https://www.linkedin.com/in/dancarpenter-broadcom/"},
    {"title": "Roland Matthys - SVP Engineering - Broadcom | LinkedIn",                  "url": "https://www.linkedin.com/in/rolandmatthys/"},
], min_required=3, max_keep=10))

# SAP
print("SAP:", ingest_profiles("SAP", [
    {"title": "Christian Klein - CEO - SAP | LinkedIn",                                  "url": "https://www.linkedin.com/in/christianklein/"},
    {"title": "Dominik Asam - CFO - SAP | LinkedIn",                                     "url": "https://www.linkedin.com/in/dominikasam/"},
    {"title": "Thomas Saueressig - President Product Engineering - SAP | LinkedIn",      "url": "https://www.linkedin.com/in/thomassaueressig/"},
    {"title": "Sabine Bendiek - Chief People Officer - SAP | LinkedIn",                  "url": "https://www.linkedin.com/in/sabinebendiek/"},
    {"title": "Scott Russell - President Customer Success - SAP | LinkedIn",             "url": "https://www.linkedin.com/in/scottrussell-sap/"},
    {"title": "Muhammad Alam - President Industries and CX - SAP | LinkedIn",            "url": "https://www.linkedin.com/in/muhammadalam-sap/"},
    {"title": "Julia White - Chief Marketing and Solutions Officer - SAP | LinkedIn",    "url": "https://www.linkedin.com/in/juliawhite/"},
    {"title": "Adaire Fox-Martin - President EMEA - SAP | LinkedIn",                    "url": "https://www.linkedin.com/in/adairefoxmartin/"},
    {"title": "Naz Stoelinga - General Counsel - SAP | LinkedIn",                        "url": "https://www.linkedin.com/in/nazstoelinga/"},
    {"title": "Juergen Mueller - CTO - SAP | LinkedIn",                                  "url": "https://www.linkedin.com/in/juergenmueller-sap/"},
], min_required=3, max_keep=10))

# Marriott
print("Marriott:", ingest_profiles("Marriott", [
    {"title": "Anthony Capuano - President and CEO - Marriott | LinkedIn",               "url": "https://www.linkedin.com/in/anthony-capuano/"},
    {"title": "Leeny Oberg - CFO - Marriott | LinkedIn",                                 "url": "https://www.linkedin.com/in/leenyoberg/"},
    {"title": "Stephanie Linnartz - Former President - Marriott | LinkedIn",             "url": "https://www.linkedin.com/in/stephanielinnartz/"},
    {"title": "Drew Pinto - EVP Global Operations - Marriott | LinkedIn",                "url": "https://www.linkedin.com/in/drewpinto/"},
    {"title": "David Rodriguez - EVP Chief HR Officer - Marriott | LinkedIn",            "url": "https://www.linkedin.com/in/davidrodriguez-marriott/"},
    {"title": "Karin Timpone - Global Chief Marketing Officer - Marriott | LinkedIn",    "url": "https://www.linkedin.com/in/karintimpone/"},
    {"title": "Craig Smith - EVP International - Marriott | LinkedIn",                   "url": "https://www.linkedin.com/in/craigsmith-marriott/"},
    {"title": "Julius Robinson - Chief Sales and Marketing Officer - Marriott | LinkedIn","url": "https://www.linkedin.com/in/juliusrobinson/"},
    {"title": "Carlton Ervin - EVP Lodging Development Americas - Marriott | LinkedIn",  "url": "https://www.linkedin.com/in/carltonervin/"},
    {"title": "Tina Edmundson - Chief Brand Officer - Marriott | LinkedIn",              "url": "https://www.linkedin.com/in/tinaedmundson/"},
], min_required=3, max_keep=10))

# Coinbase
print("Coinbase:", ingest_profiles("Coinbase", [
    {"title": "Brian Armstrong - CEO - Coinbase | LinkedIn",                             "url": "https://www.linkedin.com/in/barmstrong/"},
    {"title": "Alesia Haas - CFO - Coinbase | LinkedIn",                                 "url": "https://www.linkedin.com/in/alesiahaas/"},
    {"title": "Emilie Choi - President and COO - Coinbase | LinkedIn",                   "url": "https://www.linkedin.com/in/emiliechoi/"},
    {"title": "L.J. Brock - Chief People Officer - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/ljbrock/"},
    {"title": "Paul Grewal - Chief Legal Officer - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/paulgrewal/"},
    {"title": "Surojit Chatterjee - Chief Product Officer - Coinbase | LinkedIn",        "url": "https://www.linkedin.com/in/surojitchatterjee/"},
    {"title": "Nana Murugesan - VP International - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/nanamurugesan/"},
    {"title": "Tom Duff Gordon - VP Commercial - Coinbase | LinkedIn",                   "url": "https://www.linkedin.com/in/tomduffgordon/"},
    {"title": "Max Branzburg - VP Product Consumer - Coinbase | LinkedIn",               "url": "https://www.linkedin.com/in/maxbranzburg/"},
    {"title": "Jeff Haul - VP Engineering - Coinbase | LinkedIn",                        "url": "https://www.linkedin.com/in/jeffhaul/"},
], min_required=3, max_keep=10))

# Qualcomm
print("Qualcomm:", ingest_profiles("Qualcomm", [
    {"title": "Cristiano Amon - President and CEO - Qualcomm | LinkedIn",                "url": "https://www.linkedin.com/in/cristiano-amon/"},
    {"title": "Akash Palkhiwala - CFO - Qualcomm | LinkedIn",                            "url": "https://www.linkedin.com/in/akashpalkhiwala/"},
    {"title": "Alex Katouzian - SVP Mobile - Qualcomm | LinkedIn",                       "url": "https://www.linkedin.com/in/alexkatouzian/"},
    {"title": "Durga Malladi - SVP Engineering 5G - Qualcomm | LinkedIn",                "url": "https://www.linkedin.com/in/durgamalladi/"},
    {"title": "Don McGuire - Chief Marketing Officer - Qualcomm | LinkedIn",             "url": "https://www.linkedin.com/in/donmcguire-qualcomm/"},
    {"title": "Judy Brown - Chief People Officer - Qualcomm | LinkedIn",                 "url": "https://www.linkedin.com/in/judybrown-qualcomm/"},
    {"title": "Francisco Jeronimo - VP Strategy EMEA - Qualcomm | LinkedIn",            "url": "https://www.linkedin.com/in/franciscojeronimo/"},
    {"title": "Brian Modoff - VP Investor Relations - Qualcomm | LinkedIn",              "url": "https://www.linkedin.com/in/brianmodoff/"},
    {"title": "Raj Talluri - SVP Industrial IoT - Qualcomm | LinkedIn",                  "url": "https://www.linkedin.com/in/rajtalluri/"},
    {"title": "Nakul Duggal - SVP Automotive - Qualcomm | LinkedIn",                     "url": "https://www.linkedin.com/in/nakulduggal/"},
], min_required=3, max_keep=10))

# Reddit
print("Reddit:", ingest_profiles("Reddit", [
    {"title": "Steve Huffman - CEO - Reddit | LinkedIn",                                 "url": "https://www.linkedin.com/in/stevehuffman/"},
    {"title": "Drew Vollero - CFO - Reddit | LinkedIn",                                  "url": "https://www.linkedin.com/in/drewvollero/"},
    {"title": "Jen Wong - COO - Reddit | LinkedIn",                                      "url": "https://www.linkedin.com/in/jenwong-reddit/"},
    {"title": "Pali Bhat - CPO - Reddit | LinkedIn",                                     "url": "https://www.linkedin.com/in/palibhat/"},
    {"title": "Neil Clarke - CRO - Reddit | LinkedIn",                                   "url": "https://www.linkedin.com/in/neilclarke-reddit/"},
    {"title": "Roxy Young - CMO - Reddit | LinkedIn",                                    "url": "https://www.linkedin.com/in/roxyyoung/"},
    {"title": "Renee Guttmann - Chief Trust Officer - Reddit | LinkedIn",                "url": "https://www.linkedin.com/in/reneeguttmann/"},
    {"title": "Patrick Doyle - VP Engineering - Reddit | LinkedIn",                      "url": "https://www.linkedin.com/in/patrickdoyle-reddit/"},
    {"title": "Jessica Zartler - VP People - Reddit | LinkedIn",                         "url": "https://www.linkedin.com/in/jessicazartler/"},
    {"title": "Tariq Hassan - Chief Marketing Officer - Reddit | LinkedIn",              "url": "https://www.linkedin.com/in/tariqhassan/"},
], min_required=3, max_keep=10))

# Samsung
print("Samsung:", ingest_profiles("Samsung", [
    {"title": "TM Roh - President Mobile - Samsung Electronics | LinkedIn",              "url": "https://www.linkedin.com/in/tmroh/"},
    {"title": "Kyehyun Kyung - President Memory - Samsung Electronics | LinkedIn",       "url": "https://www.linkedin.com/in/kyehyunkyung/"},
    {"title": "KH Kim - Vice Chairman - Samsung Electronics | LinkedIn",                 "url": "https://www.linkedin.com/in/khkim-samsung/"},
    {"title": "Mike Lawrie - SVP Samsung Americas | LinkedIn",                           "url": "https://www.linkedin.com/in/mikelawrie-samsung/"},
    {"title": "Mark Holloway - VP Corporate Marketing Americas - Samsung | LinkedIn",    "url": "https://www.linkedin.com/in/markholloway-samsung/"},
    {"title": "Stephanie Choi - EVP Chief Marketing Officer - Samsung Mobile | LinkedIn","url": "https://www.linkedin.com/in/stephaniechoi-samsung/"},
    {"title": "Jon Gabay - VP Business Development Samsung Semiconductor | LinkedIn",    "url": "https://www.linkedin.com/in/jongabay/"},
    {"title": "Sangjoon Park - President Samsung Research America | LinkedIn",           "url": "https://www.linkedin.com/in/sangjoonpark/"},
    {"title": "Patrick Chomet - EVP Customer Experience - Samsung Mobile | LinkedIn",   "url": "https://www.linkedin.com/in/patrickchomet/"},
    {"title": "Yongin Park - VP Strategy - Samsung Electronics | LinkedIn",              "url": "https://www.linkedin.com/in/yonginpark/"},
], min_required=3, max_keep=10))

# CrowdStrike
print("CrowdStrike:", ingest_profiles("CrowdStrike", [
    {"title": "George Kurtz - CEO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/georgekurtz/"},
    {"title": "Burt Podbere - CFO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/burtpodbere/"},
    {"title": "Shawn Henry - President Field Operations - CrowdStrike | LinkedIn",       "url": "https://www.linkedin.com/in/shawnhenry/"},
    {"title": "Mike Sentonas - President - CrowdStrike | LinkedIn",                      "url": "https://www.linkedin.com/in/mikesentonas/"},
    {"title": "Elia Zaitsev - Chief Technology Officer - CrowdStrike | LinkedIn",        "url": "https://www.linkedin.com/in/eliazaitsev/"},
    {"title": "TJ Erickson - Chief People Officer - CrowdStrike | LinkedIn",             "url": "https://www.linkedin.com/in/tjerickson/"},
    {"title": "Raj Rajamani - CPO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/rajrajamani/"},
    {"title": "Drew Bagley - VP Privacy and Cyber Policy - CrowdStrike | LinkedIn",     "url": "https://www.linkedin.com/in/drewbagley/"},
    {"title": "Jenny Menna - VP Public Sector - CrowdStrike | LinkedIn",                 "url": "https://www.linkedin.com/in/jennymenna/"},
    {"title": "Daniel Bernard - Chief Business Officer - CrowdStrike | LinkedIn",        "url": "https://www.linkedin.com/in/danielbernard-crwd/"},
], min_required=3, max_keep=10))

# Datadog
print("Datadog:", ingest_profiles("Datadog", [
    {"title": "Olivier Pomel - CEO - Datadog | LinkedIn",                                "url": "https://www.linkedin.com/in/olivierpomel/"},
    {"title": "David Obstler - CFO - Datadog | LinkedIn",                                "url": "https://www.linkedin.com/in/davidobstler/"},
    {"title": "Alexis Le-Quoc - CTO - Datadog | LinkedIn",                               "url": "https://www.linkedin.com/in/alexislequoc/"},
    {"title": "Alex Rosemblat - VP Marketing - Datadog | LinkedIn",                      "url": "https://www.linkedin.com/in/alexrosemblat/"},
    {"title": "Dan Fougere - Chief Revenue Officer - Datadog | LinkedIn",                "url": "https://www.linkedin.com/in/danfougere/"},
    {"title": "Amanda Kleha - Chief Customer Officer - Datadog | LinkedIn",              "url": "https://www.linkedin.com/in/amandakleha/"},
    {"title": "Renaud Bouchard - VP Engineering - Datadog | LinkedIn",                   "url": "https://www.linkedin.com/in/renaudbouchard/"},
    {"title": "Jay Snyder - SVP Global Sales - Datadog | LinkedIn",                      "url": "https://www.linkedin.com/in/jaysnyder-datadog/"},
    {"title": "Ilan Rabinovitch - SVP Product - Datadog | LinkedIn",                     "url": "https://www.linkedin.com/in/irabinovitch/"},
    {"title": "Yrieix Garnier - VP People - Datadog | LinkedIn",                         "url": "https://www.linkedin.com/in/yrieixgarnier/"},
], min_required=3, max_keep=10))

# Confluent
print("Confluent:", ingest_profiles("Confluent", [
    {"title": "Jay Kreps - CEO - Confluent | LinkedIn",                                  "url": "https://www.linkedin.com/in/jaykreps/"},
    {"title": "Rohan Sivaram - CFO - Confluent | LinkedIn",                              "url": "https://www.linkedin.com/in/rohansivaram/"},
    {"title": "Erica Schultz - President Field Operations - Confluent | LinkedIn",       "url": "https://www.linkedin.com/in/ericaschultz/"},
    {"title": "Shayde Christian - Chief Data Officer - Confluent | LinkedIn",            "url": "https://www.linkedin.com/in/shaydechristian/"},
    {"title": "Greg Mefford - Chief Revenue Officer - Confluent | LinkedIn",             "url": "https://www.linkedin.com/in/gregmefford/"},
    {"title": "Hima Garimella - VP Engineering - Confluent | LinkedIn",                  "url": "https://www.linkedin.com/in/himagarimella/"},
    {"title": "Chad Verbowski - VP Product - Confluent | LinkedIn",                      "url": "https://www.linkedin.com/in/chadverbowski/"},
    {"title": "Will LaForest - VP Technology Strategy - Confluent | LinkedIn",           "url": "https://www.linkedin.com/in/willlaforest/"},
    {"title": "Krish Krishnan - VP Sales - Confluent | LinkedIn",                        "url": "https://www.linkedin.com/in/krishkrishnan-confluent/"},
    {"title": "Laura King - Chief People Officer - Confluent | LinkedIn",                "url": "https://www.linkedin.com/in/lauraking-confluent/"},
], min_required=3, max_keep=10))

# Zscaler
print("Zscaler:", ingest_profiles("Zscaler", [
    {"title": "Jay Chaudhry - CEO - Zscaler | LinkedIn",                                 "url": "https://www.linkedin.com/in/jaychaudhry/"},
    {"title": "Remo Canessa - CFO - Zscaler | LinkedIn",                                 "url": "https://www.linkedin.com/in/remocanessa/"},
    {"title": "Dali Kaafar - Chief Scientist - Zscaler | LinkedIn",                      "url": "https://www.linkedin.com/in/dalikaafar/"},
    {"title": "Howie Xu - VP AI and Machine Learning - Zscaler | LinkedIn",              "url": "https://www.linkedin.com/in/howiexu/"},
    {"title": "Stephen Kovac - VP Global Government - Zscaler | LinkedIn",               "url": "https://www.linkedin.com/in/stephenkovac/"},
    {"title": "Kavitha Mariappan - EVP Customer Experience - Zscaler | LinkedIn",        "url": "https://www.linkedin.com/in/kavithamariappan/"},
    {"title": "Karl Soderlund - SVP Partners - Zscaler | LinkedIn",                      "url": "https://www.linkedin.com/in/karlsoderlund/"},
    {"title": "Naresh Kumar - SVP Engineering - Zscaler | LinkedIn",                     "url": "https://www.linkedin.com/in/nareshkumar-zscaler/"},
    {"title": "Micheline Murphy - Chief People Officer - Zscaler | LinkedIn",            "url": "https://www.linkedin.com/in/michelinemurphy/"},
    {"title": "Dhawal Sharma - VP Product Management - Zscaler | LinkedIn",              "url": "https://www.linkedin.com/in/dhawal-sharma-zscaler/"},
], min_required=3, max_keep=10))

# Hugging Face
print("Hugging Face:", ingest_profiles("Hugging Face", [
    {"title": "Clement Delangue - CEO - Hugging Face | LinkedIn",                        "url": "https://www.linkedin.com/in/clementdelangue/"},
    {"title": "Julien Chaumond - CTO - Hugging Face | LinkedIn",                         "url": "https://www.linkedin.com/in/julienchaumond/"},
    {"title": "Thomas Wolf - Chief Science Officer - Hugging Face | LinkedIn",           "url": "https://www.linkedin.com/in/thomwolf/"},
    {"title": "Margaret Mitchell - Chief Ethics Scientist - Hugging Face | LinkedIn",    "url": "https://www.linkedin.com/in/margaret-mitchell-ai/"},
    {"title": "Lewis Tunstall - Machine Learning Engineer - Hugging Face | LinkedIn",    "url": "https://www.linkedin.com/in/lewistunstall/"},
    {"title": "Victor Sanh - Research Scientist - Hugging Face | LinkedIn",              "url": "https://www.linkedin.com/in/victorsanh/"},
    {"title": "Lysandre Debut - Research Engineer - Hugging Face | LinkedIn",            "url": "https://www.linkedin.com/in/lysandredebut/"},
    {"title": "Jeff Boudier - Head of Product - Hugging Face | LinkedIn",                "url": "https://www.linkedin.com/in/jeffboudier/"},
    {"title": "Omar Sanseviero - Chief of Staff ML - Hugging Face | LinkedIn",           "url": "https://www.linkedin.com/in/omarsanseviero/"},
    {"title": "Yacine Jernite - ML and Society Lead - Hugging Face | LinkedIn",          "url": "https://www.linkedin.com/in/yacinejernite/"},
], min_required=3, max_keep=10))

# Lam Research
print("Lam Research:", ingest_profiles("Lam Research", [
    {"title": "Tim Archer - President and CEO - Lam Research | LinkedIn",                "url": "https://www.linkedin.com/in/tim-archer-lam/"},
    {"title": "Doug Bettinger - CFO - Lam Research | LinkedIn",                          "url": "https://www.linkedin.com/in/dougbettinger/"},
    {"title": "Patrick Lord - COO - Lam Research | LinkedIn",                            "url": "https://www.linkedin.com/in/patrick-lord-lam/"},
    {"title": "Seshasayee Varadarajan - EVP Products - Lam Research | LinkedIn",         "url": "https://www.linkedin.com/in/seshasayee/"},
    {"title": "Vahid Vahedi - SVP Technology - Lam Research | LinkedIn",                 "url": "https://www.linkedin.com/in/vahidvahedi/"},
    {"title": "Richard Gottscho - EVP CTO - Lam Research | LinkedIn",                   "url": "https://www.linkedin.com/in/richardgottscho/"},
    {"title": "Gajus Worthington - Chief Strategy Officer - Lam Research | LinkedIn",   "url": "https://www.linkedin.com/in/gajusworthington/"},
    {"title": "Mary Humiston - SVP Chief HR Officer - Lam Research | LinkedIn",          "url": "https://www.linkedin.com/in/maryhumiston/"},
    {"title": "Ava Hahn - General Counsel - Lam Research | LinkedIn",                    "url": "https://www.linkedin.com/in/avahahn/"},
    {"title": "Uday Mitra - Chief Marketing Officer - Lam Research | LinkedIn",          "url": "https://www.linkedin.com/in/udaymitra/"},
], min_required=3, max_keep=10))

# ── Available contacts summary ────────────────────────────────────────────────
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

# ── STEP 3: Create campaign ───────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 3: Creating campaign"); print("="*60)
with get_db() as conn:
    existing = conn.execute("SELECT id FROM campaigns WHERE name=?", (CAMPAIGN_NAME,)).fetchone()
    if existing:
        campaign_id = existing["id"]
        print(f"  [=] Already exists: {campaign_id}")
    else:
        campaign_id = new_id()
        conn.execute("INSERT INTO campaigns (id, name, status) VALUES (?, ?, 'active')", (campaign_id, CAMPAIGN_NAME))
        print(f"  [+] Created: {CAMPAIGN_NAME}")
print(f"  Campaign ID: {campaign_id}")

# ── STEP 4: Personalize ───────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing — BBS template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(
    campaign_id=campaign_id,
    sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1,
    company_domains=COMPANY_DOMAINS,
    template="bbs",
    max_contacts_per_company=10,
    exclude_contacted=True,
)

# ── STEP 5: Send ─────────────────────────────────────────────────────────────
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
    SELECT sr.id as sr_id,
           ct.primary_email, ct.first_name, ct.last_name,
           co.name as company_name,
           pm.subject, pm.body
    FROM send_records sr
    JOIN contacts ct ON sr.contact_id = ct.id
    JOIN companies co ON ct.company_id = co.id
    JOIN personalized_messages pm ON sr.message_id = pm.id
    WHERE sr.campaign_id = ? AND sr.status = 'queued'
    ORDER BY co.name, ct.last_name
""", (campaign_id,)).fetchall()

print(f"  {len(rows)} emails queued — sending from eleynxiong@gmail.com...")

total_sent = 0; total_failed = 0

for row in rows:
    retries = 0
    while retries < 3:
        try:
            result = gmail.send_email(
                to=row["primary_email"],
                subject=row["subject"],
                body=row["body"],
                sender_name="Eleyn Xiong",
                sender_email="eleynxiong@gmail.com",
            )
            safe_exec(
                "UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=? WHERE id=?",
                (result["id"], result["threadId"], datetime.now().isoformat(), row["sr_id"])
            )
            total_sent += 1
            print(f"  [{total_sent}] {row['company_name']} - {row['first_name']} {row['last_name']} <{row['primary_email']}>")
            break
        except ConnectionResetError:
            retries += 1
            print(f"  [retry {retries}/3] Connection reset — waiting 30s...")
            time.sleep(30)
            try:
                gmail = GmailClient(account="gmail")
            except Exception:
                pass
        except Exception as e:
            total_failed += 1
            print(f"  [!] FAILED {row['primary_email']}: {e}")
            safe_exec(
                "UPDATE send_records SET status='failed',error=? WHERE id=?",
                (str(e)[:500], row["sr_id"])
            )
            break
    else:
        total_failed += 1
        print(f"  [!] GAVE UP {row['primary_email']} after 3 retries")
        safe_exec(
            "UPDATE send_records SET status='failed',error='ConnectionResetError after 3 retries' WHERE id=?",
            (row["sr_id"],)
        )
    time.sleep(random.uniform(60, 90))

conn_s.close()
print(f"\n{'='*60}")
print(f"DONE — {total_sent} sent, {total_failed} failed")
print(f"Sender: eleynxiong@gmail.com | Campaign: {CAMPAIGN_NAME}")
print(f"{'='*60}")
