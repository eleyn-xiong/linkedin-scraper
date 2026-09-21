"""BBS Batch 10 — 25 new Fortune 500 companies, 10 emails each, eleynxiong@berkeley.edu."""
import sys, time, random, sqlite3
from schedule_utils import check_send_window
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
    {"name": "Fifth Third Bancorp",      "domain": "53.com",              "industry": "Regional Banking / Consumer and Commercial Finance / Wealth Management", "email_pattern": "first.last"},
    {"name": "Comerica",                  "domain": "comerica.com",        "industry": "Commercial Banking / Wealth Management / Treasury / Business Finance",   "email_pattern": "first.last"},
    {"name": "Unum Group",                "domain": "unum.com",            "industry": "Group Benefits / Life Disability Dental Vision Insurance",               "email_pattern": "first.last"},
    {"name": "Lincoln National",          "domain": "lincolnnational.com", "industry": "Life Insurance / Annuities / Retirement Plans / Group Protection",       "email_pattern": "first.last"},
    {"name": "Erie Indemnity",            "domain": "erieindemnity.com",   "industry": "Property Casualty Insurance / Auto Home Business Erie agents",           "email_pattern": "first.last"},
    {"name": "Markel Group",              "domain": "markel.com",          "industry": "Specialty Insurance / Reinsurance / Markel Ventures / Investments",      "email_pattern": "first.last"},
    {"name": "CACI International",        "domain": "caci.com",            "industry": "Defense IT / Intelligence / Cyber / Government Technology Services",     "email_pattern": "first.last"},
    {"name": "Textron",                   "domain": "textron.com",         "industry": "Aerospace Defense Aviation Bell Helicopter Cessna Textron Systems",      "email_pattern": "first.last"},
    {"name": "Howmet Aerospace",          "domain": "howmet.com",          "industry": "Aerospace Engine Components / Fastening Systems / Engineered Structures","email_pattern": "first.last"},
    {"name": "Entergy",                   "domain": "entergy.com",         "industry": "Electric Utility / Nuclear Power / Regulated Energy / Gulf South",       "email_pattern": "first.last"},
    {"name": "Ameren",                    "domain": "ameren.com",          "industry": "Electric and Gas Utility / Missouri Illinois / Transmission / Renewables","email_pattern": "first.last"},
    {"name": "Consolidated Edison",       "domain": "conedison.com",       "industry": "Electric and Gas Utility / New York / Sustainability / Clean Energy",    "email_pattern": "first.last"},
    {"name": "Eastman Chemical",          "domain": "eastman.com",         "industry": "Specialty Chemicals / Advanced Materials / Fibers / Circular Economy",   "email_pattern": "first.last"},
    {"name": "Huntsman Corporation",      "domain": "huntsman.com",        "industry": "Polyurethanes / Performance Products / Advanced Materials / Specialty",  "email_pattern": "first.last"},
    {"name": "DaVita",                    "domain": "davita.com",          "industry": "Kidney Care / Dialysis / Integrated Kidney Health / Value Based Care",   "email_pattern": "first.last"},
    {"name": "Tenet Healthcare",          "domain": "tenethealth.com",     "industry": "Acute Care Hospitals / Ambulatory Surgery / USPI / Health Systems",      "email_pattern": "first.last"},
    {"name": "Henry Schein",              "domain": "henryschein.com",     "industry": "Healthcare Products Distribution / Dental Medical Vet / Technology",     "email_pattern": "first.last"},
    {"name": "Lamb Weston",               "domain": "lambweston.com",      "industry": "Frozen Potato Products / Foodservice / Food Manufacturing / Supply",     "email_pattern": "first.last"},
    {"name": "Post Holdings",             "domain": "postholdings.com",    "industry": "Consumer Food Brands / Cereal / Pet Food / Private Label / Foodservice", "email_pattern": "first.last"},
    {"name": "AutoZone",                  "domain": "autozone.com",        "industry": "Auto Parts Retail / DIY and DIFM / Commercial / International Stores",   "email_pattern": "first.last"},
    {"name": "CarMax",                    "domain": "carmax.com",          "industry": "Used Vehicle Retail / Auto Finance / Digital Car Buying / CarMax Auto",  "email_pattern": "first.last"},
    {"name": "Ryder System",              "domain": "ryder.com",           "industry": "Fleet Management / Supply Chain / Last Mile Delivery / Truck Leasing",   "email_pattern": "first.last"},
    {"name": "CoStar Group",              "domain": "costar.com",          "industry": "Commercial Real Estate Data / Apartments.com / LoopNet / Analytics",     "email_pattern": "first.last"},
    {"name": "RPM International",         "domain": "rpminc.com",          "industry": "Specialty Coatings Sealants Adhesives / Rust-Oleum / DAP / Tremco",      "email_pattern": "first.last"},
    {"name": "Macys",                     "domain": "macys.com",           "industry": "Department Store / Fashion Retail / Bloomingdale's / Digital Commerce",  "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 10 - July 2026"
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
                (new_id(), c["name"], c["domain"], c["industry"], c["email_pattern"], 70.0))
            print(f"  [+] {c['name']}")
        except Exception as e:
            print(f"  [=] {c['name']} already exists" if "UNIQUE" in str(e).upper() else f"  [!] {e}")

print("\n" + "="*60); print("STEP 2: Ingesting profiles"); print("="*60)

print("Fifth Third Bancorp:", ingest_profiles("Fifth Third Bancorp", [
    {"title": "Tim Spence - President and CEO - Fifth Third Bancorp | LinkedIn",                   "url": "https://www.linkedin.com/in/timspence-53/"},
    {"title": "Bryan Preston - EVP and CFO - Fifth Third Bancorp | LinkedIn",                      "url": "https://www.linkedin.com/in/bryanpreston-53/"},
    {"title": "Jamie Leonard - EVP and Chief Risk Officer - Fifth Third Bancorp | LinkedIn",       "url": "https://www.linkedin.com/in/jamieleonard-53/"},
    {"title": "Corinne Bailey - EVP Consumer Banking - Fifth Third Bancorp | LinkedIn",            "url": "https://www.linkedin.com/in/corinnejbailey-53/"},
    {"title": "Ben Hoffman - EVP Commercial Banking - Fifth Third Bancorp | LinkedIn",             "url": "https://www.linkedin.com/in/benhoffman-53/"},
    {"title": "Bridget Frey - EVP and Chief Technology Officer - Fifth Third Bancorp | LinkedIn",  "url": "https://www.linkedin.com/in/bridgetfrey-53/"},
    {"title": "Kala Gibson - EVP Chief Corporate Responsibility - Fifth Third Bancorp | LinkedIn", "url": "https://www.linkedin.com/in/kalagibson-53/"},
    {"title": "Howard Hammond - EVP Chief Human Resources - Fifth Third Bancorp | LinkedIn",      "url": "https://www.linkedin.com/in/howardhammond-53/"},
    {"title": "Tayfun Tuzun - Former EVP and CFO - Fifth Third Bancorp | LinkedIn",               "url": "https://www.linkedin.com/in/tayfuntuzun-53/"},
    {"title": "Matt Jauchius - EVP Chief Marketing Officer - Fifth Third Bancorp | LinkedIn",     "url": "https://www.linkedin.com/in/mattjauchius-53/"},
], min_required=3, max_keep=10))

