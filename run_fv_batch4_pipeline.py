"""FV Batch 4 — 20 new Fortune 500 / large enterprise companies, eleynxiong@berkeley.edu."""
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
    {"name": "Warner Bros. Discovery",        "domain": "wbd.com",                     "industry": "Media / Streaming / Entertainment / News",     "email_pattern": "first.last"},
    {"name": "Paramount Global",              "domain": "paramount.com",               "industry": "Media / Streaming / Film / TV",                 "email_pattern": "first.last"},
    {"name": "Spotify",                       "domain": "spotify.com",                 "industry": "Music Streaming / Audio Tech / Creator Economy","email_pattern": "first.last"},
    {"name": "Roblox",                        "domain": "roblox.com",                  "industry": "Gaming / Metaverse / User-Generated Content",   "email_pattern": "first.last"},
    {"name": "Take-Two Interactive",          "domain": "take2games.com",              "industry": "Video Games / Interactive Entertainment",       "email_pattern": "first.last"},
    {"name": "Regeneron",                     "domain": "regeneron.com",               "industry": "Biotechnology / Oncology / Immunology",         "email_pattern": "first.last"},
    {"name": "Vertex Pharmaceuticals",        "domain": "vrtx.com",                    "industry": "Biotechnology / Rare Disease / Gene Therapy",   "email_pattern": "first.last"},
    {"name": "Biogen",                        "domain": "biogen.com",                  "industry": "Biotechnology / Neurology / Rare Diseases",     "email_pattern": "first.last"},
    {"name": "Intuitive Surgical",            "domain": "intuitive.com",               "industry": "Surgical Robotics / Medical Technology / AI",   "email_pattern": "first.last"},
    {"name": "Edwards Lifesciences",          "domain": "edwards.com",                 "industry": "Cardiac Devices / Heart Valves / Hemodynamics", "email_pattern": "first.last"},
    {"name": "Truist Financial",              "domain": "truist.com",                  "industry": "Banking / Commercial Finance / Wealth Management","email_pattern": "first.last"},
    {"name": "State Street",                  "domain": "statestreet.com",             "industry": "Asset Management / Custody / Institutional Finance","email_pattern": "first.last"},
    {"name": "Principal Financial",           "domain": "principal.com",               "industry": "Insurance / Retirement / Asset Management",     "email_pattern": "first.last"},
    {"name": "Aflac",                         "domain": "aflac.com",                   "industry": "Supplemental Insurance / Employee Benefits",    "email_pattern": "first.last"},
    {"name": "Intercontinental Exchange",     "domain": "theice.com",                  "industry": "Financial Exchanges / Data / Derivatives",      "email_pattern": "first.last"},
    {"name": "CME Group",                     "domain": "cmegroup.com",                "industry": "Derivatives Exchanges / Futures / Risk Mgmt",   "email_pattern": "first.last"},
    {"name": "Veeva Systems",                 "domain": "veeva.com",                   "industry": "Cloud / Life Sciences SaaS / CRM / Clinical",   "email_pattern": "first.last"},
    {"name": "Dynatrace",                     "domain": "dynatrace.com",               "industry": "Observability / AIOps / Cloud Monitoring SaaS", "email_pattern": "first.last"},
    {"name": "Nutanix",                       "domain": "nutanix.com",                 "industry": "Hybrid Cloud / HCI / Enterprise Infrastructure","email_pattern": "first.last"},
    {"name": "Live Nation Entertainment",     "domain": "livenationentertainment.com", "industry": "Live Events / Ticketing / Artist Management",   "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Batch 4 - July 2026"
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

print("Warner Bros. Discovery:", ingest_profiles("Warner Bros. Discovery", [
    {"title": "David Zaslav - President and CEO - Warner Bros. Discovery | LinkedIn",         "url": "https://www.linkedin.com/in/davidzaslav/"},
    {"title": "Gunnar Wiedenfels - CFO - Warner Bros. Discovery | LinkedIn",                  "url": "https://www.linkedin.com/in/gunnarwiedenfels/"},
    {"title": "Casey Bloys - Chairman and CEO HBO and Max Content - WBD | LinkedIn",          "url": "https://www.linkedin.com/in/caseybloys/"},
    {"title": "Kathleen Finch - Chairman US Networks - Warner Bros. Discovery | LinkedIn",    "url": "https://www.linkedin.com/in/kathleenfinch/"},
    {"title": "JB Perrette - CEO and President Global Streaming - WBD | LinkedIn",           "url": "https://www.linkedin.com/in/jbperrette/"},
    {"title": "Gerhard Zeiler - Chief Revenue Officer International - WBD | LinkedIn",        "url": "https://www.linkedin.com/in/gerhardzeiler/"},
    {"title": "Adria Alpert Romm - Chief People and Culture Officer - WBD | LinkedIn",       "url": "https://www.linkedin.com/in/adriaalpertromm/"},
    {"title": "Bruce Campbell - Chief Strategy Officer - Warner Bros. Discovery | LinkedIn",  "url": "https://www.linkedin.com/in/brucecampbell-wbd/"},
    {"title": "Lori Locke - EVP General Counsel - Warner Bros. Discovery | LinkedIn",         "url": "https://www.linkedin.com/in/lorilocke-wbd/"},
    {"title": "Savalle Sims - EVP Chief Legal Officer - WBD | LinkedIn",                     "url": "https://www.linkedin.com/in/savallesims/"},
], min_required=3, max_keep=10))

print("Paramount Global:", ingest_profiles("Paramount Global", [
    {"title": "Bob Bakish - Former CEO - Paramount Global | LinkedIn",                        "url": "https://www.linkedin.com/in/bobbakish/"},
    {"title": "Naveen Chopra - EVP and CFO - Paramount Global | LinkedIn",                    "url": "https://www.linkedin.com/in/naveenchopra-paramount/"},
    {"title": "Brian Robbins - President and CEO Paramount Pictures - Paramount | LinkedIn",  "url": "https://www.linkedin.com/in/brianrobbins-paramount/"},
    {"title": "Chris McCarthy - President CEO Showtime and MTV Entertainment - Paramount | LinkedIn","url": "https://www.linkedin.com/in/chrismccarthy-paramount/"},
    {"title": "Marco Nobili - EVP International President Paramount+ - Paramount | LinkedIn", "url": "https://www.linkedin.com/in/marconobili/"},
    {"title": "Pam Kaufman - President International Markets - Paramount | LinkedIn",         "url": "https://www.linkedin.com/in/pamkaufman/"},
    {"title": "Anthony DiClemente - EVP Investor Relations - Paramount Global | LinkedIn",    "url": "https://www.linkedin.com/in/anthonydiclemente/"},
    {"title": "Marni Turner - EVP Chief People Officer - Paramount Global | LinkedIn",        "url": "https://www.linkedin.com/in/marniturner/"},
    {"title": "Dan Cohen - EVP Worldwide TV Distribution - Paramount Global | LinkedIn",      "url": "https://www.linkedin.com/in/dancohen-paramount/"},
    {"title": "Jeff Shultz - Chief Business Officer Paramount+ - Paramount | LinkedIn",       "url": "https://www.linkedin.com/in/jeffshultz-paramount/"},
], min_required=3, max_keep=10))

print("Spotify:", ingest_profiles("Spotify", [
    {"title": "Daniel Ek - CEO and Co-Founder - Spotify | LinkedIn",                         "url": "https://www.linkedin.com/in/danielek/"},
    {"title": "Christian Luiga - CFO - Spotify | LinkedIn",                                  "url": "https://www.linkedin.com/in/christianluiga/"},
    {"title": "Alex Norström - Chief Business Officer - Spotify | LinkedIn",                  "url": "https://www.linkedin.com/in/alexnorstrom/"},
    {"title": "Gustav Söderström - Chief Product Officer - Spotify | LinkedIn",               "url": "https://www.linkedin.com/in/gustavsoderstrom/"},
    {"title": "Katarina Berg - Chief HR Officer - Spotify | LinkedIn",                        "url": "https://www.linkedin.com/in/katarinberg/"},
    {"title": "Dustee Jenkins - Chief Public Affairs Officer - Spotify | LinkedIn",           "url": "https://www.linkedin.com/in/dusteejenkins/"},
    {"title": "Jeremy Erlich - Co-Head of Music - Spotify | LinkedIn",                       "url": "https://www.linkedin.com/in/jeremyerlich/"},
    {"title": "Dawn Ostroff - Former Chief Content Officer - Spotify | LinkedIn",             "url": "https://www.linkedin.com/in/dawnostroff/"},
    {"title": "Sahar Elhabashi - VP and GM Podcast - Spotify | LinkedIn",                    "url": "https://www.linkedin.com/in/saharelhabashi/"},
    {"title": "Brian Benedik - VP Global Sales - Spotify | LinkedIn",                        "url": "https://www.linkedin.com/in/brianbenedik/"},
], min_required=3, max_keep=10))

print("Roblox:", ingest_profiles("Roblox", [
    {"title": "David Baszucki - CEO and Founder - Roblox | LinkedIn",                        "url": "https://www.linkedin.com/in/davidbaszucki/"},
    {"title": "Michael Guthrie - CFO - Roblox | LinkedIn",                                   "url": "https://www.linkedin.com/in/michaelguthrie-roblox/"},
    {"title": "Barbara Messing - Chief People Officer - Roblox | LinkedIn",                  "url": "https://www.linkedin.com/in/barbaramessing/"},
    {"title": "Daniel Sturman - CTO - Roblox | LinkedIn",                                    "url": "https://www.linkedin.com/in/danielsturman/"},
    {"title": "Stefano Corazza - SVP Metaverse - Roblox | LinkedIn",                         "url": "https://www.linkedin.com/in/stefanocorazza/"},
    {"title": "Manuel Bronstein - Chief Product Officer - Roblox | LinkedIn",                "url": "https://www.linkedin.com/in/manuelbronstein/"},
    {"title": "Tami Bhaumik - VP Safety and Civility - Roblox | LinkedIn",                   "url": "https://www.linkedin.com/in/tamibhaumik/"},
    {"title": "Brian Cooper - Chief Legal Officer - Roblox | LinkedIn",                      "url": "https://www.linkedin.com/in/briancooper-roblox/"},
    {"title": "Christina Wootton - VP Brand and Creator Partnerships - Roblox | LinkedIn",   "url": "https://www.linkedin.com/in/christinawootton/"},
    {"title": "Eric Cassel - Co-Founder and VP Product Experience - Roblox | LinkedIn",      "url": "https://www.linkedin.com/in/ericcassel/"},
], min_required=3, max_keep=10))

print("Take-Two Interactive:", ingest_profiles("Take-Two Interactive", [
    {"title": "Strauss Zelnick - Executive Chairman and CEO - Take-Two Interactive | LinkedIn","url": "https://www.linkedin.com/in/strausszelnick/"},
    {"title": "Lainie Goldstein - EVP and CFO - Take-Two Interactive | LinkedIn",            "url": "https://www.linkedin.com/in/lainiegoldstein/"},
    {"title": "Karl Slatoff - President - Take-Two Interactive | LinkedIn",                  "url": "https://www.linkedin.com/in/karlslatoff/"},
    {"title": "Dan Emerson - EVP and GM 2K - Take-Two Interactive | LinkedIn",               "url": "https://www.linkedin.com/in/danemerson-2k/"},
    {"title": "David Ismailer - President 2K - Take-Two Interactive | LinkedIn",             "url": "https://www.linkedin.com/in/davidismailer/"},
    {"title": "Scott Hartsman - VP Product Development - Take-Two Interactive | LinkedIn",   "url": "https://www.linkedin.com/in/scotthartsman/"},
    {"title": "Matthew Breitman - EVP and General Counsel - Take-Two Interactive | LinkedIn","url": "https://www.linkedin.com/in/matthewbreitman/"},
    {"title": "Andrew Pederson - EVP Human Resources - Take-Two Interactive | LinkedIn",     "url": "https://www.linkedin.com/in/andrewpederson-t2/"},
    {"title": "Hank Diamond - EVP Global Operations - Take-Two Interactive | LinkedIn",      "url": "https://www.linkedin.com/in/hankdiamond-t2/"},
    {"title": "Alan Lewis - EVP Corporate Communications - Take-Two Interactive | LinkedIn", "url": "https://www.linkedin.com/in/alanlewis-t2/"},
], min_required=3, max_keep=10))

print("Regeneron:", ingest_profiles("Regeneron", [
    {"title": "Leonard Schleifer - Co-Founder President and CEO - Regeneron | LinkedIn",     "url": "https://www.linkedin.com/in/leonardschleifer/"},
    {"title": "George Yancopoulos - Co-Founder President and CSO - Regeneron | LinkedIn",    "url": "https://www.linkedin.com/in/georgeyancopoulos/"},
    {"title": "Chris Fenimore - CFO - Regeneron | LinkedIn",                                 "url": "https://www.linkedin.com/in/chrisfenimore/"},
    {"title": "Ryan Crowe - EVP Chief Commercial Officer - Regeneron | LinkedIn",            "url": "https://www.linkedin.com/in/ryancrowe-regeneron/"},
    {"title": "Christopher Azzara - EVP General Counsel - Regeneron | LinkedIn",             "url": "https://www.linkedin.com/in/christopherazzara/"},
    {"title": "Huw Jones - SVP Head of Global Medical Affairs - Regeneron | LinkedIn",       "url": "https://www.linkedin.com/in/huwjones-regeneron/"},
    {"title": "Marion McCourt - EVP Commercial Operations - Regeneron | LinkedIn",           "url": "https://www.linkedin.com/in/marionmccourt/"},
    {"title": "Patrick Aldridge - SVP Oncology - Regeneron | LinkedIn",                     "url": "https://www.linkedin.com/in/patrickaldridge-regeneron/"},
    {"title": "Yunji Mao - VP Quantitative Sciences - Regeneron | LinkedIn",                 "url": "https://www.linkedin.com/in/yunjimao/"},
    {"title": "George Dohrmann - SVP HR - Regeneron | LinkedIn",                             "url": "https://www.linkedin.com/in/georgedohrmann/"},
], min_required=3, max_keep=10))

print("Vertex Pharmaceuticals:", ingest_profiles("Vertex Pharmaceuticals", [
    {"title": "Reshma Kewalramani - CEO and President - Vertex Pharmaceuticals | LinkedIn",   "url": "https://www.linkedin.com/in/reshmaker/"},
    {"title": "Charlie Wagner - EVP and CFO - Vertex Pharmaceuticals | LinkedIn",             "url": "https://www.linkedin.com/in/charliewagner-vrtx/"},
    {"title": "Stuart Arbuckle - EVP Chief Operating Officer - Vertex Pharmaceuticals | LinkedIn","url": "https://www.linkedin.com/in/stuartarbuckle/"},
    {"title": "Carmen Bozic - EVP Chief Medical Officer - Vertex Pharmaceuticals | LinkedIn", "url": "https://www.linkedin.com/in/carmenbozic/"},
    {"title": "Bastiano Sanna - EVP Cell and Genetic Therapies - Vertex | LinkedIn",         "url": "https://www.linkedin.com/in/bastianosanna/"},
    {"title": "Nia Tatsis - EVP Chief Regulatory Officer - Vertex | LinkedIn",               "url": "https://www.linkedin.com/in/niatatsis/"},
    {"title": "Mike Parini - EVP General Counsel - Vertex Pharmaceuticals | LinkedIn",        "url": "https://www.linkedin.com/in/mikeparini/"},
    {"title": "Tracy Sequeira - SVP HR - Vertex Pharmaceuticals | LinkedIn",                 "url": "https://www.linkedin.com/in/tracysequeira/"},
    {"title": "David Altshuler - EVP Global Research - Vertex | LinkedIn",                   "url": "https://www.linkedin.com/in/davidaltshuler/"},
    {"title": "Sense Subramaniam - SVP Head of Commercial - Vertex | LinkedIn",              "url": "https://www.linkedin.com/in/sensesubramaniam/"},
], min_required=3, max_keep=10))

print("Biogen:", ingest_profiles("Biogen", [
    {"title": "Christopher Viehbacher - President and CEO - Biogen | LinkedIn",              "url": "https://www.linkedin.com/in/christopherviehbacher/"},
    {"title": "Robin Kramer - EVP and CFO - Biogen | LinkedIn",                              "url": "https://www.linkedin.com/in/robinkramer-biogen/"},
    {"title": "Priya Singhal - EVP Head of Development - Biogen | LinkedIn",                 "url": "https://www.linkedin.com/in/priyasinghal-biogen/"},
    {"title": "Alisha Alaimo - President North America - Biogen | LinkedIn",                 "url": "https://www.linkedin.com/in/alishaalaimo/"},
    {"title": "Alfred Sandrock - Former EVP CMO - Biogen | LinkedIn",                        "url": "https://www.linkedin.com/in/alfredsandrock/"},
    {"title": "Susan Specht - EVP Chief HR Officer - Biogen | LinkedIn",                     "url": "https://www.linkedin.com/in/susanspecht-biogen/"},
    {"title": "Mike McDonnell - EVP General Counsel - Biogen | LinkedIn",                    "url": "https://www.linkedin.com/in/mikemcdonnell-biogen/"},
    {"title": "Chirfi Guindo - EVP Chief Commercial Officer - Biogen | LinkedIn",            "url": "https://www.linkedin.com/in/chirfiguindo/"},
    {"title": "Dasha Mishina - SVP Neurodegeneration Research - Biogen | LinkedIn",          "url": "https://www.linkedin.com/in/dashamishina/"},
    {"title": "Katie Mast - SVP Investor Relations - Biogen | LinkedIn",                     "url": "https://www.linkedin.com/in/katiemast-biogen/"},
], min_required=3, max_keep=10))

print("Intuitive Surgical:", ingest_profiles("Intuitive Surgical", [
    {"title": "Gary Guthart - President and CEO - Intuitive Surgical | LinkedIn",            "url": "https://www.linkedin.com/in/garyguthart/"},
    {"title": "Jamie Samath - CFO - Intuitive Surgical | LinkedIn",                          "url": "https://www.linkedin.com/in/jamiesamath/"},
    {"title": "Myriam Curet - EVP and CMO - Intuitive Surgical | LinkedIn",                  "url": "https://www.linkedin.com/in/myriamcuret/"},
    {"title": "Dave Rosa - EVP Products and Technology - Intuitive Surgical | LinkedIn",     "url": "https://www.linkedin.com/in/daverosa-isrg/"},
    {"title": "Sally Miley - EVP Customer Service - Intuitive Surgical | LinkedIn",          "url": "https://www.linkedin.com/in/sallymiley/"},
    {"title": "Brian Miller - VP Finance and Business Development - Intuitive | LinkedIn",   "url": "https://www.linkedin.com/in/brianmiller-isrg/"},
    {"title": "Glenn Vavoso - SVP Strategy and Acquisitions - Intuitive | LinkedIn",         "url": "https://www.linkedin.com/in/glennvavoso/"},
    {"title": "Erin Lavin Calder - VP Human Resources - Intuitive Surgical | LinkedIn",     "url": "https://www.linkedin.com/in/erinlavincalder/"},
    {"title": "Ana Leal - VP International - Intuitive Surgical | LinkedIn",                 "url": "https://www.linkedin.com/in/analeal-isrg/"},
    {"title": "Tom Cooper - SVP Business Development - Intuitive Surgical | LinkedIn",       "url": "https://www.linkedin.com/in/tomcooper-isrg/"},
], min_required=3, max_keep=10))

print("Edwards Lifesciences:", ingest_profiles("Edwards Lifesciences", [
    {"title": "Michael Mussallem - Chairman and CEO - Edwards Lifesciences | LinkedIn",      "url": "https://www.linkedin.com/in/michaelmussallem/"},
    {"title": "Scott Ullem - EVP and CFO - Edwards Lifesciences | LinkedIn",                 "url": "https://www.linkedin.com/in/scottullem/"},
    {"title": "Larry Wood - Group VP Transcatheter Structural Heart - Edwards | LinkedIn",   "url": "https://www.linkedin.com/in/larrywood-edwards/"},
    {"title": "Donald Bobo Jr. - Group VP Surgical Structural Heart - Edwards | LinkedIn",   "url": "https://www.linkedin.com/in/donaldbobojr/"},
    {"title": "Daveen Chopra - Group VP Critical Care - Edwards Lifesciences | LinkedIn",    "url": "https://www.linkedin.com/in/daveenchopra/"},
    {"title": "Catherine Szyman - EVP and GM Edwards Infusion - Edwards | LinkedIn",        "url": "https://www.linkedin.com/in/catherineszyman/"},
    {"title": "Staci Doying - Group VP Human Resources - Edwards Lifesciences | LinkedIn",  "url": "https://www.linkedin.com/in/stacidoying/"},
    {"title": "David Erickson - Group VP Research and Technology - Edwards | LinkedIn",      "url": "https://www.linkedin.com/in/daviderickson-edwards/"},
    {"title": "Christine Blansett - VP Investor Relations - Edwards Lifesciences | LinkedIn","url": "https://www.linkedin.com/in/christineblansett/"},
    {"title": "Mike Mussallem - CEO - Edwards Lifesciences | LinkedIn",                     "url": "https://www.linkedin.com/in/mikemussallem/"},
], min_required=3, max_keep=10))

print("Truist Financial:", ingest_profiles("Truist Financial", [
    {"title": "Bill Rogers - Chairman and CEO - Truist Financial | LinkedIn",                "url": "https://www.linkedin.com/in/billrogers-truist/"},
    {"title": "Mike Maguire - CFO - Truist Financial | LinkedIn",                            "url": "https://www.linkedin.com/in/mikemaguire-truist/"},
    {"title": "Donta Wilson - Chief Digital and Client Experience Officer - Truist | LinkedIn","url": "https://www.linkedin.com/in/dontawilson/"},
    {"title": "Scott Case - Chief Information Officer - Truist Financial | LinkedIn",        "url": "https://www.linkedin.com/in/scottcase-truist/"},
    {"title": "Brant Standridge - President Retail and Small Business - Truist | LinkedIn",  "url": "https://www.linkedin.com/in/brantstandridge/"},
    {"title": "Hugh Cummins - Vice Chairman COO - Truist Financial | LinkedIn",              "url": "https://www.linkedin.com/in/hughcummins-truist/"},
    {"title": "Ellen Fitzsimmons - Vice Chairman and CLO - Truist Financial | LinkedIn",     "url": "https://www.linkedin.com/in/ellenfitzsimmons/"},
    {"title": "Kimberly Moore - Chief HR Officer - Truist Financial | LinkedIn",             "url": "https://www.linkedin.com/in/kimberlymoore-truist/"},
    {"title": "Daryl Bible - Former CFO - Truist Financial | LinkedIn",                      "url": "https://www.linkedin.com/in/darylbible/"},
    {"title": "Joe Thompson - Head of Investment Banking - Truist | LinkedIn",               "url": "https://www.linkedin.com/in/joethompson-truist/"},
], min_required=3, max_keep=10))

print("State Street:", ingest_profiles("State Street", [
    {"title": "Ron O'Hanley - Chairman and CEO - State Street | LinkedIn",                   "url": "https://www.linkedin.com/in/ronohanley/"},
    {"title": "Eric Aboaf - EVP and CFO - State Street | LinkedIn",                          "url": "https://www.linkedin.com/in/ericaboaf/"},
    {"title": "Yie-Hsin Hung - President and CEO State Street Global Advisors - State Street | LinkedIn","url": "https://www.linkedin.com/in/yiehsinhung/"},
    {"title": "Donna Milrod - EVP Chief Client Officer - State Street | LinkedIn",           "url": "https://www.linkedin.com/in/donnamulrod/"},
    {"title": "Martine Bond - EVP Human Resources - State Street | LinkedIn",                "url": "https://www.linkedin.com/in/martinebond/"},
    {"title": "Jeff Conway - EVP Asset Owner Solutions - State Street | LinkedIn",           "url": "https://www.linkedin.com/in/jeffconway-statestreet/"},
    {"title": "Andrew Erickson - EVP Alternatives Servicing - State Street | LinkedIn",      "url": "https://www.linkedin.com/in/andrewerickson-statestreet/"},
    {"title": "David Puth - EVP Markets Division - State Street | LinkedIn",                 "url": "https://www.linkedin.com/in/davidputh/"},
    {"title": "Lori Heinel - Global CIO SSGA - State Street | LinkedIn",                    "url": "https://www.linkedin.com/in/loriheinel/"},
    {"title": "Deven Sharma - Director - State Street | LinkedIn",                           "url": "https://www.linkedin.com/in/devensharma-statestreet/"},
], min_required=3, max_keep=10))

print("Principal Financial:", ingest_profiles("Principal Financial", [
    {"title": "Dan Houston - Chairman President and CEO - Principal Financial | LinkedIn",   "url": "https://www.linkedin.com/in/danhouston-principal/"},
    {"title": "Deanna Strable - EVP and CFO - Principal Financial | LinkedIn",               "url": "https://www.linkedin.com/in/deannastrable/"},
    {"title": "Renee Schaaf - President Principal International - Principal Financial | LinkedIn","url": "https://www.linkedin.com/in/reneeschaaf/"},
    {"title": "Patrick Halter - President Principal Global Investors - Principal | LinkedIn","url": "https://www.linkedin.com/in/patrickhalter/"},
    {"title": "Amy Friedrich - President Benefits and Protection - Principal | LinkedIn",    "url": "https://www.linkedin.com/in/amyfriedrich-principal/"},
    {"title": "Karen Shaff - EVP and General Counsel - Principal Financial | LinkedIn",      "url": "https://www.linkedin.com/in/karenshaff/"},
    {"title": "Natalie Lamarque - Chief HR Officer - Principal Financial | LinkedIn",        "url": "https://www.linkedin.com/in/natalielamarque/"},
    {"title": "Chris Littlefield - President and GM Retirement and Income - Principal | LinkedIn","url": "https://www.linkedin.com/in/chrislittlefield-principal/"},
    {"title": "Timothy Dunbar - Former CIO - Principal Financial | LinkedIn",                "url": "https://www.linkedin.com/in/timothydunbar/"},
    {"title": "Juan Pablo Newman - EVP Corporate Finance - Principal | LinkedIn",            "url": "https://www.linkedin.com/in/juanpablonewman/"},
], min_required=3, max_keep=10))

print("Aflac:", ingest_profiles("Aflac", [
    {"title": "Daniel Amos - Chairman and CEO - Aflac | LinkedIn",                           "url": "https://www.linkedin.com/in/danielamos-aflac/"},
    {"title": "Max Brodén - EVP and CFO - Aflac | LinkedIn",                                 "url": "https://www.linkedin.com/in/maxbroden/"},
    {"title": "Frederick Crawford - EVP and COO Aflac US - Aflac | LinkedIn",                "url": "https://www.linkedin.com/in/frederickrawford/"},
    {"title": "Virgil Miller - President Aflac US - Aflac | LinkedIn",                       "url": "https://www.linkedin.com/in/virgilmiller-aflac/"},
    {"title": "Koichiro Yoshizumi - President Aflac Japan - Aflac | LinkedIn",               "url": "https://www.linkedin.com/in/koichiroyoshizumi/"},
    {"title": "April Clobes - EVP Chief Marketing Officer - Aflac | LinkedIn",               "url": "https://www.linkedin.com/in/aprilclobes/"},
    {"title": "Catherine Blades - SVP Corporate Communications - Aflac | LinkedIn",          "url": "https://www.linkedin.com/in/catherineblades/"},
    {"title": "Lisa Gable - VP Human Resources - Aflac | LinkedIn",                          "url": "https://www.linkedin.com/in/lisagable-aflac/"},
    {"title": "J. Todd Combs - SVP Investments - Aflac | LinkedIn",                         "url": "https://www.linkedin.com/in/jtoddcombs/"},
    {"title": "Steve Beaver - EVP Chief Information Officer - Aflac | LinkedIn",             "url": "https://www.linkedin.com/in/stevebeaver-aflac/"},
], min_required=3, max_keep=10))

print("Intercontinental Exchange:", ingest_profiles("Intercontinental Exchange", [
    {"title": "Jeffrey Sprecher - Founder Chairman and CEO - ICE | LinkedIn",                "url": "https://www.linkedin.com/in/jeffreysprecher/"},
    {"title": "Warren Gardiner - EVP and CFO - Intercontinental Exchange | LinkedIn",        "url": "https://www.linkedin.com/in/warrengardiner-ice/"},
    {"title": "Ben Jackson - President - Intercontinental Exchange | LinkedIn",              "url": "https://www.linkedin.com/in/benjackson-ice/"},
    {"title": "Lynn Martin - President NYSE and Fixed Income Data - ICE | LinkedIn",         "url": "https://www.linkedin.com/in/lynnmartin-ice/"},
    {"title": "Chris Edmonds - President ICE Fixed Income and Data Services | LinkedIn",     "url": "https://www.linkedin.com/in/chrisedmonds-ice/"},
    {"title": "Stacey Cunningham - Former President NYSE - ICE | LinkedIn",                  "url": "https://www.linkedin.com/in/staceycunningham-nyse/"},
    {"title": "Andrew Lamb - President ICE Futures US and ICE Clear US | LinkedIn",         "url": "https://www.linkedin.com/in/andrewlamb-ice/"},
    {"title": "Michael Bodson - Board Director - ICE | LinkedIn",                            "url": "https://www.linkedin.com/in/michaelbodson/"},
    {"title": "Jamie Mauldin - EVP Chief HR Officer - ICE | LinkedIn",                       "url": "https://www.linkedin.com/in/jamiemauldin/"},
    {"title": "Johnathan Short - EVP Chief Legal and Regulatory Officer - ICE | LinkedIn",  "url": "https://www.linkedin.com/in/johnathanshort/"},
], min_required=3, max_keep=10))

print("CME Group:", ingest_profiles("CME Group", [
    {"title": "Terry Duffy - Chairman and CEO - CME Group | LinkedIn",                       "url": "https://www.linkedin.com/in/terryduffy/"},
    {"title": "Lynne Fitzpatrick - CFO - CME Group | LinkedIn",                              "url": "https://www.linkedin.com/in/lynnefitzpatrick-cme/"},
    {"title": "Sean Tully - Global Head of Rates and OTC - CME Group | LinkedIn",           "url": "https://www.linkedin.com/in/seantully-cme/"},
    {"title": "Tim McCourt - Global Head of Equity and FX - CME Group | LinkedIn",          "url": "https://www.linkedin.com/in/timmccourt/"},
    {"title": "Sunil Cutinho - President CME Clearing - CME Group | LinkedIn",               "url": "https://www.linkedin.com/in/sunilcutinho/"},
    {"title": "Suzanne Sprague - MD Global Head of Clearing - CME Group | LinkedIn",        "url": "https://www.linkedin.com/in/suzannesprague/"},
    {"title": "Bryan Durkin - Former President - CME Group | LinkedIn",                      "url": "https://www.linkedin.com/in/bryandurkin/"},
    {"title": "Andrew Lamb - Chief HR Officer - CME Group | LinkedIn",                       "url": "https://www.linkedin.com/in/andrewlamb-cme/"},
    {"title": "Kathleen Cronin - SVP and General Counsel - CME Group | LinkedIn",            "url": "https://www.linkedin.com/in/kathleencronin-cme/"},
    {"title": "Derek Sammann - Global Head of Commodities and Options - CME Group | LinkedIn","url": "https://www.linkedin.com/in/dereksammann/"},
], min_required=3, max_keep=10))

print("Veeva Systems:", ingest_profiles("Veeva Systems", [
    {"title": "Peter Gassner - Founder and CEO - Veeva Systems | LinkedIn",                  "url": "https://www.linkedin.com/in/petergassner/"},
    {"title": "Brent Bowman - CFO - Veeva Systems | LinkedIn",                               "url": "https://www.linkedin.com/in/brentbowman-veeva/"},
    {"title": "Paul Shawah - SVP Commercial Strategy - Veeva Systems | LinkedIn",            "url": "https://www.linkedin.com/in/paulshawah/"},
    {"title": "Gunnar Esiason - VP R&D Engagement - Veeva Systems | LinkedIn",              "url": "https://www.linkedin.com/in/gunnaresiason/"},
    {"title": "Tom Schwenger - President - Veeva Systems | LinkedIn",                        "url": "https://www.linkedin.com/in/tomschwenger/"},
    {"title": "Jim Reilly - General Counsel - Veeva Systems | LinkedIn",                     "url": "https://www.linkedin.com/in/jimreilly-veeva/"},
    {"title": "Mary Doris - VP Human Resources - Veeva Systems | LinkedIn",                  "url": "https://www.linkedin.com/in/marydoris/"},
    {"title": "Rishi Bhatt - VP Product Management - Veeva Systems | LinkedIn",              "url": "https://www.linkedin.com/in/rishibhatt-veeva/"},
    {"title": "Alan Mateo - VP North America Commercial - Veeva Systems | LinkedIn",         "url": "https://www.linkedin.com/in/alanmateo-veeva/"},
    {"title": "Ian Hersey - SVP Vault Clinical - Veeva Systems | LinkedIn",                  "url": "https://www.linkedin.com/in/ianhersey/"},
], min_required=3, max_keep=10))

print("Dynatrace:", ingest_profiles("Dynatrace", [
    {"title": "Rick McConnell - CEO - Dynatrace | LinkedIn",                                  "url": "https://www.linkedin.com/in/rickmcconnell/"},
    {"title": "Jim Benson - CFO - Dynatrace | LinkedIn",                                     "url": "https://www.linkedin.com/in/jimbenson-dynatrace/"},
    {"title": "Steve Tack - SVP Product Management - Dynatrace | LinkedIn",                  "url": "https://www.linkedin.com/in/stevetack/"},
    {"title": "Brian Healy - SVP Go-to-Market - Dynatrace | LinkedIn",                       "url": "https://www.linkedin.com/in/brianhealy-dynatrace/"},
    {"title": "Alois Reitbauer - VP Research and Innovation - Dynatrace | LinkedIn",         "url": "https://www.linkedin.com/in/aloisreitbauer/"},
    {"title": "Michael Kopp - SVP Product - Dynatrace | LinkedIn",                           "url": "https://www.linkedin.com/in/michaelkopp-dynatrace/"},
    {"title": "Florian Rainer - SVP Engineering - Dynatrace | LinkedIn",                     "url": "https://www.linkedin.com/in/florianrainer/"},
    {"title": "Graeme Payne - Chief Trust and Security Officer - Dynatrace | LinkedIn",      "url": "https://www.linkedin.com/in/graemepayne/"},
    {"title": "Mike Silvey - Chief Customer Officer - Dynatrace | LinkedIn",                 "url": "https://www.linkedin.com/in/mikesilvey/"},
    {"title": "Bernd Greifeneder - CTO - Dynatrace | LinkedIn",                              "url": "https://www.linkedin.com/in/berndgreifeneder/"},
], min_required=3, max_keep=10))

print("Nutanix:", ingest_profiles("Nutanix", [
    {"title": "Rajiv Ramaswami - President and CEO - Nutanix | LinkedIn",                    "url": "https://www.linkedin.com/in/rajivramaswami/"},
    {"title": "Rukmini Sivaraman - CFO - Nutanix | LinkedIn",                                "url": "https://www.linkedin.com/in/rukmini-sivaraman/"},
    {"title": "Tarkan Maner - President and CCO - Nutanix | LinkedIn",                       "url": "https://www.linkedin.com/in/tarkanmaner/"},
    {"title": "Thomas Cornely - SVP Product and Solutions - Nutanix | LinkedIn",             "url": "https://www.linkedin.com/in/thomascornely/"},
    {"title": "Christian Alvarez - SVP Worldwide Sales - Nutanix | LinkedIn",                "url": "https://www.linkedin.com/in/christianalvarez-nutanix/"},
    {"title": "Roopa Bhatt - Chief People Officer - Nutanix | LinkedIn",                     "url": "https://www.linkedin.com/in/roopabhatt/"},
    {"title": "Wendy M. Pfeiffer - CIO - Nutanix | LinkedIn",                               "url": "https://www.linkedin.com/in/wendypfeiffer/"},
    {"title": "Lee Caswell - SVP Product and Solutions Marketing - Nutanix | LinkedIn",      "url": "https://www.linkedin.com/in/leecaswell/"},
    {"title": "Priti Shokeen - SVP Strategy - Nutanix | LinkedIn",                           "url": "https://www.linkedin.com/in/pritishokeen/"},
    {"title": "Aaron Weis - Chief Digital and Technology Officer - Nutanix | LinkedIn",      "url": "https://www.linkedin.com/in/aaronweis/"},
], min_required=3, max_keep=10))

print("Live Nation Entertainment:", ingest_profiles("Live Nation Entertainment", [
    {"title": "Michael Rapino - President and CEO - Live Nation Entertainment | LinkedIn",   "url": "https://www.linkedin.com/in/michaelrapino/"},
    {"title": "Joe Berchtold - President and COO - Live Nation Entertainment | LinkedIn",    "url": "https://www.linkedin.com/in/joeberchtold/"},
    {"title": "Brian Capo - EVP and CFO - Live Nation Entertainment | LinkedIn",             "url": "https://www.linkedin.com/in/briancapo-livenation/"},
    {"title": "Mark Campana - EVP North American Concerts - Live Nation | LinkedIn",         "url": "https://www.linkedin.com/in/markcampana/"},
    {"title": "Michael Cohl - Former Chairman - Live Nation Entertainment | LinkedIn",       "url": "https://www.linkedin.com/in/michaelcohl/"},
    {"title": "David Marcus - EVP Music - Live Nation Entertainment | LinkedIn",             "url": "https://www.linkedin.com/in/davidmarcus-livenation/"},
    {"title": "John Meglen - President and CEO Concerts West - Live Nation | LinkedIn",      "url": "https://www.linkedin.com/in/johnmeglen/"},
    {"title": "Greg Trojan - EVP Venue Nation - Live Nation Entertainment | LinkedIn",       "url": "https://www.linkedin.com/in/gregtrojan/"},
    {"title": "Bob Roux - President US Concerts - Live Nation | LinkedIn",                   "url": "https://www.linkedin.com/in/bobroux/"},
    {"title": "Geoff Harris - Chief HR Officer - Live Nation Entertainment | LinkedIn",      "url": "https://www.linkedin.com/in/geoffharris-livenation/"},
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

with open("FV_CAMPAIGN_ID.txt", "w") as f:
    f.write(campaign_id)

# ── Personalize ───────────────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing — FV template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="fv",
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
