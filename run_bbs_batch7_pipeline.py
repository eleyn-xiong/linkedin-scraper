"""BBS Batch 7 — 25 new Fortune 500 companies, 10 emails each, eleynxiong@berkeley.edu."""
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
    {"name": "Progressive Insurance",   "domain": "progressive.com",       "industry": "Auto / Property / Casualty Insurance",              "email_pattern": "first.last"},
    {"name": "Aon",                      "domain": "aon.com",               "industry": "Insurance / Risk / Consulting / HR Solutions",      "email_pattern": "first.last"},
    {"name": "Marsh McLennan",           "domain": "marshmclennan.com",     "industry": "Risk / Insurance Brokerage / HR Consulting",        "email_pattern": "first.last"},
    {"name": "Kimberly-Clark",           "domain": "kimberly-clark.com",    "industry": "Consumer Goods / Personal Care / Healthcare",       "email_pattern": "first.last"},
    {"name": "Estee Lauder",             "domain": "elcompanies.com",       "industry": "Beauty / Skincare / Fragrance / Cosmetics",        "email_pattern": "first.last"},
    {"name": "Hasbro",                   "domain": "hasbro.com",            "industry": "Toys / Entertainment / Gaming / Consumer",         "email_pattern": "first.last"},
    {"name": "Molina Healthcare",        "domain": "molinahealthcare.com",  "industry": "Managed Care / Medicaid / Medicare / Health Plans","email_pattern": "first.last"},
    {"name": "Quest Diagnostics",        "domain": "questdiagnostics.com",  "industry": "Diagnostics / Lab Testing / Healthcare",           "email_pattern": "first.last"},
    {"name": "Labcorp",                  "domain": "labcorp.com",           "industry": "Clinical Lab / Drug Development / Genomics",       "email_pattern": "first.last"},
    {"name": "Baxter International",     "domain": "baxter.com",            "industry": "Medical Devices / Renal / Hospital Products",      "email_pattern": "first.last"},
    {"name": "KLA Corporation",          "domain": "kla.com",               "industry": "Semiconductor Equipment / Process Control",        "email_pattern": "first.last"},
    {"name": "Marvell Technology",       "domain": "marvell.com",           "industry": "Semiconductor / Data Infrastructure / 5G / Cloud", "email_pattern": "first.last"},
    {"name": "ON Semiconductor",         "domain": "onsemi.com",            "industry": "Semiconductor / Power Management / Automotive",    "email_pattern": "first.last"},
    {"name": "TE Connectivity",          "domain": "te.com",                "industry": "Electronic Components / Sensors / Connectivity",   "email_pattern": "first.last"},
    {"name": "Amphenol",                 "domain": "amphenol.com",          "industry": "Electronic Connectors / Sensors / Antennas",       "email_pattern": "first.last"},
    {"name": "Cummins",                  "domain": "cummins.com",           "industry": "Engines / Power / Filtration / Electrification",   "email_pattern": "first.last"},
    {"name": "Fortive",                  "domain": "fortive.com",           "industry": "Industrial Technology / Software / Healthcare",    "email_pattern": "first.last"},
    {"name": "Roper Technologies",       "domain": "ropertech.com",         "industry": "Diversified Industrial / Software / SaaS",        "email_pattern": "first.last"},
    {"name": "W.W. Grainger",            "domain": "grainger.com",          "industry": "Industrial Distribution / MRO / Supply Chain",    "email_pattern": "first.last"},
    {"name": "Dollar Tree",              "domain": "dollartree.com",        "industry": "Discount Retail / Value Retail / Consumer",        "email_pattern": "first.last"},
    {"name": "Ross Stores",              "domain": "rossstores.com",        "industry": "Off-Price Retail / Apparel / Home",               "email_pattern": "first.last"},
    {"name": "Nordstrom",                "domain": "nordstrom.com",         "industry": "Department Store / Fashion Retail / E-Commerce",   "email_pattern": "first.last"},
    {"name": "Waste Management",         "domain": "wm.com",                "industry": "Environmental Services / Recycling / Sustainability","email_pattern": "first.last"},
    {"name": "Republic Services",        "domain": "republicservices.com",  "industry": "Environmental Services / Waste / Recycling",       "email_pattern": "first.last"},
    {"name": "IQVIA",                    "domain": "iqvia.com",             "industry": "Healthcare Data / Clinical Research / Analytics",  "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 7 - July 2026"
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

print("Progressive Insurance:", ingest_profiles("Progressive Insurance", [
    {"title": "Tricia Griffith - President and CEO - Progressive Insurance | LinkedIn",             "url": "https://www.linkedin.com/in/tricia-griffith-progressive/"},
    {"title": "John Sauerland - Vice Chairman and CFO - Progressive Insurance | LinkedIn",          "url": "https://www.linkedin.com/in/johnsauerland/"},
    {"title": "Patrick Callahan - President Personal Lines - Progressive Insurance | LinkedIn",     "url": "https://www.linkedin.com/in/patrickcallahan-progressive/"},
    {"title": "Karen Bailo - President Commercial Lines - Progressive Insurance | LinkedIn",        "url": "https://www.linkedin.com/in/karenbailo/"},
    {"title": "M. Jeffrey Charney - Chief Marketing Officer - Progressive Insurance | LinkedIn",    "url": "https://www.linkedin.com/in/jeffcharney/"},
    {"title": "Lori Niederst - Chief Human Resource Officer - Progressive Insurance | LinkedIn",    "url": "https://www.linkedin.com/in/lori-niederst/"},
    {"title": "Daniel Mascaro - Chief Legal Officer - Progressive Insurance | LinkedIn",            "url": "https://www.linkedin.com/in/danielmascaro-progressive/"},
    {"title": "Andrew Quigg - Chief Strategy Officer - Progressive Insurance | LinkedIn",           "url": "https://www.linkedin.com/in/andrewquigg-progressive/"},
    {"title": "Susan Griffith - Chief Information Officer - Progressive Insurance | LinkedIn",      "url": "https://www.linkedin.com/in/susangriffith-progressive/"},
    {"title": "Steve Broz - Chief Information Officer - Progressive Insurance | LinkedIn",          "url": "https://www.linkedin.com/in/stevebroz-progressive/"},
], min_required=3, max_keep=10))

print("Aon:", ingest_profiles("Aon", [
    {"title": "Greg Case - CEO - Aon | LinkedIn",                                                   "url": "https://www.linkedin.com/in/gregcase/"},
    {"title": "Christa Davies - EVP and CFO - Aon | LinkedIn",                                     "url": "https://www.linkedin.com/in/christadavies/"},
    {"title": "Eric Andersen - President - Aon | LinkedIn",                                        "url": "https://www.linkedin.com/in/ericandersen-aon/"},
    {"title": "Lamberto Andreotti - Board Director - Aon | LinkedIn",                               "url": "https://www.linkedin.com/in/lamberto-andreotti/"},
    {"title": "Lisa Stevens - Chief People Officer - Aon | LinkedIn",                               "url": "https://www.linkedin.com/in/lisa-stevens-aon/"},
    {"title": "Adam Messer - Chief Technology Officer - Aon | LinkedIn",                            "url": "https://www.linkedin.com/in/adammesser-aon/"},
    {"title": "Mindy Simon - Chief Operating Officer - Aon | LinkedIn",                             "url": "https://www.linkedin.com/in/mindysimon-aon/"},
    {"title": "Julie Page - CEO UK - Aon | LinkedIn",                                               "url": "https://www.linkedin.com/in/juliepage-aon/"},
    {"title": "Russ Johnston - CEO Reinsurance Solutions - Aon | LinkedIn",                         "url": "https://www.linkedin.com/in/russjohnston-aon/"},
    {"title": "Cara Carmichael - VP Sustainability - Aon | LinkedIn",                               "url": "https://www.linkedin.com/in/caracarmichael-aon/"},
], min_required=3, max_keep=10))

print("Marsh McLennan:", ingest_profiles("Marsh McLennan", [
    {"title": "John Doyle - President and CEO - Marsh McLennan | LinkedIn",                        "url": "https://www.linkedin.com/in/johndoyle-marshmclennan/"},
    {"title": "Mark McGivney - EVP and CFO - Marsh McLennan | LinkedIn",                           "url": "https://www.linkedin.com/in/markmcgivney/"},
    {"title": "Martin South - President and CEO Marsh - Marsh McLennan | LinkedIn",                "url": "https://www.linkedin.com/in/martinsouth-marsh/"},
    {"title": "Dean Klisura - President and CEO Guy Carpenter - Marsh McLennan | LinkedIn",        "url": "https://www.linkedin.com/in/deanklisura/"},
    {"title": "Pat Tomlinson - President and CEO Mercer - Marsh McLennan | LinkedIn",              "url": "https://www.linkedin.com/in/pattomlinson-mercer/"},
    {"title": "Nick Studer - President and CEO Oliver Wyman - Marsh McLennan | LinkedIn",          "url": "https://www.linkedin.com/in/nickstuder-owg/"},
    {"title": "Carmen Fariña - Chief People Officer - Marsh McLennan | LinkedIn",                  "url": "https://www.linkedin.com/in/carmenfarina-mmc/"},
    {"title": "Katherine Dobel - Chief Legal Officer - Marsh McLennan | LinkedIn",                 "url": "https://www.linkedin.com/in/kathdobel/"},
    {"title": "Martine Ferland - Former President Mercer - Marsh McLennan | LinkedIn",             "url": "https://www.linkedin.com/in/martineferland/"},
    {"title": "Peter Hearn - EVP - Marsh McLennan | LinkedIn",                                     "url": "https://www.linkedin.com/in/peterhearn-mmc/"},
], min_required=3, max_keep=10))

print("Kimberly-Clark:", ingest_profiles("Kimberly-Clark", [
    {"title": "Mike Hsu - Chairman and CEO - Kimberly-Clark | LinkedIn",                           "url": "https://www.linkedin.com/in/mikehsu-kc/"},
    {"title": "Nelson Urdaneta - SVP and CFO - Kimberly-Clark | LinkedIn",                         "url": "https://www.linkedin.com/in/nelsonurdaneta/"},
    {"title": "Alison Lewis - Chief Growth Officer - Kimberly-Clark | LinkedIn",                   "url": "https://www.linkedin.com/in/alisonlewis-kc/"},
    {"title": "Zack Hicks - Chief Digital and Technology Officer - Kimberly-Clark | LinkedIn",     "url": "https://www.linkedin.com/in/zachickhicks/"},
    {"title": "Sandra MacQuillan - Chief Supply Chain Officer - Kimberly-Clark | LinkedIn",        "url": "https://www.linkedin.com/in/sandramacquillan/"},
    {"title": "Tamera Bhatt - Chief Human Resources Officer - Kimberly-Clark | LinkedIn",          "url": "https://www.linkedin.com/in/tamerabhatt/"},
    {"title": "Darlene Fuller - Chief Legal Officer - Kimberly-Clark | LinkedIn",                  "url": "https://www.linkedin.com/in/darlenefuller-kc/"},
    {"title": "Michael Heltzer - EVP North America Commercial - Kimberly-Clark | LinkedIn",        "url": "https://www.linkedin.com/in/michaelheltzer/"},
    {"title": "Nathalie Roos - President International Family Care - Kimberly-Clark | LinkedIn",   "url": "https://www.linkedin.com/in/nathalieroos-kc/"},
    {"title": "Ram Krishnamurthy - Chief R&D Officer - Kimberly-Clark | LinkedIn",                 "url": "https://www.linkedin.com/in/ramkrishnamurthy-kc/"},
], min_required=3, max_keep=10))

print("Estee Lauder:", ingest_profiles("Estee Lauder", [
    {"title": "Stephane de La Faverie - President and CEO - Estee Lauder Companies | LinkedIn",    "url": "https://www.linkedin.com/in/stephanedelafaverie/"},
    {"title": "Tracey Travis - EVP and CFO - Estee Lauder Companies | LinkedIn",                   "url": "https://www.linkedin.com/in/traceytravis/"},
    {"title": "Chris Good - Group President Asia Pacific - Estee Lauder Companies | LinkedIn",     "url": "https://www.linkedin.com/in/chrisgood-elc/"},
    {"title": "Deirdre Stanley - EVP General Counsel - Estee Lauder Companies | LinkedIn",         "url": "https://www.linkedin.com/in/deirdrestanley/"},
    {"title": "Michael O'Hare - EVP Chief Human Resources Officer - Estee Lauder | LinkedIn",     "url": "https://www.linkedin.com/in/michaelohare-elc/"},
    {"title": "Jane Lauder - EVP Enterprise Marketing and Chief Data Officer - ELC | LinkedIn",    "url": "https://www.linkedin.com/in/janelauder/"},
    {"title": "Gregory Polcer - EVP Global Supply Chain - Estee Lauder Companies | LinkedIn",     "url": "https://www.linkedin.com/in/gregorypolcer/"},
    {"title": "Sarah Crespo - President EMEA - Estee Lauder Companies | LinkedIn",                "url": "https://www.linkedin.com/in/sarahcrespo-elc/"},
    {"title": "Peter Jueptner - Group President International - Estee Lauder Companies | LinkedIn","url": "https://www.linkedin.com/in/peterjueptner/"},
    {"title": "Cedric Prouve - Group President International - Estee Lauder Companies | LinkedIn", "url": "https://www.linkedin.com/in/cedricprouve/"},
], min_required=3, max_keep=10))

print("Hasbro:", ingest_profiles("Hasbro", [
    {"title": "Chris Cocks - CEO - Hasbro | LinkedIn",                                             "url": "https://www.linkedin.com/in/chriscocks-hasbro/"},
    {"title": "Gina Goetter - EVP and CFO - Hasbro | LinkedIn",                                    "url": "https://www.linkedin.com/in/ginagoetter/"},
    {"title": "Cynthia Williams - President Wizards of the Coast - Hasbro | LinkedIn",             "url": "https://www.linkedin.com/in/cynthiawilliams-hasbro/"},
    {"title": "Darren Throop - CEO eOne - Hasbro | LinkedIn",                                      "url": "https://www.linkedin.com/in/darrenthroop/"},
    {"title": "Laurel Thielen - Chief People Officer - Hasbro | LinkedIn",                         "url": "https://www.linkedin.com/in/laurelthielen-hasbro/"},
    {"title": "Tarrant Rockwood - Chief Legal Officer - Hasbro | LinkedIn",                        "url": "https://www.linkedin.com/in/tarrantrockwood/"},
    {"title": "Eric Nyman - President Consumer Products - Hasbro | LinkedIn",                      "url": "https://www.linkedin.com/in/ericnyman-hasbro/"},
    {"title": "Stephanie Wissink - VP Investor Relations - Hasbro | LinkedIn",                     "url": "https://www.linkedin.com/in/stephaniewissink/"},
    {"title": "Casey Collins - Chief Commercial Officer - Hasbro | LinkedIn",                      "url": "https://www.linkedin.com/in/caseycollins-hasbro/"},
    {"title": "Tim Kilpin - President Toy and Consumer Products - Hasbro | LinkedIn",              "url": "https://www.linkedin.com/in/timkilpin/"},
], min_required=3, max_keep=10))

print("Molina Healthcare:", ingest_profiles("Molina Healthcare", [
    {"title": "Joe Zubretsky - President and CEO - Molina Healthcare | LinkedIn",                  "url": "https://www.linkedin.com/in/joezubretsky/"},
    {"title": "Mark Keim - EVP and CFO - Molina Healthcare | LinkedIn",                            "url": "https://www.linkedin.com/in/markkeim-molina/"},
    {"title": "Jeff Barlow - SVP and General Counsel - Molina Healthcare | LinkedIn",              "url": "https://www.linkedin.com/in/jeffbarlow-molina/"},
    {"title": "Lori Schumacher - Chief Human Resources Officer - Molina Healthcare | LinkedIn",    "url": "https://www.linkedin.com/in/lorischumacher-molina/"},
    {"title": "Craig Samitt - Chief Clinical Officer - Molina Healthcare | LinkedIn",              "url": "https://www.linkedin.com/in/craigsamitt/"},
    {"title": "James Woys - EVP Health Plan Operations - Molina Healthcare | LinkedIn",            "url": "https://www.linkedin.com/in/jameswoys/"},
    {"title": "Joseph White - SVP and Chief Accounting Officer - Molina Healthcare | LinkedIn",    "url": "https://www.linkedin.com/in/josephwhite-molina/"},
    {"title": "Ritu Bhargava - SVP and CIO - Molina Healthcare | LinkedIn",                        "url": "https://www.linkedin.com/in/ritubhargava-molina/"},
    {"title": "Garrick Stoldt - SVP Medicaid - Molina Healthcare | LinkedIn",                      "url": "https://www.linkedin.com/in/garrickstoldt/"},
    {"title": "Cindy Wakefield - SVP Marketing and Communications - Molina Healthcare | LinkedIn", "url": "https://www.linkedin.com/in/cindywakefield-molina/"},
], min_required=3, max_keep=10))

print("Quest Diagnostics:", ingest_profiles("Quest Diagnostics", [
    {"title": "Jim Davis - Chairman President and CEO - Quest Diagnostics | LinkedIn",              "url": "https://www.linkedin.com/in/jimdavis-questdiagnostics/"},
    {"title": "Sam Samad - EVP and CFO - Quest Diagnostics | LinkedIn",                            "url": "https://www.linkedin.com/in/samsamad/"},
    {"title": "Shawn Bevec - EVP Physician and Consumer Solutions - Quest Diagnostics | LinkedIn", "url": "https://www.linkedin.com/in/shawnbevec/"},
    {"title": "Cathleen Bigos - EVP Hospital and Health System Solutions - Quest | LinkedIn",      "url": "https://www.linkedin.com/in/cathleenbigos-quest/"},
    {"title": "James Davis - Chief Medical Officer - Quest Diagnostics | LinkedIn",                "url": "https://www.linkedin.com/in/jamesdavis-quest-cmo/"},
    {"title": "Wendy Bost - EVP Corporate Communications - Quest Diagnostics | LinkedIn",          "url": "https://www.linkedin.com/in/wendybost/"},
    {"title": "Michelle Pennington - EVP Chief People Officer - Quest Diagnostics | LinkedIn",     "url": "https://www.linkedin.com/in/michellepennington-quest/"},
    {"title": "M. Darlene Solomon - EVP Chief Innovation Officer - Quest Diagnostics | LinkedIn",  "url": "https://www.linkedin.com/in/darlenesolomon/"},
    {"title": "Carrie Eglinton - EVP and General Counsel - Quest Diagnostics | LinkedIn",          "url": "https://www.linkedin.com/in/carrieeglinton/"},
    {"title": "Steven Rusckowski - Former CEO - Quest Diagnostics | LinkedIn",                     "url": "https://www.linkedin.com/in/stevenrusckowski/"},
], min_required=3, max_keep=10))

print("Labcorp:", ingest_profiles("Labcorp", [
    {"title": "Adam Schechter - Chairman and CEO - Labcorp | LinkedIn",                            "url": "https://www.linkedin.com/in/adamschechter/"},
    {"title": "Glenn Eisenberg - EVP and CFO - Labcorp | LinkedIn",                                "url": "https://www.linkedin.com/in/glenneisenberg/"},
    {"title": "Brian Caveney - EVP and Chief Medical Officer - Labcorp | LinkedIn",                "url": "https://www.linkedin.com/in/briancaveney/"},
    {"title": "Sandra van der Vaart - EVP General Counsel - Labcorp | LinkedIn",                   "url": "https://www.linkedin.com/in/sandravandervaart-labcorp/"},
    {"title": "Michele Mayes - EVP Chief People Officer - Labcorp | LinkedIn",                     "url": "https://www.linkedin.com/in/michelemayes-labcorp/"},
    {"title": "Jill Barker - EVP President Diagnostics - Labcorp | LinkedIn",                      "url": "https://www.linkedin.com/in/jillbarker-labcorp/"},
    {"title": "Erin Olszewski - EVP Investor Relations - Labcorp | LinkedIn",                      "url": "https://www.linkedin.com/in/erinolszewski-labcorp/"},
    {"title": "Nathalie Anderson - EVP Marketing and Communications - Labcorp | LinkedIn",         "url": "https://www.linkedin.com/in/nathalieanderson-labcorp/"},
    {"title": "Michael Greenberg - EVP Chief Strategy Officer - Labcorp | LinkedIn",               "url": "https://www.linkedin.com/in/michaelgreenberg-labcorp/"},
    {"title": "Scott Frommer - EVP Chief Information Officer - Labcorp | LinkedIn",                "url": "https://www.linkedin.com/in/scottfrommer-labcorp/"},
], min_required=3, max_keep=10))

print("Baxter International:", ingest_profiles("Baxter International", [
    {"title": "Jose Almeida - Chairman President and CEO - Baxter International | LinkedIn",       "url": "https://www.linkedin.com/in/josealmeida-baxter/"},
    {"title": "Joel Grade - EVP and CFO - Baxter International | LinkedIn",                        "url": "https://www.linkedin.com/in/joelgrade/"},
    {"title": "Christopher Toth - President Hospital Products - Baxter International | LinkedIn",  "url": "https://www.linkedin.com/in/christophertoth-baxter/"},
    {"title": "David Pirner - EVP and General Counsel - Baxter International | LinkedIn",          "url": "https://www.linkedin.com/in/davidpirner-baxter/"},
    {"title": "Anna Segovia - EVP Chief HR Officer - Baxter International | LinkedIn",             "url": "https://www.linkedin.com/in/annasegovia-baxter/"},
    {"title": "Paul Martin - EVP Chief Supply Chain - Baxter International | LinkedIn",            "url": "https://www.linkedin.com/in/paulmartin-baxter/"},
    {"title": "Alok Sonig - EVP President Kidney Care - Baxter International | LinkedIn",         "url": "https://www.linkedin.com/in/aloksonig/"},
    {"title": "Amy Stalzer - VP Investor Relations - Baxter International | LinkedIn",             "url": "https://www.linkedin.com/in/amystalzer-baxter/"},
    {"title": "Jeff Warren - EVP President Pharmaceuticals - Baxter International | LinkedIn",     "url": "https://www.linkedin.com/in/jeffwarren-baxter/"},
    {"title": "Heather Knight - SVP Corporate Communications - Baxter International | LinkedIn",   "url": "https://www.linkedin.com/in/heatherknight-baxter/"},
], min_required=3, max_keep=10))

print("KLA Corporation:", ingest_profiles("KLA Corporation", [
    {"title": "Rick Wallace - President and CEO - KLA Corporation | LinkedIn",                     "url": "https://www.linkedin.com/in/rickwallace-kla/"},
    {"title": "Bren Higgins - EVP and CFO - KLA Corporation | LinkedIn",                           "url": "https://www.linkedin.com/in/brenhiggins/"},
    {"title": "Ahmad Khan - President Semiconductor Process Control - KLA Corporation | LinkedIn", "url": "https://www.linkedin.com/in/ahmadkhan-kla/"},
    {"title": "Oreste Donzella - EVP Services and Emerging Markets - KLA Corporation | LinkedIn",  "url": "https://www.linkedin.com/in/orestedonzella/"},
    {"title": "Mary Humiston - SVP Global HR - KLA Corporation | LinkedIn",                        "url": "https://www.linkedin.com/in/maryhumiston-kla/"},
    {"title": "Brian Lorig - SVP Corporate Development and Strategy - KLA | LinkedIn",             "url": "https://www.linkedin.com/in/brianlorig-kla/"},
    {"title": "Kevin Kessel - VP Investor Relations - KLA Corporation | LinkedIn",                 "url": "https://www.linkedin.com/in/kevinkessel-kla/"},
    {"title": "Maciek Wojtkowski - CTO - KLA Corporation | LinkedIn",                              "url": "https://www.linkedin.com/in/maciekwojtkowski-kla/"},
    {"title": "Pam Johnson - SVP General Counsel - KLA Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/pamjohnson-kla/"},
    {"title": "Timothy Archer - Former CEO - KLA Corporation | LinkedIn",                          "url": "https://www.linkedin.com/in/timothyarcher-kla/"},
], min_required=3, max_keep=10))

print("Marvell Technology:", ingest_profiles("Marvell Technology", [
    {"title": "Matt Murphy - President and CEO - Marvell Technology | LinkedIn",                   "url": "https://www.linkedin.com/in/mattmurphy-marvell/"},
    {"title": "Willem Meintjes - SVP and CFO - Marvell Technology | LinkedIn",                     "url": "https://www.linkedin.com/in/willemmeintjes/"},
    {"title": "Chris Koopmans - EVP and COO - Marvell Technology | LinkedIn",                      "url": "https://www.linkedin.com/in/chriskoopmans-marvell/"},
    {"title": "Raghib Hussain - President Products and Technologies - Marvell Technology | LinkedIn","url": "https://www.linkedin.com/in/raghib-hussain/"},
    {"title": "Nitin Kasbekar - EVP Cloud Business - Marvell Technology | LinkedIn",               "url": "https://www.linkedin.com/in/nitinkasbekar/"},
    {"title": "Steve Greer - SVP Automotive and Industrial - Marvell Technology | LinkedIn",       "url": "https://www.linkedin.com/in/stevegreer-marvell/"},
    {"title": "Mauli Mehta - SVP Chief HR Officer - Marvell Technology | LinkedIn",                "url": "https://www.linkedin.com/in/maulimehta-marvell/"},
    {"title": "James Laufman - SVP General Counsel - Marvell Technology | LinkedIn",               "url": "https://www.linkedin.com/in/jameslaufman/"},
    {"title": "Tyler Melling - SVP Corporate Development - Marvell Technology | LinkedIn",         "url": "https://www.linkedin.com/in/tylermelling-marvell/"},
    {"title": "Ashish Saran - VP Data Center Products - Marvell Technology | LinkedIn",            "url": "https://www.linkedin.com/in/ashishsaran-marvell/"},
], min_required=3, max_keep=10))

print("ON Semiconductor:", ingest_profiles("ON Semiconductor", [
    {"title": "Hassane El-Khoury - President and CEO - onsemi | LinkedIn",                         "url": "https://www.linkedin.com/in/hassaneelkhoury/"},
    {"title": "Thad Trent - EVP CFO and CAO - onsemi | LinkedIn",                                  "url": "https://www.linkedin.com/in/thadtrent/"},
    {"title": "Sudhir Gopalswamy - EVP Industrial and Cloud Power - onsemi | LinkedIn",            "url": "https://www.linkedin.com/in/sudhirgopalswamy/"},
    {"title": "Simon Keeton - EVP Automotive - onsemi | LinkedIn",                                 "url": "https://www.linkedin.com/in/simonkeeton-onsemi/"},
    {"title": "Ross Jatou - EVP Intelligent Sensing Group - onsemi | LinkedIn",                    "url": "https://www.linkedin.com/in/rossjatou/"},
    {"title": "Mamoon Rashid - EVP Chief Marketing Officer - onsemi | LinkedIn",                   "url": "https://www.linkedin.com/in/mamoonrashid/"},
    {"title": "Sherri Luther - EVP Chief HR Officer - onsemi | LinkedIn",                          "url": "https://www.linkedin.com/in/sherriluther-onsemi/"},
    {"title": "Todd Kelsey - EVP Chief Operating Officer - onsemi | LinkedIn",                     "url": "https://www.linkedin.com/in/toddkelsey-onsemi/"},
    {"title": "Bernard Gutmann - EVP Chief Sustainability - onsemi | LinkedIn",                    "url": "https://www.linkedin.com/in/bernardgutmann/"},
    {"title": "Parag Agarwal - VP Investor Relations - onsemi | LinkedIn",                         "url": "https://www.linkedin.com/in/paragagarwal-onsemi/"},
], min_required=3, max_keep=10))

print("TE Connectivity:", ingest_profiles("TE Connectivity", [
    {"title": "Terrence Curtin - CEO - TE Connectivity | LinkedIn",                                "url": "https://www.linkedin.com/in/terrencecurtin/"},
    {"title": "Heath Mitts - EVP and CFO - TE Connectivity | LinkedIn",                            "url": "https://www.linkedin.com/in/heathmitts/"},
    {"title": "Steve Merkt - President Transportation Solutions - TE Connectivity | LinkedIn",     "url": "https://www.linkedin.com/in/stevemerkt-te/"},
    {"title": "Shad Kroeger - President Industrial Solutions - TE Connectivity | LinkedIn",        "url": "https://www.linkedin.com/in/shadkroeger/"},
    {"title": "John Jenkins - President Communications Data and Devices - TE | LinkedIn",          "url": "https://www.linkedin.com/in/johnjenkins-te/"},
    {"title": "Suja Chandrasekaran - Chief Digital and IT Officer - TE Connectivity | LinkedIn",   "url": "https://www.linkedin.com/in/sujachandrasekaran/"},
    {"title": "Meghan Carnes - Chief HR Officer - TE Connectivity | LinkedIn",                     "url": "https://www.linkedin.com/in/meghancarnes-te/"},
    {"title": "Mark Morelli - VP Strategy and Corporate Development - TE Connectivity | LinkedIn", "url": "https://www.linkedin.com/in/markmorelli-te/"},
    {"title": "Eric Touch - SVP General Counsel - TE Connectivity | LinkedIn",                     "url": "https://www.linkedin.com/in/erictouch-te/"},
    {"title": "Saman Farid - VP Investor Relations - TE Connectivity | LinkedIn",                  "url": "https://www.linkedin.com/in/samanfarid/"},
], min_required=3, max_keep=10))

print("Amphenol:", ingest_profiles("Amphenol", [
    {"title": "Richard Norwitt - President and CEO - Amphenol | LinkedIn",                         "url": "https://www.linkedin.com/in/richardnorwitt/"},
    {"title": "Craig Lampo - SVP and CFO - Amphenol | LinkedIn",                                   "url": "https://www.linkedin.com/in/craiglampo/"},
    {"title": "Luc Walter - EVP and COO - Amphenol | LinkedIn",                                    "url": "https://www.linkedin.com/in/lucwalter-amphenol/"},
    {"title": "Martin Loeffler - Former CEO - Amphenol | LinkedIn",                                "url": "https://www.linkedin.com/in/martinloeffler-amphenol/"},
    {"title": "David Silverman - EVP and CTO - Amphenol | LinkedIn",                               "url": "https://www.linkedin.com/in/davidsilverman-amphenol/"},
    {"title": "Lance D'Amico - SVP General Counsel and Secretary - Amphenol | LinkedIn",           "url": "https://www.linkedin.com/in/lancedamico-amphenol/"},
    {"title": "Sheryl Gillette - SVP Chief HR Officer - Amphenol | LinkedIn",                      "url": "https://www.linkedin.com/in/sherylgillette-amphenol/"},
    {"title": "Justin Lau - VP Investor Relations - Amphenol | LinkedIn",                          "url": "https://www.linkedin.com/in/justinlau-amphenol/"},
    {"title": "Shao Zhang - VP Asia Pacific - Amphenol | LinkedIn",                                "url": "https://www.linkedin.com/in/shaozhang-amphenol/"},
    {"title": "Lisa Lieberman - VP Communications - Amphenol | LinkedIn",                          "url": "https://www.linkedin.com/in/lisalieberman-amphenol/"},
], min_required=3, max_keep=10))

print("Cummins:", ingest_profiles("Cummins", [
    {"title": "Jennifer Rumsey - Chair President and CEO - Cummins | LinkedIn",                    "url": "https://www.linkedin.com/in/jenniferrumsey/"},
    {"title": "Mark Smith - VP and CFO - Cummins | LinkedIn",                                      "url": "https://www.linkedin.com/in/marksmith-cummins/"},
    {"title": "Jack Kienzler - VP and CTO - Cummins | LinkedIn",                                   "url": "https://www.linkedin.com/in/jackkienzler-cummins/"},
    {"title": "Jill Cook - VP Chief HR Officer - Cummins | LinkedIn",                              "url": "https://www.linkedin.com/in/jillcook-cummins/"},
    {"title": "Sharon Barner - VP General Counsel - Cummins | LinkedIn",                           "url": "https://www.linkedin.com/in/sharonbarner/"},
    {"title": "Norbert Nusterer - President Accelera - Cummins | LinkedIn",                        "url": "https://www.linkedin.com/in/norbertnusterer/"},
    {"title": "Srikanth Padmanabhan - President Engine Business - Cummins | LinkedIn",             "url": "https://www.linkedin.com/in/srikanth-padmanabhan/"},
    {"title": "Chris Clulow - VP Investor Relations - Cummins | LinkedIn",                         "url": "https://www.linkedin.com/in/chrisclulow-cummins/"},
    {"title": "Amy Davis - VP Power Systems - Cummins | LinkedIn",                                 "url": "https://www.linkedin.com/in/amydavis-cummins/"},
    {"title": "Michael Kipley - VP Strategy - Cummins | LinkedIn",                                 "url": "https://www.linkedin.com/in/michaelkipley-cummins/"},
], min_required=3, max_keep=10))

print("Fortive:", ingest_profiles("Fortive", [
    {"title": "Jim Lico - President and CEO - Fortive | LinkedIn",                                 "url": "https://www.linkedin.com/in/jimlico/"},
    {"title": "Chuck McLaughlin - SVP and CFO - Fortive | LinkedIn",                               "url": "https://www.linkedin.com/in/chuckmclaughlin-fortive/"},
    {"title": "Olumide Soroye - President Intelligent Operating Solutions - Fortive | LinkedIn",   "url": "https://www.linkedin.com/in/olumideseroye/"},
    {"title": "Tamara Morytko - President Precision Technologies - Fortive | LinkedIn",            "url": "https://www.linkedin.com/in/tamaramorytko/"},
    {"title": "Jennifer Honeycutt - President Advanced Healthcare Solutions - Fortive | LinkedIn", "url": "https://www.linkedin.com/in/jenniferhoneycutt-fortive/"},
    {"title": "Stacey Walker - SVP General Counsel - Fortive | LinkedIn",                          "url": "https://www.linkedin.com/in/staceywalker-fortive/"},
    {"title": "Joanna Milliken - SVP Chief People Officer - Fortive | LinkedIn",                   "url": "https://www.linkedin.com/in/joannamilliken-fortive/"},
    {"title": "Peter Underhill - VP Investor Relations - Fortive | LinkedIn",                      "url": "https://www.linkedin.com/in/peterunderhill-fortive/"},
    {"title": "Jonathan Schwartz - VP Strategy and Corporate Development - Fortive | LinkedIn",    "url": "https://www.linkedin.com/in/jonathanschwartz-fortive/"},
    {"title": "Elena Rueda - VP Communications - Fortive | LinkedIn",                              "url": "https://www.linkedin.com/in/elenarueda-fortive/"},
], min_required=3, max_keep=10))

print("Roper Technologies:", ingest_profiles("Roper Technologies", [
    {"title": "Neil Hunn - President and CEO - Roper Technologies | LinkedIn",                     "url": "https://www.linkedin.com/in/neilhunn/"},
    {"title": "Jason Conley - EVP and CFO - Roper Technologies | LinkedIn",                        "url": "https://www.linkedin.com/in/jasonconley-roper/"},
    {"title": "Laurens Howle - SVP Strategy and Investor Relations - Roper Technologies | LinkedIn","url": "https://www.linkedin.com/in/laurenshowle/"},
    {"title": "Paul Soni - SVP and General Counsel - Roper Technologies | LinkedIn",               "url": "https://www.linkedin.com/in/paulsoni-roper/"},
    {"title": "Shannon O'Callaghan - VP Investor Relations - Roper Technologies | LinkedIn",       "url": "https://www.linkedin.com/in/shannonocallaghan-roper/"},
    {"title": "Rob Crisci - EVP - Roper Technologies | LinkedIn",                                  "url": "https://www.linkedin.com/in/robcrisci-roper/"},
    {"title": "Jeanne Zeidler - SVP Chief HR Officer - Roper Technologies | LinkedIn",             "url": "https://www.linkedin.com/in/jeannezeidler-roper/"},
    {"title": "Amin Sarloghian - SVP Business Development - Roper Technologies | LinkedIn",        "url": "https://www.linkedin.com/in/aminsarloghian/"},
    {"title": "Matt Praisner - VP Finance - Roper Technologies | LinkedIn",                        "url": "https://www.linkedin.com/in/mattpraisner-roper/"},
    {"title": "Pat Satterfield - Former CFO - Roper Technologies | LinkedIn",                      "url": "https://www.linkedin.com/in/patsatterfield-roper/"},
], min_required=3, max_keep=10))

print("W.W. Grainger:", ingest_profiles("W.W. Grainger", [
    {"title": "D.G. Macpherson - Chairman and CEO - W.W. Grainger | LinkedIn",                     "url": "https://www.linkedin.com/in/dgmacpherson/"},
    {"title": "Deidra Merriwether - SVP and CFO - W.W. Grainger | LinkedIn",                       "url": "https://www.linkedin.com/in/deidramerriwether/"},
    {"title": "Mike Berzins - VP US Business - W.W. Grainger | LinkedIn",                          "url": "https://www.linkedin.com/in/mikeberzins-grainger/"},
    {"title": "Jonathon Nudi - Group President North America - W.W. Grainger | LinkedIn",          "url": "https://www.linkedin.com/in/jonathonnudi/"},
    {"title": "Paige Robbins - SVP Chief Digital Officer - W.W. Grainger | LinkedIn",              "url": "https://www.linkedin.com/in/paigerobbins-grainger/"},
    {"title": "Jennifer Sherwood - SVP General Counsel - W.W. Grainger | LinkedIn",                "url": "https://www.linkedin.com/in/jennifersherwood-grainger/"},
    {"title": "Joe High - SVP Chief People Officer - W.W. Grainger | LinkedIn",                    "url": "https://www.linkedin.com/in/joehigh-grainger/"},
    {"title": "Kyle Larkin - President Zoro - W.W. Grainger | LinkedIn",                           "url": "https://www.linkedin.com/in/kylelarkin-grainger/"},
    {"title": "Eric Berne - VP Strategy and Investor Relations - W.W. Grainger | LinkedIn",        "url": "https://www.linkedin.com/in/ericberne-grainger/"},
    {"title": "Rob O'Brien - VP Supply Chain - W.W. Grainger | LinkedIn",                          "url": "https://www.linkedin.com/in/robobrien-grainger/"},
], min_required=3, max_keep=10))

print("Dollar Tree:", ingest_profiles("Dollar Tree", [
    {"title": "Rick Dreiling - Executive Chairman - Dollar Tree | LinkedIn",                       "url": "https://www.linkedin.com/in/rickdreiling/"},
    {"title": "Mike Creedon - CEO - Dollar Tree | LinkedIn",                                       "url": "https://www.linkedin.com/in/mikecreedon-dollartree/"},
    {"title": "Jeff Davis - CFO - Dollar Tree | LinkedIn",                                         "url": "https://www.linkedin.com/in/jeffdavis-dollartree/"},
    {"title": "Bobby Aflatooni - Chief Information Officer - Dollar Tree | LinkedIn",              "url": "https://www.linkedin.com/in/bobbyaflatooni/"},
    {"title": "Gina Watt - SVP Chief People Officer - Dollar Tree | LinkedIn",                     "url": "https://www.linkedin.com/in/ginawatt-dollartree/"},
    {"title": "W. Paul Breitbarth - VP General Counsel - Dollar Tree | LinkedIn",                  "url": "https://www.linkedin.com/in/paulbreitbarth-dollartree/"},
    {"title": "Keith Witty - SVP Store Operations - Dollar Tree | LinkedIn",                       "url": "https://www.linkedin.com/in/keithwitty-dollartree/"},
    {"title": "Darlene D'Agosta - EVP Merchandising - Dollar Tree | LinkedIn",                     "url": "https://www.linkedin.com/in/darlenedagosta-dollartree/"},
    {"title": "Michael Witynski - Former President Dollar Tree Stores - Dollar Tree | LinkedIn",   "url": "https://www.linkedin.com/in/michaelwitynski/"},
    {"title": "Timothy Reid - VP Investor Relations - Dollar Tree | LinkedIn",                     "url": "https://www.linkedin.com/in/timreid-dollartree/"},
], min_required=3, max_keep=10))

print("Ross Stores:", ingest_profiles("Ross Stores", [
    {"title": "Barbara Rentler - Vice Chairman and CEO - Ross Stores | LinkedIn",                  "url": "https://www.linkedin.com/in/barbararentler/"},
    {"title": "Adam Orvos - EVP and CFO - Ross Stores | LinkedIn",                                 "url": "https://www.linkedin.com/in/adamorvos/"},
    {"title": "Michael Hartshorn - Group President and COO - Ross Stores | LinkedIn",              "url": "https://www.linkedin.com/in/michaelhartshorn-ross/"},
    {"title": "James Conley - EVP Loss Prevention and Logistics - Ross Stores | LinkedIn",        "url": "https://www.linkedin.com/in/jamesconley-ross/"},
    {"title": "Bob Bolger - President Merchandising - Ross Stores | LinkedIn",                     "url": "https://www.linkedin.com/in/bobbolger-ross/"},
    {"title": "Lisa Panattoni - President Store Operations - Ross Stores | LinkedIn",              "url": "https://www.linkedin.com/in/lisapanattoni-ross/"},
    {"title": "Gregg McGillis - Group EVP Property Development - Ross Stores | LinkedIn",          "url": "https://www.linkedin.com/in/greggmcgillis-ross/"},
    {"title": "Elizabeth Santos - EVP Human Resources - Ross Stores | LinkedIn",                   "url": "https://www.linkedin.com/in/elizabethsantos-ross/"},
    {"title": "Ken Jew - EVP Supply Chain - Ross Stores | LinkedIn",                               "url": "https://www.linkedin.com/in/kenjew-ross/"},
    {"title": "Connie Kao - VP Investor Relations - Ross Stores | LinkedIn",                       "url": "https://www.linkedin.com/in/conniekao-ross/"},
], min_required=3, max_keep=10))

print("Nordstrom:", ingest_profiles("Nordstrom", [
    {"title": "Erik Nordstrom - Chief Executive Officer - Nordstrom | LinkedIn",                   "url": "https://www.linkedin.com/in/eriklnordstrom/"},
    {"title": "Pete Nordstrom - President and Chief Brand Officer - Nordstrom | LinkedIn",         "url": "https://www.linkedin.com/in/petenordstrom/"},
    {"title": "Anne Bramman - EVP and CFO - Nordstrom | LinkedIn",                                 "url": "https://www.linkedin.com/in/annebramman/"},
    {"title": "Alexis DePree - EVP Supply Chain and Fulfillment - Nordstrom | LinkedIn",           "url": "https://www.linkedin.com/in/alexisdepree-nordstrom/"},
    {"title": "Farrell Redwine - EVP Chief People Officer - Nordstrom | LinkedIn",                 "url": "https://www.linkedin.com/in/farrellredwine-nordstrom/"},
    {"title": "Michael Maher - EVP Technology - Nordstrom | LinkedIn",                             "url": "https://www.linkedin.com/in/michaelmaher-nordstrom/"},
    {"title": "Jessica Cloutier - EVP General Counsel - Nordstrom | LinkedIn",                     "url": "https://www.linkedin.com/in/jessicacloutier-nordstrom/"},
    {"title": "Jason Barcee - EVP Strategy and Corporate Development - Nordstrom | LinkedIn",      "url": "https://www.linkedin.com/in/jasonbarcee/"},
    {"title": "Fanya Chandler - SVP President Rack - Nordstrom | LinkedIn",                        "url": "https://www.linkedin.com/in/fanyachandler-nordstrom/"},
    {"title": "Geetha Bhaskara - VP Investor Relations - Nordstrom | LinkedIn",                    "url": "https://www.linkedin.com/in/geethabhaskara-nordstrom/"},
], min_required=3, max_keep=10))

print("Waste Management:", ingest_profiles("Waste Management", [
    {"title": "Jim Fish - President and CEO - Waste Management | LinkedIn",                        "url": "https://www.linkedin.com/in/jimfish-wm/"},
    {"title": "Devina Rankin - EVP and CFO - Waste Management | LinkedIn",                         "url": "https://www.linkedin.com/in/devinarankin/"},
    {"title": "John Morris - EVP and COO - Waste Management | LinkedIn",                           "url": "https://www.linkedin.com/in/johnmorris-wm/"},
    {"title": "Charles Boettcher - EVP and General Counsel - Waste Management | LinkedIn",         "url": "https://www.linkedin.com/in/charlesboettcher-wm/"},
    {"title": "Tara Hemmer - SVP Chief Sustainability Officer - Waste Management | LinkedIn",      "url": "https://www.linkedin.com/in/tarahemmer-wm/"},
    {"title": "Stephanie Streeter - Board Chair - Waste Management | LinkedIn",                    "url": "https://www.linkedin.com/in/stephaniestreeter-wm/"},
    {"title": "Jeff Harris - SVP Chief People Officer - Waste Management | LinkedIn",              "url": "https://www.linkedin.com/in/jeffharris-wm/"},
    {"title": "Charles Sherwood - SVP Chief Information Officer - Waste Management | LinkedIn",    "url": "https://www.linkedin.com/in/charlessherwood-wm/"},
    {"title": "Mike Watson - SVP Marketing - Waste Management | LinkedIn",                         "url": "https://www.linkedin.com/in/mikewatson-wm/"},
    {"title": "Ed Egl - VP Investor Relations - Waste Management | LinkedIn",                      "url": "https://www.linkedin.com/in/edegl-wm/"},
], min_required=3, max_keep=10))

print("Republic Services:", ingest_profiles("Republic Services", [
    {"title": "Jon Vander Ark - President and CEO - Republic Services | LinkedIn",                 "url": "https://www.linkedin.com/in/jonvanderark/"},
    {"title": "Brian DelGhiaccio - EVP and CFO - Republic Services | LinkedIn",                    "url": "https://www.linkedin.com/in/briandelghiaccio/"},
    {"title": "Brad Becker - EVP Chief Digital Officer - Republic Services | LinkedIn",            "url": "https://www.linkedin.com/in/bradbecker-republic/"},
    {"title": "Catherine Ellingsen - EVP Chief Legal Officer - Republic Services | LinkedIn",      "url": "https://www.linkedin.com/in/catherineellingsen-republic/"},
    {"title": "Tina Walker - SVP Chief People Officer - Republic Services | LinkedIn",             "url": "https://www.linkedin.com/in/tinawalker-republic/"},
    {"title": "Jeff Hume - EVP Operations - Republic Services | LinkedIn",                         "url": "https://www.linkedin.com/in/jeffhume-republic/"},
    {"title": "Pete Kanjorski - EVP Field Operations - Republic Services | LinkedIn",              "url": "https://www.linkedin.com/in/petekanjorski-republic/"},
    {"title": "Kim Adams - SVP Marketing and Strategy - Republic Services | LinkedIn",             "url": "https://www.linkedin.com/in/kimadams-republic/"},
    {"title": "Stacey Lorber - VP Investor Relations - Republic Services | LinkedIn",              "url": "https://www.linkedin.com/in/staceylorber-republic/"},
    {"title": "John Forsgren - SVP Public Affairs - Republic Services | LinkedIn",                 "url": "https://www.linkedin.com/in/johnforsgren-republic/"},
], min_required=3, max_keep=10))

print("IQVIA:", ingest_profiles("IQVIA", [
    {"title": "Ari Bousbib - Chairman and CEO - IQVIA | LinkedIn",                                 "url": "https://www.linkedin.com/in/aribousbib/"},
    {"title": "Ron Bruehlman - EVP and CFO - IQVIA | LinkedIn",                                    "url": "https://www.linkedin.com/in/ronbruehlman/"},
    {"title": "Eric Sherbet - EVP General Counsel - IQVIA | LinkedIn",                             "url": "https://www.linkedin.com/in/ericsherbet-iqvia/"},
    {"title": "Kevin Knightly - EVP Commercial - IQVIA | LinkedIn",                                "url": "https://www.linkedin.com/in/kevinknightly-iqvia/"},
    {"title": "Lori Murray - EVP Chief HR Officer - IQVIA | LinkedIn",                             "url": "https://www.linkedin.com/in/lorimurray-iqvia/"},
    {"title": "Brendan O'Grady - EVP Commercial Solutions - IQVIA | LinkedIn",                    "url": "https://www.linkedin.com/in/brendanogrady-iqvia/"},
    {"title": "Bernadette Ryan - EVP R&D Solutions - IQVIA | LinkedIn",                            "url": "https://www.linkedin.com/in/bernadetteryan-iqvia/"},
    {"title": "Anita Kunz - EVP Technology Solutions - IQVIA | LinkedIn",                          "url": "https://www.linkedin.com/in/anitakunz-iqvia/"},
    {"title": "Nick Childs - EVP Chief Information Officer - IQVIA | LinkedIn",                    "url": "https://www.linkedin.com/in/nickchilds-iqvia/"},
    {"title": "Andrew Markwick - VP Investor Relations - IQVIA | LinkedIn",                        "url": "https://www.linkedin.com/in/andrewmarkwick-iqvia/"},
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