print("Comerica:", ingest_profiles("Comerica", [
    {"title": "Curtis Farmer - Chairman President and CEO - Comerica | LinkedIn",                  "url": "https://www.linkedin.com/in/curtisfarmer-comerica/"},
    {"title": "James Herzog - EVP and CFO - Comerica | LinkedIn",                                  "url": "https://www.linkedin.com/in/jamesherzog-comerica/"},
    {"title": "Peter Guilfoile - EVP and Chief Risk Officer - Comerica | LinkedIn",               "url": "https://www.linkedin.com/in/peterguilfoile-comerica/"},
    {"title": "Cassandra McKinney - EVP Chief Human Resources - Comerica | LinkedIn",             "url": "https://www.linkedin.com/in/cassandramckinney-comerica/"},
    {"title": "Megan Burkhart - EVP General Counsel - Comerica | LinkedIn",                       "url": "https://www.linkedin.com/in/meganburkhart-comerica/"},
    {"title": "Bill Tucker - EVP Commercial Banking - Comerica | LinkedIn",                        "url": "https://www.linkedin.com/in/billtucker-comerica/"},
    {"title": "Curt Farmer - President Western Market - Comerica | LinkedIn",                     "url": "https://www.linkedin.com/in/curtfarmer-comerica/"},
    {"title": "Muneera Carr - EVP and Chief Accounting Officer - Comerica | LinkedIn",            "url": "https://www.linkedin.com/in/muneeracarr-comerica/"},
    {"title": "Michael Ritchie - VP Investor Relations - Comerica | LinkedIn",                    "url": "https://www.linkedin.com/in/michaelritchie-comerica/"},
    {"title": "Nadia Laurinci - SVP Human Resources - Comerica | LinkedIn",                       "url": "https://www.linkedin.com/in/nadialaurinci-comerica/"},
], min_required=3, max_keep=10))

print("Unum Group:", ingest_profiles("Unum Group", [
    {"title": "Rick McKenney - President and CEO - Unum Group | LinkedIn",                         "url": "https://www.linkedin.com/in/rickmckenney-unum/"},
    {"title": "Steve Zabel - EVP and CFO - Unum Group | LinkedIn",                                 "url": "https://www.linkedin.com/in/stevezabel-unum/"},
    {"title": "Tim Arnold - EVP and President Unum Benefits - Unum Group | LinkedIn",              "url": "https://www.linkedin.com/in/timarnold-unum/"},
    {"title": "Kate Terry - EVP and President Colonial Life - Unum Group | LinkedIn",              "url": "https://www.linkedin.com/in/kateterry-unum/"},
    {"title": "Lisa Iglesias - EVP General Counsel - Unum Group | LinkedIn",                       "url": "https://www.linkedin.com/in/lisaiglesias-unum/"},
    {"title": "Jody Davids - EVP Chief Information Officer - Unum Group | LinkedIn",               "url": "https://www.linkedin.com/in/jodydavids-unum/"},
    {"title": "Mike Simonds - Former EVP and President - Unum Group | LinkedIn",                   "url": "https://www.linkedin.com/in/mikesimonds-unum/"},
    {"title": "Jack McGarry - EVP and President Unum International - Unum Group | LinkedIn",      "url": "https://www.linkedin.com/in/jackmcgarry-unum/"},
    {"title": "Peter Burke - VP Investor Relations - Unum Group | LinkedIn",                       "url": "https://www.linkedin.com/in/peterburke-unum/"},
    {"title": "Breege Farrell - EVP Chief HR Officer - Unum Group | LinkedIn",                    "url": "https://www.linkedin.com/in/breegfarrell-unum/"},
], min_required=3, max_keep=10))

print("Lincoln National:", ingest_profiles("Lincoln National", [
    {"title": "Ellen Cooper - President and CEO - Lincoln National Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/ellencooper-lincolnnational/"},
    {"title": "Chris Neczypor - EVP and CFO - Lincoln National Corporation | LinkedIn",            "url": "https://www.linkedin.com/in/chrisneczypor-lnc/"},
    {"title": "Craig Bromley - President Insurance Solutions - Lincoln National | LinkedIn",        "url": "https://www.linkedin.com/in/craigbromley-lnc/"},
    {"title": "Barbara Turner - President Group Protection - Lincoln National | LinkedIn",          "url": "https://www.linkedin.com/in/barbaraturner-lnc/"},
    {"title": "Will Fuller - EVP and President Annuities - Lincoln National | LinkedIn",            "url": "https://www.linkedin.com/in/willfuller-lnc/"},
    {"title": "Jayson Bronchetti - EVP Chief HR Officer - Lincoln National | LinkedIn",            "url": "https://www.linkedin.com/in/jaysonbronchetti-lnc/"},
    {"title": "Tore Stole - EVP and CIO Retirement Plan Services - Lincoln National | LinkedIn",   "url": "https://www.linkedin.com/in/torestole-lnc/"},
    {"title": "Adam Cardinal - SVP and General Counsel - Lincoln National | LinkedIn",             "url": "https://www.linkedin.com/in/adamcardinal-lnc/"},
    {"title": "Al Zucaro - SVP Investor Relations - Lincoln National | LinkedIn",                  "url": "https://www.linkedin.com/in/alzucaro-lnc/"},
    {"title": "Chuck Cornelio - EVP and President Life Insurance - Lincoln National | LinkedIn",   "url": "https://www.linkedin.com/in/chuckcornelio-lnc/"},
], min_required=3, max_keep=10))

