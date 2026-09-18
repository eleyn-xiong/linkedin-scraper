"""BBS Batch 4 — 15 new Fortune 500 companies, eleynxiong@berkeley.edu."""
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
    {"name": "Merck",                  "domain": "merck.com",         "industry": "Pharmaceuticals / Vaccines",               "email_pattern": "first.last"},
    {"name": "Eli Lilly",              "domain": "lilly.com",         "industry": "Pharmaceuticals / GLP-1 / Oncology",       "email_pattern": "first.last"},
    {"name": "AbbVie",                 "domain": "abbvie.com",        "industry": "Biopharmaceuticals / Immunology",          "email_pattern": "first.last"},
    {"name": "General Dynamics",       "domain": "gd.com",            "industry": "Defense / Aerospace / IT Services",        "email_pattern": "first.last"},
    {"name": "L3Harris Technologies",  "domain": "l3harris.com",      "industry": "Defense Electronics / Space / Cyber",      "email_pattern": "first.last"},
    {"name": "Medtronic",              "domain": "medtronic.com",     "industry": "Medical Devices / Cardiovascular / Neuro", "email_pattern": "first.last"},
    {"name": "Stryker",                "domain": "stryker.com",       "industry": "Medical Devices / Orthopedics / Robotics", "email_pattern": "first.last"},
    {"name": "Honeywell",              "domain": "honeywell.com",     "industry": "Industrial / Aerospace / Building Tech",   "email_pattern": "first.last"},
    {"name": "Caterpillar",            "domain": "cat.com",           "industry": "Construction / Mining Equipment",          "email_pattern": "first.last"},
    {"name": "GE Aerospace",           "domain": "geaerospace.com",   "industry": "Aviation Engines / Defense / Services",    "email_pattern": "first.last"},
    {"name": "Emerson Electric",       "domain": "emerson.com",       "industry": "Industrial Automation / Technology",       "email_pattern": "first.last"},
    {"name": "Illinois Tool Works",    "domain": "itw.com",           "industry": "Industrial Manufacturing / Components",    "email_pattern": "first.last"},
    {"name": "Eaton",                  "domain": "eaton.com",         "industry": "Power Management / Electrical Systems",    "email_pattern": "first.last"},
    {"name": "Parker Hannifin",        "domain": "parker.com",        "industry": "Motion & Control / Industrial Systems",    "email_pattern": "first.last"},
    {"name": "Amgen",                  "domain": "amgen.com",         "industry": "Biotechnology / Biopharmaceuticals",       "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 4 - June 2026"
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

print("Merck:", ingest_profiles("Merck", [
    {"title": "Robert Davis - Chairman and CEO - Merck | LinkedIn",                          "url": "https://www.linkedin.com/in/robert-davis-merck/"},
    {"title": "Caroline Litchfield - CFO - Merck | LinkedIn",                               "url": "https://www.linkedin.com/in/carolinelitchfield/"},
    {"title": "Dean Li - EVP Research and Chief Medical Officer - Merck | LinkedIn",         "url": "https://www.linkedin.com/in/deanli-merck/"},
    {"title": "Jennifer Zachary - EVP General Counsel - Merck | LinkedIn",                   "url": "https://www.linkedin.com/in/jenniferzachary/"},
    {"title": "Mike Nally - EVP Chief Marketing Officer - Merck | LinkedIn",                 "url": "https://www.linkedin.com/in/mikenally/"},
    {"title": "Sanat Chattopadhyay - EVP Manufacturing - Merck | LinkedIn",                  "url": "https://www.linkedin.com/in/sanatchattopadhyay/"},
    {"title": "Frank Clyburn - EVP Human Health - Merck | LinkedIn",                         "url": "https://www.linkedin.com/in/frankclyburn/"},
    {"title": "David Fredrickson - EVP Oncology - Merck | LinkedIn",                         "url": "https://www.linkedin.com/in/davidfredrickson-merck/"},
    {"title": "Chirfi Guindo - EVP Market Access - Merck | LinkedIn",                        "url": "https://www.linkedin.com/in/chirfiguindo/"},
    {"title": "Rick DeLong - SVP Pharmaceutical Sciences - Merck | LinkedIn",                "url": "https://www.linkedin.com/in/rickdelong-merck/"},
], min_required=3, max_keep=10))

print("Eli Lilly:", ingest_profiles("Eli Lilly", [
    {"title": "David Ricks - Chairman and CEO - Eli Lilly | LinkedIn",                       "url": "https://www.linkedin.com/in/davidricks/"},
    {"title": "Anat Hakim - SVP and General Counsel - Eli Lilly | LinkedIn",                 "url": "https://www.linkedin.com/in/anathakim/"},
    {"title": "Dan Skovronsky - EVP Chief Scientific Officer - Eli Lilly | LinkedIn",        "url": "https://www.linkedin.com/in/danskovronsky/"},
    {"title": "Anne White - EVP President Neuroscience - Eli Lilly | LinkedIn",              "url": "https://www.linkedin.com/in/annewhite-lilly/"},
    {"title": "Patrik Jonsson - EVP Cardiometabolic Health - Eli Lilly | LinkedIn",          "url": "https://www.linkedin.com/in/patrikjonsson-lilly/"},
    {"title": "Edgardo Hernandez - EVP Manufacturing - Eli Lilly | LinkedIn",                "url": "https://www.linkedin.com/in/edgardohernandez-lilly/"},
    {"title": "Melissa Barnes - EVP Human Resources - Eli Lilly | LinkedIn",                 "url": "https://www.linkedin.com/in/melissabarnes-lilly/"},
    {"title": "Ilya Yuffa - SVP President Lilly International - Eli Lilly | LinkedIn",       "url": "https://www.linkedin.com/in/ilyayuffa/"},
    {"title": "Jake Van Naarden - President Loxo Oncology - Eli Lilly | LinkedIn",           "url": "https://www.linkedin.com/in/jakevannaarden/"},
    {"title": "Andrew Adams - EVP President Oncology - Eli Lilly | LinkedIn",                "url": "https://www.linkedin.com/in/andrewadams-lilly/"},
], min_required=3, max_keep=10))

print("AbbVie:", ingest_profiles("AbbVie", [
    {"title": "Robert Michael - President and CEO - AbbVie | LinkedIn",                      "url": "https://www.linkedin.com/in/robertmichael-abbvie/"},
    {"title": "Scott Reents - Executive VP and CFO - AbbVie | LinkedIn",                     "url": "https://www.linkedin.com/in/scottreents/"},
    {"title": "Roopal Thakkar - Chief Medical Officer - AbbVie | LinkedIn",                  "url": "https://www.linkedin.com/in/roopalthakkar/"},
    {"title": "Timothy Richmond - EVP Chief HR Officer - AbbVie | LinkedIn",                 "url": "https://www.linkedin.com/in/timothyrichmond-abbvie/"},
    {"title": "Laura Schumacher - Vice Chairman - AbbVie | LinkedIn",                        "url": "https://www.linkedin.com/in/lauraschumacher-abbvie/"},
    {"title": "Jeffrey Stewart - EVP Commercial Operations US - AbbVie | LinkedIn",          "url": "https://www.linkedin.com/in/jeffreystewart-abbvie/"},
    {"title": "Thomas Hudson - SVP Research and Development - AbbVie | LinkedIn",            "url": "https://www.linkedin.com/in/thomashudson-abbvie/"},
    {"title": "Carrie Strom - SVP Global Aesthetics - AbbVie | LinkedIn",                   "url": "https://www.linkedin.com/in/carriestrom/"},
    {"title": "Matthew Nicolai - SVP Strategy and Corporate Development - AbbVie | LinkedIn","url": "https://www.linkedin.com/in/matthewnicolai/"},
    {"title": "Richard Gonzalez - Executive Chairman - AbbVie | LinkedIn",                   "url": "https://www.linkedin.com/in/richardgonzalez-abbvie/"},
], min_required=3, max_keep=10))

print("General Dynamics:", ingest_profiles("General Dynamics", [
    {"title": "Phebe Novakovic - Chairman and CEO - General Dynamics | LinkedIn",            "url": "https://www.linkedin.com/in/phebenovakovic/"},
    {"title": "Jason Aiken - EVP Finance and CFO - General Dynamics | LinkedIn",             "url": "https://www.linkedin.com/in/jasonaiken-gd/"},
    {"title": "Mark Roualet - EVP Marine Systems - General Dynamics | LinkedIn",             "url": "https://www.linkedin.com/in/markroualet/"},
    {"title": "Chris Brady - EVP Combat Systems - General Dynamics | LinkedIn",              "url": "https://www.linkedin.com/in/chrisbradygd/"},
    {"title": "Dave Heebner - EVP Aerospace - General Dynamics | LinkedIn",                  "url": "https://www.linkedin.com/in/daveheebner/"},
    {"title": "Chris Marzilli - EVP Technologies - General Dynamics | LinkedIn",             "url": "https://www.linkedin.com/in/chrismarzilli/"},
    {"title": "William Moss - Chief Legal Officer - General Dynamics | LinkedIn",            "url": "https://www.linkedin.com/in/williammoss-gd/"},
    {"title": "Kim Kuryea - SVP Human Resources - General Dynamics | LinkedIn",              "url": "https://www.linkedin.com/in/kimkuryea/"},
    {"title": "Rex Megna - SVP Corporate Development - General Dynamics | LinkedIn",         "url": "https://www.linkedin.com/in/rexmegna/"},
    {"title": "Dan Johnson - EVP Mission Systems - General Dynamics | LinkedIn",             "url": "https://www.linkedin.com/in/danjohnson-gd/"},
], min_required=3, max_keep=10))

print("L3Harris Technologies:", ingest_profiles("L3Harris Technologies", [
    {"title": "Christopher Kubasik - Chairman and CEO - L3Harris Technologies | LinkedIn",   "url": "https://www.linkedin.com/in/christopherkubasik/"},
    {"title": "Jesus Malave - CFO - L3Harris Technologies | LinkedIn",                       "url": "https://www.linkedin.com/in/jesusmalave/"},
    {"title": "Ed Zoiss - President Space and Airborne Systems - L3Harris | LinkedIn",       "url": "https://www.linkedin.com/in/edzoiss/"},
    {"title": "Sean Stackley - President Integrated Mission Systems - L3Harris | LinkedIn",  "url": "https://www.linkedin.com/in/seanstackley/"},
    {"title": "Todd West - President Communication Systems - L3Harris | LinkedIn",           "url": "https://www.linkedin.com/in/toddwest-l3harris/"},
    {"title": "Dana Mehnert - President Aviation Systems - L3Harris | LinkedIn",             "url": "https://www.linkedin.com/in/danamehnert/"},
    {"title": "Carolyn Debois - VP Human Resources - L3Harris | LinkedIn",                   "url": "https://www.linkedin.com/in/carolyndebois/"},
    {"title": "Jack Croft - VP General Counsel - L3Harris Technologies | LinkedIn",          "url": "https://www.linkedin.com/in/jackcroft-l3harris/"},
    {"title": "Russ Sharer - VP Strategy - L3Harris Technologies | LinkedIn",                "url": "https://www.linkedin.com/in/russsharer/"},
    {"title": "Zach Meyer - SVP Business Development - L3Harris | LinkedIn",                 "url": "https://www.linkedin.com/in/zachmeyer-l3harris/"},
], min_required=3, max_keep=10))

print("Medtronic:", ingest_profiles("Medtronic", [
    {"title": "Geoff Martha - Chairman and CEO - Medtronic | LinkedIn",                      "url": "https://www.linkedin.com/in/geoffmartha/"},
    {"title": "Karen Parkhill - EVP and CFO - Medtronic | LinkedIn",                         "url": "https://www.linkedin.com/in/karenparkhill/"},
    {"title": "Michael Marinaro - EVP President Americas - Medtronic | LinkedIn",            "url": "https://www.linkedin.com/in/michaelmarinaro/"},
    {"title": "Que Dallara - EVP President Cardiovascular - Medtronic | LinkedIn",           "url": "https://www.linkedin.com/in/quedallara/"},
    {"title": "Brett Wall - EVP President Neuroscience - Medtronic | LinkedIn",              "url": "https://www.linkedin.com/in/brettwall/"},
    {"title": "Thierry Piuz - EVP President Medical Surgical - Medtronic | LinkedIn",        "url": "https://www.linkedin.com/in/thierrypiuz/"},
    {"title": "Carol Surface - EVP Chief People Officer - Medtronic | LinkedIn",             "url": "https://www.linkedin.com/in/carolsurface/"},
    {"title": "Brad Lerman - EVP General Counsel - Medtronic | LinkedIn",                    "url": "https://www.linkedin.com/in/bradlerman/"},
    {"title": "Rob ten Hoedt - EVP President International - Medtronic | LinkedIn",          "url": "https://www.linkedin.com/in/robtenhoedt/"},
    {"title": "Lionel Carneiro - SVP Strategy - Medtronic | LinkedIn",                       "url": "https://www.linkedin.com/in/lionelcarneiro/"},
], min_required=3, max_keep=10))

print("Stryker:", ingest_profiles("Stryker", [
    {"title": "Kevin Lobo - Executive Chairman - Stryker | LinkedIn",                        "url": "https://www.linkedin.com/in/kevinlobo/"},
    {"title": "Glenn Boehnlein - VP and CFO - Stryker | LinkedIn",                           "url": "https://www.linkedin.com/in/glennboehnlein/"},
    {"title": "Timothy Scannell - COO - Stryker | LinkedIn",                                 "url": "https://www.linkedin.com/in/timothyscannell/"},
    {"title": "Kim Powell - Group President MedSurg and Neurotechnology - Stryker | LinkedIn","url": "https://www.linkedin.com/in/kimpowell-stryker/"},
    {"title": "Viju Menon - President Global Operations - Stryker | LinkedIn",               "url": "https://www.linkedin.com/in/vijumenon/"},
    {"title": "Katherine Owen - VP Strategy and Investor Relations - Stryker | LinkedIn",    "url": "https://www.linkedin.com/in/katherineowen-stryker/"},
    {"title": "Yin Becker - VP Chief Communications Officer - Stryker | LinkedIn",           "url": "https://www.linkedin.com/in/yinbecker/"},
    {"title": "Michelle James - VP General Counsel - Stryker | LinkedIn",                    "url": "https://www.linkedin.com/in/michellejames-stryker/"},
    {"title": "Brad Saar - President Neurotechnology - Stryker | LinkedIn",                  "url": "https://www.linkedin.com/in/bradsaar/"},
    {"title": "Ryan Gleason - VP HR - Stryker | LinkedIn",                                   "url": "https://www.linkedin.com/in/ryangleason-stryker/"},
], min_required=3, max_keep=10))

print("Honeywell:", ingest_profiles("Honeywell", [
    {"title": "Vimal Kapur - Chairman and CEO - Honeywell | LinkedIn",                       "url": "https://www.linkedin.com/in/vimalkapur/"},
    {"title": "Greg Lewis - SVP and CFO - Honeywell | LinkedIn",                             "url": "https://www.linkedin.com/in/greglewis-honeywell/"},
    {"title": "Anne Madden - SVP General Counsel - Honeywell | LinkedIn",                    "url": "https://www.linkedin.com/in/annemadden-honeywell/"},
    {"title": "Torsten Pilz - EVP Industrial Automation - Honeywell | LinkedIn",             "url": "https://www.linkedin.com/in/torstenpilz/"},
    {"title": "Mark James - President Aerospace Technologies - Honeywell | LinkedIn",        "url": "https://www.linkedin.com/in/markjames-honeywell/"},
    {"title": "Nefin Dincel - Chief HR Officer - Honeywell | LinkedIn",                      "url": "https://www.linkedin.com/in/nefindincel/"},
    {"title": "Michael Nefkens - President Building Automation - Honeywell | LinkedIn",      "url": "https://www.linkedin.com/in/michaelnefkens/"},
    {"title": "Jim Currier - President Performance Materials - Honeywell | LinkedIn",        "url": "https://www.linkedin.com/in/jimcurrier-honeywell/"},
    {"title": "Mike Markovitch - VP Chief Digital Technology Officer - Honeywell | LinkedIn","url": "https://www.linkedin.com/in/mikemarkovitch/"},
    {"title": "Que Dallara - Former VP Connected Enterprise - Honeywell | LinkedIn",         "url": "https://www.linkedin.com/in/quedallara/"},
], min_required=3, max_keep=10))

print("Caterpillar:", ingest_profiles("Caterpillar", [
    {"title": "Jim Umpleby - Chairman and CEO - Caterpillar | LinkedIn",                     "url": "https://www.linkedin.com/in/jimumpleby/"},
    {"title": "Andrew Bonfield - CFO - Caterpillar | LinkedIn",                              "url": "https://www.linkedin.com/in/andrewbonfield/"},
    {"title": "Joe Creed - Group President Energy and Transportation - Caterpillar | LinkedIn","url": "https://www.linkedin.com/in/joecreed-cat/"},
    {"title": "Tony Fassino - Group President Services and Digital - Caterpillar | LinkedIn","url": "https://www.linkedin.com/in/tonyfassino/"},
    {"title": "Ramin Younessi - Group President Construction Industries - Caterpillar | LinkedIn","url": "https://www.linkedin.com/in/raminyounessi/"},
    {"title": "Asha Varghese - Chief Digital Officer - Caterpillar | LinkedIn",              "url": "https://www.linkedin.com/in/ashavarghese/"},
    {"title": "Suzette Long - General Counsel - Caterpillar | LinkedIn",                     "url": "https://www.linkedin.com/in/suzettelong/"},
    {"title": "Stacy Loretz-Congdon - VP Human Resources - Caterpillar | LinkedIn",         "url": "https://www.linkedin.com/in/stacyloretzcongdon/"},
    {"title": "Rob Charter - VP Marketing and Digital - Caterpillar | LinkedIn",             "url": "https://www.linkedin.com/in/robcharter-cat/"},
    {"title": "Kyle Epley - VP North America Distribution Services - Caterpillar | LinkedIn","url": "https://www.linkedin.com/in/kyleepley/"},
], min_required=3, max_keep=10))

print("GE Aerospace:", ingest_profiles("GE Aerospace", [
    {"title": "H. Lawrence Culp Jr. - Chairman and CEO - GE Aerospace | LinkedIn",           "url": "https://www.linkedin.com/in/lawrenceculp/"},
    {"title": "Rahul Ghai - SVP and CFO - GE Aerospace | LinkedIn",                          "url": "https://www.linkedin.com/in/rahulghai/"},
    {"title": "Russell Stokes - President Commercial Engines and Services - GE Aerospace | LinkedIn","url": "https://www.linkedin.com/in/russellstokes-ge/"},
    {"title": "Mohamed Ali - President Global Services - GE Aerospace | LinkedIn",            "url": "https://www.linkedin.com/in/mohamedali-ge/"},
    {"title": "Jennifer Reed - EVP Chief Legal Officer - GE Aerospace | LinkedIn",            "url": "https://www.linkedin.com/in/jenniferreed-ge/"},
    {"title": "Eric Gebhardt - Chief Technology Officer - GE Aerospace | LinkedIn",           "url": "https://www.linkedin.com/in/ericgebhardt/"},
    {"title": "John Slattery - President Aerospace - GE Aerospace | LinkedIn",                "url": "https://www.linkedin.com/in/johnslattery-ge/"},
    {"title": "Shane Wright - SVP Supply Chain - GE Aerospace | LinkedIn",                    "url": "https://www.linkedin.com/in/shanewright-ge/"},
    {"title": "John Vilja - VP Human Resources - GE Aerospace | LinkedIn",                    "url": "https://www.linkedin.com/in/johnvilja/"},
    {"title": "Steve Bolze - Former President Power - GE Aerospace | LinkedIn",               "url": "https://www.linkedin.com/in/stevebolze/"},
], min_required=3, max_keep=10))

print("Emerson Electric:", ingest_profiles("Emerson Electric", [
    {"title": "Lal Karsanbhai - President and CEO - Emerson Electric | LinkedIn",            "url": "https://www.linkedin.com/in/lalkarsanbhai/"},
    {"title": "Mike Baughman - SVP and CFO - Emerson Electric | LinkedIn",                   "url": "https://www.linkedin.com/in/mikebaughman-emerson/"},
    {"title": "Ram Krishnan - COO - Emerson Electric | LinkedIn",                            "url": "https://www.linkedin.com/in/ramkrishnan-emerson/"},
    {"title": "Denise Cade - SVP General Counsel - Emerson Electric | LinkedIn",             "url": "https://www.linkedin.com/in/denisecade/"},
    {"title": "Vidya Ramnath - SVP Human Resources - Emerson Electric | LinkedIn",           "url": "https://www.linkedin.com/in/vidyaramnath/"},
    {"title": "Brian Walker - President Intelligent Devices - Emerson Electric | LinkedIn",  "url": "https://www.linkedin.com/in/brianwalker-emerson/"},
    {"title": "Axel Nordvall - Executive VP - Emerson Electric | LinkedIn",                   "url": "https://www.linkedin.com/in/axelnordvall/"},
    {"title": "Jake Gruber - SVP Strategy - Emerson Electric | LinkedIn",                    "url": "https://www.linkedin.com/in/jakegruber-emerson/"},
    {"title": "Randal Wells - Executive VP - Emerson Electric | LinkedIn",                   "url": "https://www.linkedin.com/in/randalwells-emerson/"},
    {"title": "Steve Pelch - SVP and COO - Emerson Electric | LinkedIn",                     "url": "https://www.linkedin.com/in/stevepelch/"},
], min_required=3, max_keep=10))

print("Illinois Tool Works:", ingest_profiles("Illinois Tool Works", [
    {"title": "Christopher O'Herlihy - Chairman and CEO - Illinois Tool Works | LinkedIn",   "url": "https://www.linkedin.com/in/christopherorherlihy/"},
    {"title": "Michael Larsen - SVP and CFO - Illinois Tool Works | LinkedIn",               "url": "https://www.linkedin.com/in/michaellarsen-itw/"},
    {"title": "Norman Finch Jr. - SVP General Counsel - Illinois Tool Works | LinkedIn",     "url": "https://www.linkedin.com/in/normanfinchjr/"},
    {"title": "Mary Beth Gustafsson - SVP Human Resources - Illinois Tool Works | LinkedIn", "url": "https://www.linkedin.com/in/marybethgustafsson/"},
    {"title": "Axel Nordvall - Executive VP - Illinois Tool Works | LinkedIn",               "url": "https://www.linkedin.com/in/axelnordvall-itw/"},
    {"title": "Randal Wells - Executive VP - Illinois Tool Works | LinkedIn",                "url": "https://www.linkedin.com/in/randalwells-itw/"},
    {"title": "Roland Martel - Executive VP - Illinois Tool Works | LinkedIn",               "url": "https://www.linkedin.com/in/rolandmartel/"},
    {"title": "Steven Martin - Executive VP - Illinois Tool Works | LinkedIn",               "url": "https://www.linkedin.com/in/stevenmartin-itw/"},
    {"title": "Sigrid Stjernvall - VP Investor Relations - Illinois Tool Works | LinkedIn",  "url": "https://www.linkedin.com/in/sigridstjernvall/"},
    {"title": "Michael Zimmerman - VP Corporate Finance - Illinois Tool Works | LinkedIn",   "url": "https://www.linkedin.com/in/michaelzimmerman-itw/"},
], min_required=3, max_keep=10))

print("Eaton:", ingest_profiles("Eaton", [
    {"title": "Craig Arnold - Chairman and CEO - Eaton | LinkedIn",                          "url": "https://www.linkedin.com/in/craigarnold-eaton/"},
    {"title": "Olivier Leonetti - EVP and CFO - Eaton | LinkedIn",                           "url": "https://www.linkedin.com/in/olivierleonetti/"},
    {"title": "Ted Crandall - President Electrical Americas - Eaton | LinkedIn",             "url": "https://www.linkedin.com/in/tedcrandall/"},
    {"title": "Uday Yadav - President Electrical Global - Eaton | LinkedIn",                 "url": "https://www.linkedin.com/in/udayyadav/"},
    {"title": "Bharat Bhushan - EVP and CTO - Eaton | LinkedIn",                             "url": "https://www.linkedin.com/in/bharatbhushan-eaton/"},
    {"title": "Taras Szmagala Jr. - SVP Chief Legal Officer - Eaton | LinkedIn",             "url": "https://www.linkedin.com/in/tarasszmagala/"},
    {"title": "Phillip Simons - Chief People Officer - Eaton | LinkedIn",                    "url": "https://www.linkedin.com/in/phillipsimons-eaton/"},
    {"title": "Heath Monesmith - President Industrial Sector - Eaton | LinkedIn",            "url": "https://www.linkedin.com/in/heathmonesmith/"},
    {"title": "Paulo Ruiz - EVP President Electrical Global - Eaton | LinkedIn",             "url": "https://www.linkedin.com/in/pauloruiz-eaton/"},
    {"title": "Tom Gross - VP Investor Relations - Eaton | LinkedIn",                        "url": "https://www.linkedin.com/in/tomgross-eaton/"},
], min_required=3, max_keep=10))

print("Parker Hannifin:", ingest_profiles("Parker Hannifin", [
    {"title": "Jenny Parmentier - President and CEO - Parker Hannifin | LinkedIn",           "url": "https://www.linkedin.com/in/jennyparmentier/"},
    {"title": "Todd Leombruno - VP and CFO - Parker Hannifin | LinkedIn",                    "url": "https://www.linkedin.com/in/toddleombruno/"},
    {"title": "Bernadette Wightman - President Engineered Materials - Parker Hannifin | LinkedIn","url": "https://www.linkedin.com/in/bernadettewightman/"},
    {"title": "Olivier Ghesquiere - President Aerospace Systems - Parker Hannifin | LinkedIn","url": "https://www.linkedin.com/in/olivierghesquiere/"},
    {"title": "Andrew Ross - VP Human Resources - Parker Hannifin | LinkedIn",               "url": "https://www.linkedin.com/in/andrewross-parker/"},
    {"title": "Joe Leonti - VP General Counsel - Parker Hannifin | LinkedIn",                "url": "https://www.linkedin.com/in/joeleonti/"},
    {"title": "Roland Bohde - President Diversified Industrial - Parker Hannifin | LinkedIn","url": "https://www.linkedin.com/in/rolandbohde/"},
    {"title": "Lee Banks - Vice Chairman - Parker Hannifin | LinkedIn",                      "url": "https://www.linkedin.com/in/leebanks-parker/"},
    {"title": "Marcia Gresko - VP Finance - Parker Hannifin | LinkedIn",                     "url": "https://www.linkedin.com/in/marciagresko/"},
    {"title": "Richie Cara - VP Corporate Treasury - Parker Hannifin | LinkedIn",            "url": "https://www.linkedin.com/in/richiecara/"},
], min_required=3, max_keep=10))

print("Amgen:", ingest_profiles("Amgen", [
    {"title": "Robert Bradway - Chairman and CEO - Amgen | LinkedIn",                        "url": "https://www.linkedin.com/in/robertbradway/"},
    {"title": "Peter Griffith - EVP and CFO - Amgen | LinkedIn",                             "url": "https://www.linkedin.com/in/petergriffith-amgen/"},
    {"title": "David Reese - EVP Research and Development - Amgen | LinkedIn",               "url": "https://www.linkedin.com/in/davidreese-amgen/"},
    {"title": "Murdo Gordon - EVP Global Commercial Operations - Amgen | LinkedIn",          "url": "https://www.linkedin.com/in/murdogordon/"},
    {"title": "Jay Bradner - EVP Research - Amgen | LinkedIn",                               "url": "https://www.linkedin.com/in/jaybradner/"},
    {"title": "Esteban Santos - EVP Global Operations - Amgen | LinkedIn",                   "url": "https://www.linkedin.com/in/estebansantos-amgen/"},
    {"title": "Jonathan Graham - EVP General Counsel - Amgen | LinkedIn",                    "url": "https://www.linkedin.com/in/jonathangraham-amgen/"},
    {"title": "Lori Johnston - EVP Chief HR Officer - Amgen | LinkedIn",                     "url": "https://www.linkedin.com/in/lorijohnston-amgen/"},
    {"title": "Vikram Karnani - EVP Commercial - Amgen | LinkedIn",                          "url": "https://www.linkedin.com/in/vikramkarnani/"},
    {"title": "James Bradner - EVP Research and Innovation - Amgen | LinkedIn",              "url": "https://www.linkedin.com/in/jamesbradner/"},
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
        print(f"  [+] Created: {CAMPAIGN_NAME} ({campaign_id})")

with open("CAMPAIGN_ID.txt", "w") as f:
    f.write(campaign_id)

# ── Personalize ───────────────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing — BBS template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="bbs",
    max_contacts_per_company=10, exclude_contacted=True)

# ── Send ──────────────────────────────────────────────────────────────────────
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