print("Erie Indemnity:", ingest_profiles("Erie Indemnity", [
    {"title": "Timothy NeCastro - President and CEO - Erie Indemnity Company | LinkedIn",          "url": "https://www.linkedin.com/in/timothynecastro-erie/"},
    {"title": "Gregory Gutting - EVP and CFO - Erie Indemnity Company | LinkedIn",                "url": "https://www.linkedin.com/in/gregorygutting-erie/"},
    {"title": "Lorianne Feltz - SVP Chief Risk Officer - Erie Indemnity Company | LinkedIn",      "url": "https://www.linkedin.com/in/loriannefeltz-erie/"},
    {"title": "John Kearns - EVP Chief Insurance Officer - Erie Indemnity Company | LinkedIn",    "url": "https://www.linkedin.com/in/johnkearns-erie/"},
    {"title": "Brian Bolash - SVP and General Counsel - Erie Indemnity Company | LinkedIn",       "url": "https://www.linkedin.com/in/brianbolash-erie/"},
    {"title": "Douglas Smith - SVP Sales - Erie Indemnity Company | LinkedIn",                    "url": "https://www.linkedin.com/in/douglassmith-erie/"},
    {"title": "Sarah Brown - SVP Customer Experience - Erie Indemnity Company | LinkedIn",        "url": "https://www.linkedin.com/in/sarahbrown-erie/"},
    {"title": "Terrence Cavanaugh - Former President - Erie Indemnity Company | LinkedIn",        "url": "https://www.linkedin.com/in/terrencecavanaugh-erie/"},
    {"title": "Scott Beilharz - VP Investor Relations - Erie Indemnity Company | LinkedIn",       "url": "https://www.linkedin.com/in/scottbeilharz-erie/"},
    {"title": "Beth Doerr - SVP Chief HR Officer - Erie Indemnity Company | LinkedIn",            "url": "https://www.linkedin.com/in/bethdoerr-erie/"},
], min_required=3, max_keep=10))

print("Markel Group:", ingest_profiles("Markel Group", [
    {"title": "Tom Gayner - Co-CEO and President Markel Investments - Markel Group | LinkedIn",    "url": "https://www.linkedin.com/in/tomgayner-markel/"},
    {"title": "Rich Whitt - Co-CEO Insurance Operations - Markel Group | LinkedIn",               "url": "https://www.linkedin.com/in/richwhitt-markel/"},
    {"title": "Jeremy Noble - EVP and CFO - Markel Group | LinkedIn",                             "url": "https://www.linkedin.com/in/jeremynoble-markel/"},
    {"title": "Gerry Albanese - EVP Global Insurance - Markel Group | LinkedIn",                  "url": "https://www.linkedin.com/in/gerryalbanese-markel/"},
    {"title": "Yael Benjamini - EVP and Chief Underwriting Officer - Markel Group | LinkedIn",    "url": "https://www.linkedin.com/in/yaelbenjamini-markel/"},
    {"title": "Nalini Bhatt - SVP Chief HR Officer - Markel Group | LinkedIn",                    "url": "https://www.linkedin.com/in/nalinibhatt-markel/"},
    {"title": "Richard Whitt III - President Wholesale Division - Markel Group | LinkedIn",       "url": "https://www.linkedin.com/in/richardwhittiii-markel/"},
    {"title": "Bryan Sanders - EVP and General Counsel - Markel Group | LinkedIn",                "url": "https://www.linkedin.com/in/bryansanders-markel/"},
    {"title": "Andrew Crowley - VP Investor Relations - Markel Group | LinkedIn",                 "url": "https://www.linkedin.com/in/andrewcrowley-markel/"},
    {"title": "Kirsten Gillespie - EVP and Head of Reinsurance - Markel Group | LinkedIn",       "url": "https://www.linkedin.com/in/kirstengillespie-markel/"},
], min_required=3, max_keep=10))

print("CACI International:", ingest_profiles("CACI International", [
    {"title": "John Mengucci - President and CEO - CACI International | LinkedIn",                 "url": "https://www.linkedin.com/in/johnmengucci-caci/"},
    {"title": "Jeffrey MacLauchlan - EVP and CFO - CACI International | LinkedIn",               "url": "https://www.linkedin.com/in/jeffreymaclauchan-caci/"},
    {"title": "DeEtte Gray - EVP and President Domestic Operations - CACI International | LinkedIn","url": "https://www.linkedin.com/in/deettegray-caci/"},
    {"title": "Greg Bradford - SVP Defense and Intelligence - CACI International | LinkedIn",     "url": "https://www.linkedin.com/in/gregbradford-caci/"},
    {"title": "Carla Lucchino - EVP Chief HR Officer - CACI International | LinkedIn",            "url": "https://www.linkedin.com/in/carlalucchino-caci/"},
    {"title": "Kathleen Biberstein - EVP Legal and Compliance - CACI International | LinkedIn",   "url": "https://www.linkedin.com/in/kathleenbiberstein-caci/"},
    {"title": "Jim Garrettson - SVP Strategy and Business Development - CACI | LinkedIn",         "url": "https://www.linkedin.com/in/jimgarrettson-caci/"},
    {"title": "Todd Probert - SVP and President Defense and Intelligence - CACI | LinkedIn",      "url": "https://www.linkedin.com/in/toddprobert-caci/"},
    {"title": "Dan Leckburg - VP Investor Relations - CACI International | LinkedIn",             "url": "https://www.linkedin.com/in/danleckburg-caci/"},
    {"title": "Brad Medairy - SVP Cyber and Intelligence - CACI International | LinkedIn",       "url": "https://www.linkedin.com/in/bradmedairy-caci/"},
], min_required=3, max_keep=10))

print("Textron:", ingest_profiles("Textron", [
    {"title": "Scott Donnelly - Chairman President and CEO - Textron | LinkedIn",                  "url": "https://www.linkedin.com/in/scottdonnelly-textron/"},
    {"title": "Frank Connor - EVP and CFO - Textron | LinkedIn",                                   "url": "https://www.linkedin.com/in/frankconnor-textron/"},
    {"title": "Mark Bamford - President Bell - Textron | LinkedIn",                               "url": "https://www.linkedin.com/in/markbamford-textron/"},
    {"title": "Ron Draper - President Textron Aviation - Textron | LinkedIn",                      "url": "https://www.linkedin.com/in/rondraper-textron/"},
    {"title": "Ellen Lord - Former EVP - Textron | LinkedIn",                                      "url": "https://www.linkedin.com/in/ellenlord-textron/"},
    {"title": "Kevin Cummings - President Textron Systems - Textron | LinkedIn",                   "url": "https://www.linkedin.com/in/kevincummings-textron/"},
    {"title": "Mary Lovejoy - SVP Chief HR Officer - Textron | LinkedIn",                          "url": "https://www.linkedin.com/in/marylovejoy-textron/"},
    {"title": "Howard Kass - SVP General Counsel - Textron | LinkedIn",                            "url": "https://www.linkedin.com/in/howardkass-textron/"},
    {"title": "Rob Goglia - VP Investor Relations - Textron | LinkedIn",                           "url": "https://www.linkedin.com/in/robgoglia-textron/"},
    {"title": "Cheryl Johnson - President Kautex - Textron | LinkedIn",                            "url": "https://www.linkedin.com/in/cheryljohnson-textron/"},
], min_required=3, max_keep=10))

print("Howmet Aerospace:", ingest_profiles("Howmet Aerospace", [
    {"title": "John Plant - Executive Chairman - Howmet Aerospace | LinkedIn",                     "url": "https://www.linkedin.com/in/johnplant-howmet/"},
    {"title": "Tolga Oal - President and CEO - Howmet Aerospace | LinkedIn",                       "url": "https://www.linkedin.com/in/tolgaoal-howmet/"},
    {"title": "Ken Giacobbe - EVP and CFO - Howmet Aerospace | LinkedIn",                          "url": "https://www.linkedin.com/in/kengiacobbe-howmet/"},
    {"title": "Paul Luther - SVP General Counsel - Howmet Aerospace | LinkedIn",                   "url": "https://www.linkedin.com/in/paulluther-howmet/"},
    {"title": "Neil Marchuk - SVP Chief HR Officer - Howmet Aerospace | LinkedIn",                 "url": "https://www.linkedin.com/in/neilmarchuk-howmet/"},
    {"title": "Keith Harvey - President Engine Products - Howmet Aerospace | LinkedIn",            "url": "https://www.linkedin.com/in/keithharvey-howmet/"},
    {"title": "Tim Myers - President Fastening Systems - Howmet Aerospace | LinkedIn",             "url": "https://www.linkedin.com/in/timmyers-howmet/"},
    {"title": "Rob Fisher - SVP Advanced Manufacturing - Howmet Aerospace | LinkedIn",             "url": "https://www.linkedin.com/in/robfisher-howmet/"},
    {"title": "Bill Whitfield - VP Investor Relations - Howmet Aerospace | LinkedIn",              "url": "https://www.linkedin.com/in/billwhitfield-howmet/"},
    {"title": "Eitan Rosenberg - President Engineered Structures - Howmet Aerospace | LinkedIn",  "url": "https://www.linkedin.com/in/eitanrosenberg-howmet/"},
], min_required=3, max_keep=10))

print("Entergy:", ingest_profiles("Entergy", [
    {"title": "Drew Marsh - Chairman and CEO - Entergy Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/drewmarsh-entergy/"},
    {"title": "Kimberly Fontan - EVP and CFO - Entergy Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/kimberlyfontan-entergy/"},
    {"title": "Marcus Brown - EVP and COO - Entergy Corporation | LinkedIn",                       "url": "https://www.linkedin.com/in/marcusbrown-entergy/"},
    {"title": "Phillip May - President Entergy Louisiana - Entergy Corporation | LinkedIn",        "url": "https://www.linkedin.com/in/philliprmay-entergy/"},
    {"title": "Sallie Rainer - President Entergy Texas - Entergy Corporation | LinkedIn",          "url": "https://www.linkedin.com/in/sallierainer-entergy/"},
    {"title": "Laura Landreaux - President Entergy Arkansas - Entergy Corporation | LinkedIn",     "url": "https://www.linkedin.com/in/lauralandreaux-entergy/"},
    {"title": "Paula Waters - EVP General Counsel - Entergy Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/paulawaters-entergy/"},
    {"title": "Rod West - EVP Utility Operations - Entergy Corporation | LinkedIn",                "url": "https://www.linkedin.com/in/rodwest-entergy/"},
    {"title": "Alyson Mount - VP Investor Relations - Entergy Corporation | LinkedIn",             "url": "https://www.linkedin.com/in/alysonmount-entergy/"},
    {"title": "Deanna Rodriguez - President Entergy New Orleans - Entergy | LinkedIn",             "url": "https://www.linkedin.com/in/deannaodriguez-entergy/"},
], min_required=3, max_keep=10))

print("Ameren:", ingest_profiles("Ameren", [
    {"title": "Marty Lyons - Chairman and CEO - Ameren Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/martylyons-ameren/"},
    {"title": "Mark Birk - EVP and CFO - Ameren Corporation | LinkedIn",                           "url": "https://www.linkedin.com/in/markbirk-ameren/"},
    {"title": "Michael Moehn - President Ameren Missouri - Ameren Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/michaelmoehn-ameren/"},
    {"title": "Bhavani Amirthalingam - President Ameren Illinois - Ameren Corporation | LinkedIn", "url": "https://www.linkedin.com/in/bhavaniamirthalingam-ameren/"},
    {"title": "Shawn Schukar - EVP and General Counsel - Ameren Corporation | LinkedIn",           "url": "https://www.linkedin.com/in/shawnschukar-ameren/"},
    {"title": "Maureen Borkowski - EVP Chief HR Officer - Ameren Corporation | LinkedIn",          "url": "https://www.linkedin.com/in/maureenborkowski-ameren/"},
    {"title": "Andrew Kirk - VP Investor Relations - Ameren Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/andrewkirk-ameren/"},
    {"title": "Fadi Diya - EVP and Chief Digital Officer - Ameren Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/fadidiya-ameren/"},
    {"title": "Cara Garretson - SVP Operations - Ameren Missouri | LinkedIn",                      "url": "https://www.linkedin.com/in/caragarretson-ameren/"},
    {"title": "Richard Mark - EVP and President Ameren Transmission - Ameren | LinkedIn",         "url": "https://www.linkedin.com/in/richardmark-ameren/"},
], min_required=3, max_keep=10))

print("Consolidated Edison:", ingest_profiles("Consolidated Edison", [
    {"title": "Tim Cawley - Chairman and CEO - Consolidated Edison | LinkedIn",                    "url": "https://www.linkedin.com/in/timcawley-coned/"},
    {"title": "Rob Hoglund - SVP and CFO - Consolidated Edison | LinkedIn",                        "url": "https://www.linkedin.com/in/robhoglund-coned/"},
    {"title": "Matthew Ketschke - President Con Edison of New York - ConEd | LinkedIn",            "url": "https://www.linkedin.com/in/matthewketschke-coned/"},
    {"title": "Joseph Oates - EVP Corporate Affairs - Consolidated Edison | LinkedIn",             "url": "https://www.linkedin.com/in/josephoates-coned/"},
    {"title": "Robert Sanchez - SVP Operations - Consolidated Edison | LinkedIn",                  "url": "https://www.linkedin.com/in/robertsanchez-coned/"},
    {"title": "Amy Kessler - SVP Customer Operations - Consolidated Edison | LinkedIn",            "url": "https://www.linkedin.com/in/amykessler-coned/"},
    {"title": "Brian Sweeney - SVP External Affairs - Consolidated Edison | LinkedIn",             "url": "https://www.linkedin.com/in/briansweeney-coned/"},
    {"title": "Alan Draper - SVP Human Resources - Consolidated Edison | LinkedIn",               "url": "https://www.linkedin.com/in/alandraper-coned/"},
    {"title": "Yukari Saegusa - VP Investor Relations - Consolidated Edison | LinkedIn",           "url": "https://www.linkedin.com/in/yukasaegusa-coned/"},
    {"title": "Carl Horowitz - VP Technology - Consolidated Edison | LinkedIn",                    "url": "https://www.linkedin.com/in/carlhorowitz-coned/"},
], min_required=3, max_keep=10))

print("Eastman Chemical:", ingest_profiles("Eastman Chemical", [
    {"title": "Mark Costa - Chairman and CEO - Eastman Chemical Company | LinkedIn",               "url": "https://www.linkedin.com/in/markcosta-eastman/"},
    {"title": "Willie McLain - EVP and CFO - Eastman Chemical Company | LinkedIn",                "url": "https://www.linkedin.com/in/williemclain-eastman/"},
    {"title": "Brad Lich - EVP Chief Commercial Officer - Eastman Chemical | LinkedIn",            "url": "https://www.linkedin.com/in/bradlich-eastman/"},
    {"title": "Steve Crawford - EVP and Chief Operating Officer - Eastman Chemical | LinkedIn",   "url": "https://www.linkedin.com/in/stevecrawford-eastman/"},
    {"title": "Chris Killian - EVP Technology - Eastman Chemical Company | LinkedIn",             "url": "https://www.linkedin.com/in/chriskillian-eastman/"},
    {"title": "Eric Becraft - SVP General Counsel - Eastman Chemical Company | LinkedIn",         "url": "https://www.linkedin.com/in/ericbecraft-eastman/"},
    {"title": "Perry Stuckey - SVP Chief HR Officer - Eastman Chemical Company | LinkedIn",       "url": "https://www.linkedin.com/in/perrystuckey-eastman/"},
    {"title": "Mike Kaufman - SVP Global Business Services - Eastman Chemical | LinkedIn",        "url": "https://www.linkedin.com/in/mikekaufman-eastman/"},
    {"title": "Brett Schloss - VP Investor Relations - Eastman Chemical Company | LinkedIn",      "url": "https://www.linkedin.com/in/brettschloss-eastman/"},
    {"title": "Reilly Whitfield - VP Operations - Eastman Chemical Company | LinkedIn",           "url": "https://www.linkedin.com/in/reillywhitfield-eastman/"},
], min_required=3, max_keep=10))

print("Huntsman Corporation:", ingest_profiles("Huntsman Corporation", [
    {"title": "Peter Huntsman - Chairman and CEO - Huntsman Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/peterhuntsman/"},
    {"title": "Phil Lister - EVP and CFO - Huntsman Corporation | LinkedIn",                       "url": "https://www.linkedin.com/in/phillister-huntsman/"},
    {"title": "Monte Edlund - President Performance Products - Huntsman Corporation | LinkedIn",   "url": "https://www.linkedin.com/in/monteedlund-huntsman/"},
    {"title": "Don Lamb - SVP General Counsel - Huntsman Corporation | LinkedIn",                  "url": "https://www.linkedin.com/in/donlamb-huntsman/"},
    {"title": "Ivan Marcuse - SVP Strategy and Business Development - Huntsman | LinkedIn",       "url": "https://www.linkedin.com/in/ivanmarcuse-huntsman/"},
    {"title": "Nils Hansson - SVP Advanced Materials - Huntsman Corporation | LinkedIn",           "url": "https://www.linkedin.com/in/nilshansson-huntsman/"},
    {"title": "Tony Hankins - SVP Polyurethanes - Huntsman Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/tonyhankins-huntsman/"},
    {"title": "David Warnock - VP Investor Relations - Huntsman Corporation | LinkedIn",           "url": "https://www.linkedin.com/in/davidwarnock-huntsman/"},
    {"title": "Gary Hunt - VP Human Resources - Huntsman Corporation | LinkedIn",                  "url": "https://www.linkedin.com/in/garyhunt-huntsman/"},
    {"title": "Ron Gerrard - SVP Textile Effects - Huntsman Corporation | LinkedIn",              "url": "https://www.linkedin.com/in/rongerrard-huntsman/"},
], min_required=3, max_keep=10))

print("DaVita:", ingest_profiles("DaVita", [
    {"title": "Javier Rodriguez - CEO - DaVita Inc | LinkedIn",                                    "url": "https://www.linkedin.com/in/javierrodriguez-davita/"},
    {"title": "Joel Ackerman - EVP and CFO - DaVita Inc | LinkedIn",                              "url": "https://www.linkedin.com/in/joelackerman-davita/"},
    {"title": "Kathleen Waters - EVP and COO - DaVita Inc | LinkedIn",                            "url": "https://www.linkedin.com/in/kathleenwaters-davita/"},
    {"title": "Bill Kelman - EVP Chief Legal Officer - DaVita Inc | LinkedIn",                    "url": "https://www.linkedin.com/in/billkelman-davita/"},
    {"title": "Rik Bhatt - EVP Chief People Officer - DaVita Inc | LinkedIn",                     "url": "https://www.linkedin.com/in/rikbhatt-davita/"},
    {"title": "Jim Hilger - EVP Chief Medical Officer - DaVita Inc | LinkedIn",                   "url": "https://www.linkedin.com/in/jimhilger-davita/"},
    {"title": "Kim Rivera - EVP and Chief Legal Officer - DaVita Inc | LinkedIn",                  "url": "https://www.linkedin.com/in/kimrivera-davita/"},
    {"title": "Vikram Bajaj - EVP Digital Health - DaVita Inc | LinkedIn",                        "url": "https://www.linkedin.com/in/vikrambajaj-davita/"},
    {"title": "Erica Gadsby - VP Investor Relations - DaVita Inc | LinkedIn",                     "url": "https://www.linkedin.com/in/ericagadsby-davita/"},
    {"title": "Dennis Kogod - EVP Chief Operating Officer - DaVita Inc | LinkedIn",               "url": "https://www.linkedin.com/in/denniskogod-davita/"},
], min_required=3, max_keep=10))

print("Tenet Healthcare:", ingest_profiles("Tenet Healthcare", [
    {"title": "Saum Sutaria - Chairman and CEO - Tenet Healthcare | LinkedIn",                     "url": "https://www.linkedin.com/in/saumsutaria-tenet/"},
    {"title": "Sun Park - EVP and CFO - Tenet Healthcare | LinkedIn",                              "url": "https://www.linkedin.com/in/sunpark-tenet/"},
    {"title": "Saumya Sutaria - EVP and President USPI - Tenet Healthcare | LinkedIn",            "url": "https://www.linkedin.com/in/saumyasutaria-tenet/"},
    {"title": "Chad Pettit - EVP and President Hospital Operations - Tenet Healthcare | LinkedIn", "url": "https://www.linkedin.com/in/chadpettit-tenet/"},
    {"title": "Paul Castanon - EVP General Counsel - Tenet Healthcare | LinkedIn",                "url": "https://www.linkedin.com/in/paulcastanon-tenet/"},
    {"title": "Kyle Napper - SVP Chief HR Officer - Tenet Healthcare | LinkedIn",                  "url": "https://www.linkedin.com/in/kylenapper-tenet/"},
    {"title": "Britt Reynolds - EVP Operations - Tenet Healthcare | LinkedIn",                    "url": "https://www.linkedin.com/in/brittreynolds-tenet/"},
    {"title": "Alex Barron - EVP Chief Strategy Officer - Tenet Healthcare | LinkedIn",           "url": "https://www.linkedin.com/in/alexbarron-tenet/"},
    {"title": "Will McIntyre - VP Investor Relations - Tenet Healthcare | LinkedIn",              "url": "https://www.linkedin.com/in/willmcintyre-tenet/"},
    {"title": "Ben Breier - Former EVP and President USPI - Tenet Healthcare | LinkedIn",         "url": "https://www.linkedin.com/in/benbreier-tenet/"},
], min_required=3, max_keep=10))

print("Henry Schein:", ingest_profiles("Henry Schein", [
    {"title": "Stanley Bergman - Chairman and CEO - Henry Schein | LinkedIn",                      "url": "https://www.linkedin.com/in/stanleybergman-henryschein/"},
    {"title": "Ronald South - EVP and CFO - Henry Schein | LinkedIn",                             "url": "https://www.linkedin.com/in/ronaldsouth-henryschein/"},
    {"title": "Brad Connett - President North America Dental - Henry Schein | LinkedIn",           "url": "https://www.linkedin.com/in/bradconnett-henryschein/"},
    {"title": "Gerald Benjamin - EVP Chief Administrative Officer - Henry Schein | LinkedIn",     "url": "https://www.linkedin.com/in/geraldbenjamin-henryschein/"},
    {"title": "Mark Mlotek - EVP Corporate Business Development - Henry Schein | LinkedIn",       "url": "https://www.linkedin.com/in/markmlotek-henryschein/"},
    {"title": "Walter Siegel - EVP and General Counsel - Henry Schein | LinkedIn",                "url": "https://www.linkedin.com/in/waltersiegel-henryschein/"},
    {"title": "Lorelei McGlynn - SVP Chief HR Officer - Henry Schein | LinkedIn",                 "url": "https://www.linkedin.com/in/loreleimcglynn-henryschein/"},
    {"title": "Paul Guggenheim - President Global Dental - Henry Schein | LinkedIn",              "url": "https://www.linkedin.com/in/paulguggenheim-henryschein/"},
    {"title": "Carolynne Borders - VP Investor Relations - Henry Schein | LinkedIn",              "url": "https://www.linkedin.com/in/carolynneborders-henryschein/"},
    {"title": "James Breslawski - Former President - Henry Schein | LinkedIn",                    "url": "https://www.linkedin.com/in/jamesbreslawski-henryschein/"},
], min_required=3, max_keep=10))

print("Lamb Weston:", ingest_profiles("Lamb Weston", [
    {"title": "Tom Werner - President and CEO - Lamb Weston | LinkedIn",                           "url": "https://www.linkedin.com/in/tomwerner-lambweston/"},
    {"title": "Bernadette Madarieta - EVP and CFO - Lamb Weston | LinkedIn",                      "url": "https://www.linkedin.com/in/bernadettemadarieta-lambweston/"},
    {"title": "Erica Sanford - EVP Chief HR Officer - Lamb Weston | LinkedIn",                    "url": "https://www.linkedin.com/in/ericasanford-lambweston/"},
    {"title": "Michael Smith - EVP Chief Legal Officer - Lamb Weston | LinkedIn",                 "url": "https://www.linkedin.com/in/michaelsmith-lambweston/"},
    {"title": "Justin Grose - SVP Foodservice Sales - Lamb Weston | LinkedIn",                    "url": "https://www.linkedin.com/in/justingrose-lambweston/"},
    {"title": "Alexis Becker - SVP North American Retail - Lamb Weston | LinkedIn",               "url": "https://www.linkedin.com/in/alexisbecker-lambweston/"},
    {"title": "Kirk Glenn - SVP Operations - Lamb Weston | LinkedIn",                             "url": "https://www.linkedin.com/in/kirkglenn-lambweston/"},
    {"title": "Lori Walker - SVP Marketing - Lamb Weston | LinkedIn",                             "url": "https://www.linkedin.com/in/loriwalker-lambweston/"},
    {"title": "Dexter Congbalay - VP Investor Relations - Lamb Weston | LinkedIn",                "url": "https://www.linkedin.com/in/dextercongbalay-lambweston/"},
    {"title": "David Colo - Former President and CEO - Lamb Weston | LinkedIn",                   "url": "https://www.linkedin.com/in/davidcolo-lambweston/"},
], min_required=3, max_keep=10))

print("Post Holdings:", ingest_profiles("Post Holdings", [
    {"title": "Rob Vitale - President and CEO - Post Holdings | LinkedIn",                         "url": "https://www.linkedin.com/in/robvitale-postholdings/"},
    {"title": "Matt Mainer - SVP and CFO - Post Holdings | LinkedIn",                             "url": "https://www.linkedin.com/in/mattmainer-postholdings/"},
    {"title": "Diedre Gray - SVP and General Counsel - Post Holdings | LinkedIn",                  "url": "https://www.linkedin.com/in/diedregray-postholdings/"},
    {"title": "Todd Cunfer - SVP Chief HR Officer - Post Holdings | LinkedIn",                     "url": "https://www.linkedin.com/in/toddcunfer-postholdings/"},
    {"title": "Jeff Zadoks - SVP Operations - Post Holdings | LinkedIn",                           "url": "https://www.linkedin.com/in/jeffzadoks-postholdings/"},
    {"title": "Steve Erdahl - SVP and President Post Consumer Brands - Post Holdings | LinkedIn",  "url": "https://www.linkedin.com/in/steveerdahl-postholdings/"},
    {"title": "Josh Kanter - SVP Consumer Brands Strategy - Post Holdings | LinkedIn",             "url": "https://www.linkedin.com/in/joshkanter-postholdings/"},
    {"title": "Tom Day - SVP Private Label - Post Holdings | LinkedIn",                            "url": "https://www.linkedin.com/in/tomday-postholdings/"},
    {"title": "Jennifer Meyer - VP Investor Relations - Post Holdings | LinkedIn",                 "url": "https://www.linkedin.com/in/jennifermeyer-postholdings/"},
    {"title": "Bill Holton - SVP Strategy - Post Holdings | LinkedIn",                             "url": "https://www.linkedin.com/in/billholton-postholdings/"},
], min_required=3, max_keep=10))

print("AutoZone:", ingest_profiles("AutoZone", [
    {"title": "Bill Rhodes - Executive Chairman - AutoZone | LinkedIn",                            "url": "https://www.linkedin.com/in/billrhodes-autozone/"},
    {"title": "Phil Daniele - President and CEO - AutoZone | LinkedIn",                            "url": "https://www.linkedin.com/in/phildaniele-autozone/"},
    {"title": "Jamere Jackson - EVP and CFO - AutoZone | LinkedIn",                               "url": "https://www.linkedin.com/in/jamerejackson-autozone/"},
    {"title": "Tom Newbern - EVP and COO - AutoZone | LinkedIn",                                   "url": "https://www.linkedin.com/in/tomnewbern-autozone/"},
    {"title": "Brian Campbell - EVP Commercial - AutoZone | LinkedIn",                             "url": "https://www.linkedin.com/in/briancampbell-autozone/"},
    {"title": "Domingo Hurtado - EVP International - AutoZone | LinkedIn",                        "url": "https://www.linkedin.com/in/domingohurtado-autozone/"},
    {"title": "Gina Gargano - EVP Chief HR Officer - AutoZone | LinkedIn",                        "url": "https://www.linkedin.com/in/ginagargano-autozone/"},
    {"title": "Charlie Pleas - SVP Finance and Accounting - AutoZone | LinkedIn",                  "url": "https://www.linkedin.com/in/charliepleas-autozone/"},
    {"title": "Brian Hughes - VP Investor Relations - AutoZone | LinkedIn",                        "url": "https://www.linkedin.com/in/brianhughes-autozone/"},
    {"title": "Mark Finestone - EVP Merchandising - AutoZone | LinkedIn",                          "url": "https://www.linkedin.com/in/markfinestone-autozone/"},
], min_required=3, max_keep=10))

print("CarMax:", ingest_profiles("CarMax", [
    {"title": "Bill Nash - President and CEO - CarMax | LinkedIn",                                 "url": "https://www.linkedin.com/in/billnash-carmax/"},
    {"title": "Enrique Mayor-Mora - EVP and CFO - CarMax | LinkedIn",                             "url": "https://www.linkedin.com/in/enriquemayor-mora-carmax/"},
    {"title": "Jon Daniels - SVP CarMax Auto Finance - CarMax | LinkedIn",                         "url": "https://www.linkedin.com/in/jondaniels-carmax/"},
    {"title": "Jim Lyski - EVP Chief Marketing Officer - CarMax | LinkedIn",                       "url": "https://www.linkedin.com/in/jimlyski-carmax/"},
    {"title": "Shamim Mohammad - EVP Chief Information and Technology - CarMax | LinkedIn",        "url": "https://www.linkedin.com/in/shamimmohammad-carmax/"},
    {"title": "Diane Cafritz - EVP Chief People and Culture Officer - CarMax | LinkedIn",          "url": "https://www.linkedin.com/in/dianecafritz-carmax/"},
    {"title": "Cam Watson - EVP Customer Experience - CarMax | LinkedIn",                          "url": "https://www.linkedin.com/in/camwatson-carmax/"},
    {"title": "Lisa Callicutt - EVP Operations - CarMax | LinkedIn",                               "url": "https://www.linkedin.com/in/lisacallicutt-carmax/"},
    {"title": "Erin Winston - SVP General Counsel - CarMax | LinkedIn",                            "url": "https://www.linkedin.com/in/erinwinston-carmax/"},
    {"title": "Brian Davis - VP Investor Relations - CarMax | LinkedIn",                           "url": "https://www.linkedin.com/in/briandavis-carmax/"},
], min_required=3, max_keep=10))

print("Ryder System:", ingest_profiles("Ryder System", [
    {"title": "Robert Sanchez - Chairman and CEO - Ryder System | LinkedIn",                       "url": "https://www.linkedin.com/in/robertsanchez-ryder/"},
    {"title": "Cristina Gallo-Aquino - EVP and CFO - Ryder System | LinkedIn",                   "url": "https://www.linkedin.com/in/cristinagalloaquino-ryder/"},
    {"title": "Steve Martin - EVP and COO - Ryder System | LinkedIn",                             "url": "https://www.linkedin.com/in/stevemartin-ryder/"},
    {"title": "Tom Havens - EVP and President Fleet Management Solutions - Ryder | LinkedIn",      "url": "https://www.linkedin.com/in/tomhavens-ryder/"},
    {"title": "John Gleason - EVP Chief Sales Officer - Ryder System | LinkedIn",                  "url": "https://www.linkedin.com/in/johngleason-ryder/"},
    {"title": "John Frasco - EVP President Supply Chain Solutions - Ryder System | LinkedIn",     "url": "https://www.linkedin.com/in/johnfrasco-ryder/"},
    {"title": "Melissa Sander - SVP Chief HR Officer - Ryder System | LinkedIn",                  "url": "https://www.linkedin.com/in/melissasander-ryder/"},
    {"title": "Gene Goldenberg - EVP General Counsel - Ryder System | LinkedIn",                  "url": "https://www.linkedin.com/in/genegoldenberg-ryder/"},
    {"title": "Neal Bhatt - VP Investor Relations - Ryder System | LinkedIn",                     "url": "https://www.linkedin.com/in/nealbhatt-ryder/"},
    {"title": "Karen Jones - EVP and Chief Marketing Officer - Ryder System | LinkedIn",           "url": "https://www.linkedin.com/in/karenjones-ryder/"},
], min_required=3, max_keep=10))

print("CoStar Group:", ingest_profiles("CoStar Group", [
    {"title": "Andy Florance - Founder and CEO - CoStar Group | LinkedIn",                         "url": "https://www.linkedin.com/in/andyflorance-costar/"},
    {"title": "Scott Wheeler - EVP and CFO - CoStar Group | LinkedIn",                             "url": "https://www.linkedin.com/in/scottwheeler-costar/"},
    {"title": "Dave Goyer - EVP and President Apartments.com - CoStar Group | LinkedIn",           "url": "https://www.linkedin.com/in/davegoyer-costar/"},
    {"title": "Michael Klein - EVP and President CoStar - CoStar Group | LinkedIn",               "url": "https://www.linkedin.com/in/michaelklein-costar/"},
    {"title": "Josh Katz - EVP and President LoopNet - CoStar Group | LinkedIn",                  "url": "https://www.linkedin.com/in/joshkatz-costar/"},
    {"title": "Lisa Ruggles - EVP Chief HR Officer - CoStar Group | LinkedIn",                    "url": "https://www.linkedin.com/in/lisaruggles-costar/"},
    {"title": "Sanford Sacks - EVP General Counsel - CoStar Group | LinkedIn",                    "url": "https://www.linkedin.com/in/sanfordsacks-costar/"},
    {"title": "Jeff Crocker - EVP Sales - CoStar Group | LinkedIn",                               "url": "https://www.linkedin.com/in/jeffcrocker-costar/"},
    {"title": "Cyndi Dale - VP Investor Relations - CoStar Group | LinkedIn",                     "url": "https://www.linkedin.com/in/cyndidale-costar/"},
    {"title": "Chris Nassetta - Board Member - CoStar Group | LinkedIn",                           "url": "https://www.linkedin.com/in/chrisnassetta-costar/"},
], min_required=3, max_keep=10))

print("RPM International:", ingest_profiles("RPM International", [
    {"title": "Frank Sullivan - Chairman and CEO - RPM International | LinkedIn",                  "url": "https://www.linkedin.com/in/franksullivan-rpm/"},
    {"title": "Timothy Knavish - President and COO - RPM International | LinkedIn",               "url": "https://www.linkedin.com/in/timothyknavish-rpm/"},
    {"title": "Rusty Gordon - EVP and CFO - RPM International | LinkedIn",                        "url": "https://www.linkedin.com/in/rustygordon-rpm/"},
    {"title": "Edward Moore - SVP and General Counsel - RPM International | LinkedIn",            "url": "https://www.linkedin.com/in/edwardmoore-rpm/"},
    {"title": "Matt Ratajczak - SVP Chief HR Officer - RPM International | LinkedIn",             "url": "https://www.linkedin.com/in/mattratajczak-rpm/"},
    {"title": "Paul Hoogenboom - SVP Manufacturing - RPM International | LinkedIn",               "url": "https://www.linkedin.com/in/paulhoogenboom-rpm/"},
    {"title": "Janeen Kastner - SVP Corporate Communications - RPM International | LinkedIn",     "url": "https://www.linkedin.com/in/janeenkastner-rpm/"},
    {"title": "Barry Slifstein - VP Investor Relations - RPM International | LinkedIn",           "url": "https://www.linkedin.com/in/barryslifstein-rpm/"},
    {"title": "Mark Scharmann - VP Finance - RPM International | LinkedIn",                       "url": "https://www.linkedin.com/in/markscharmann-rpm/"},
    {"title": "Chris Hartmann - President Rust-Oleum - RPM International | LinkedIn",             "url": "https://www.linkedin.com/in/chrishartmann-rpm/"},
], min_required=3, max_keep=10))

print("Macys:", ingest_profiles("Macys", [
    {"title": "Tony Spring - Chairman and CEO - Macys Inc | LinkedIn",                             "url": "https://www.linkedin.com/in/tonyspring-macys/"},
    {"title": "Adrian Mitchell - EVP and CFO - Macys Inc | LinkedIn",                             "url": "https://www.linkedin.com/in/adrianmitchell-macys/"},
    {"title": "Nata Dvir - EVP Chief Merchandising Officer - Macys Inc | LinkedIn",               "url": "https://www.linkedin.com/in/natadvir-macys/"},
    {"title": "Marc Mastronardi - EVP Chief Stores Officer - Macys Inc | LinkedIn",               "url": "https://www.linkedin.com/in/marcmastronardi-macys/"},
    {"title": "Mirian Graddick-Weir - EVP Chief HR Officer - Macys Inc | LinkedIn",              "url": "https://www.linkedin.com/in/miriangraddickweir-macys/"},
    {"title": "Sharon Otterman - EVP Chief Marketing Officer - Macys Inc | LinkedIn",             "url": "https://www.linkedin.com/in/sharonotterman-macys/"},
    {"title": "Mark Stocker - EVP Chief Supply Chain Officer - Macys Inc | LinkedIn",             "url": "https://www.linkedin.com/in/markstocker-macys/"},
    {"title": "Patti Ongman - EVP Chief Merchandise Planning - Macys Inc | LinkedIn",             "url": "https://www.linkedin.com/in/pattiongman-macys/"},
    {"title": "Monika Dobreva - VP Investor Relations - Macys Inc | LinkedIn",                    "url": "https://www.linkedin.com/in/monikadobreva-macys/"},
    {"title": "Sara Rosenthal - SVP Bloomingdales - Macys Inc | LinkedIn",                        "url": "https://www.linkedin.com/in/sararosenthal-macys/"},
], min_required=3, max_keep=10))

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
personalize_once_per_company(
    campaign_id=campaign_id,
    sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1,
    company_domains=COMPANY_DOMAINS,
    template="bbs",
    max_contacts_per_company=10,
    exclude_contacted=True,
)

print("\n" + "="*60); print("STEP 5: Sending from eleynxiong@berkeley.edu"); print("="*60)
gmail = GmailClient(account="default")
conn_s = sqlite3.connect("outreach.db", timeout=60)
conn_s.row_factory = sqlite3.Row
conn_s.execute("PRAGMA foreign_keys=ON")
conn_s.execute("PRAGMA busy_timeout=60000")

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
    JOIN contacts  ct ON sr.contact_id  = ct.id
    JOIN companies co ON ct.company_id  = co.id
    JOIN personalized_messages pm ON sr.message_id = pm.id
    WHERE sr.campaign_id = ? AND sr.status = 'queued'
    ORDER BY co.name, ct.last_name
""", (campaign_id,)).fetchall()

print(f"  {len(rows)} emails queued — sending from eleynxiong@berkeley.edu...")

if not check_send_window(campaign_id=campaign_id):
    conn_s.close()
    sys.exit(0)

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
                sender_email="eleynxiong@berkeley.edu",
            )
            safe_exec(
                "UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=? WHERE id=?",
                (result["id"], result["threadId"], datetime.now().isoformat(), row["sr_id"]),
            )
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
print(f"\n{'='*60}")
print(f"DONE — {total_sent} sent, {total_failed} failed")
print(f"Campaign: {CAMPAIGN_NAME}")
print(f"{'='*60}")
