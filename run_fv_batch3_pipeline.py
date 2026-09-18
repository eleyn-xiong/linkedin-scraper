"""FV Batch 3 — 15 new Fortune 500 companies, eleynxiong@berkeley.edu."""
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
    {"name": "Walgreens Boots Alliance", "domain": "walgreens.com",         "industry": "Pharmacy / Retail Health",                "email_pattern": "first.last"},
    {"name": "Best Buy",                 "domain": "bestbuy.com",           "industry": "Consumer Electronics Retail / Tech",      "email_pattern": "first.last"},
    {"name": "Kroger",                   "domain": "kroger.com",            "industry": "Grocery / Retail / Pharmacy",             "email_pattern": "first.last"},
    {"name": "American Airlines",        "domain": "aa.com",                "industry": "Commercial Aviation / Travel",            "email_pattern": "first.last"},
    {"name": "Delta Air Lines",          "domain": "delta.com",             "industry": "Commercial Aviation / Loyalty",           "email_pattern": "first.last"},
    {"name": "United Airlines",          "domain": "united.com",            "industry": "Commercial Aviation / Global",            "email_pattern": "first.last"},
    {"name": "Hilton",                   "domain": "hilton.com",            "industry": "Hospitality / Hotels / Travel Tech",      "email_pattern": "first.last"},
    {"name": "Hyatt Hotels",             "domain": "hyatt.com",             "industry": "Hospitality / Luxury Hotels",             "email_pattern": "first.last"},
    {"name": "McDonald's",               "domain": "mcdonalds.com",         "industry": "Quick Service Restaurants / Retail",      "email_pattern": "first.last"},
    {"name": "Yum Brands",               "domain": "yum.com",               "industry": "Quick Service Restaurants (KFC/Pizza Hut/Taco Bell)", "email_pattern": "first.last"},
    {"name": "General Mills",            "domain": "generalmills.com",      "industry": "Food / Consumer Packaged Goods",          "email_pattern": "first.last"},
    {"name": "Kraft Heinz",              "domain": "kraftheinzcompany.com", "industry": "Food & Beverage / Consumer Packaged Goods","email_pattern": "first.last"},
    {"name": "Tyson Foods",              "domain": "tysonfoods.com",        "industry": "Protein / Food Manufacturing",            "email_pattern": "first.last"},
    {"name": "AstraZeneca",              "domain": "astrazeneca.com",       "industry": "Biopharmaceuticals / Oncology / R&D",     "email_pattern": "first.last"},
    {"name": "Bristol-Myers Squibb",     "domain": "bms.com",               "industry": "Biopharmaceuticals / Oncology / Immunology","email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Batch 3 - June 2026"
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

print("Walgreens Boots Alliance:", ingest_profiles("Walgreens Boots Alliance", [
    {"title": "Tim Wentworth - CEO - Walgreens Boots Alliance | LinkedIn",                   "url": "https://www.linkedin.com/in/timwentworth/"},
    {"title": "Manmohan Mahajan - CFO - Walgreens Boots Alliance | LinkedIn",                "url": "https://www.linkedin.com/in/manmohanmahajan/"},
    {"title": "Holly May - EVP Chief HR Officer - Walgreens Boots Alliance | LinkedIn",      "url": "https://www.linkedin.com/in/hollymay-wba/"},
    {"title": "Tracey Brown - EVP President Walgreens - Walgreens Boots Alliance | LinkedIn","url": "https://www.linkedin.com/in/traceybrown-walgreens/"},
    {"title": "John Driscoll - President US Healthcare - Walgreens Boots Alliance | LinkedIn","url": "https://www.linkedin.com/in/johndriscoll-wba/"},
    {"title": "Rick Gates - Chief Pharmacy Officer - Walgreens Boots Alliance | LinkedIn",   "url": "https://www.linkedin.com/in/rickgates-walgreens/"},
    {"title": "Maria Smith - EVP Chief Legal Officer - Walgreens Boots Alliance | LinkedIn", "url": "https://www.linkedin.com/in/mariasmith-wba/"},
    {"title": "Ramita Iyer - VP Digital and Innovation - Walgreens Boots Alliance | LinkedIn","url": "https://www.linkedin.com/in/ramitaiyer/"},
    {"title": "Stefano Pessina - Executive Chairman - Walgreens Boots Alliance | LinkedIn",  "url": "https://www.linkedin.com/in/stefanopessina/"},
    {"title": "Elizabeth Burger - Chief People Officer - Walgreens Boots Alliance | LinkedIn","url": "https://www.linkedin.com/in/elizabethburger-wba/"},
], min_required=3, max_keep=10))

print("Best Buy:", ingest_profiles("Best Buy", [
    {"title": "Corie Barry - CEO - Best Buy | LinkedIn",                                     "url": "https://www.linkedin.com/in/coriebarry/"},
    {"title": "Matt Bilunas - CFO - Best Buy | LinkedIn",                                    "url": "https://www.linkedin.com/in/mattbilunas/"},
    {"title": "Damien Harmon - EVP Omnichannel - Best Buy | LinkedIn",                       "url": "https://www.linkedin.com/in/damienharmon/"},
    {"title": "Todd Hartman - EVP General Counsel - Best Buy | LinkedIn",                    "url": "https://www.linkedin.com/in/toddhartman-bestbuy/"},
    {"title": "Allison Peterson - Chief Customer Officer - Best Buy | LinkedIn",              "url": "https://www.linkedin.com/in/allisonpeterson-bestbuy/"},
    {"title": "Frank Bedo - EVP Chief Retail Officer - Best Buy | LinkedIn",                 "url": "https://www.linkedin.com/in/frankbedo/"},
    {"title": "Brian Tilzer - Chief Digital and Technology Officer - Best Buy | LinkedIn",   "url": "https://www.linkedin.com/in/briantilzer/"},
    {"title": "Trish Walker - President Best Buy Health - Best Buy | LinkedIn",              "url": "https://www.linkedin.com/in/trishwalker-bestbuy/"},
    {"title": "Suja Chandrasekaran - Chief Information Officer - Best Buy | LinkedIn",       "url": "https://www.linkedin.com/in/sujachandrasekaran/"},
    {"title": "Jason Bonfig - Chief Merchandising Officer - Best Buy | LinkedIn",            "url": "https://www.linkedin.com/in/jasonbonfig/"},
], min_required=3, max_keep=10))

print("Kroger:", ingest_profiles("Kroger", [
    {"title": "Rodney McMullen - Chairman and CEO - Kroger | LinkedIn",                      "url": "https://www.linkedin.com/in/rodneymcmullen/"},
    {"title": "Todd Foley - CFO - Kroger | LinkedIn",                                        "url": "https://www.linkedin.com/in/toddfoley-kroger/"},
    {"title": "Kenneth Kimbell - EVP General Counsel - Kroger | LinkedIn",                   "url": "https://www.linkedin.com/in/kennethkimbell/"},
    {"title": "Stuart Aitken - SVP Chief Merchant and Marketing Officer - Kroger | LinkedIn","url": "https://www.linkedin.com/in/stuartaitken/"},
    {"title": "Yael Cosset - EVP Chief Information Officer - Kroger | LinkedIn",             "url": "https://www.linkedin.com/in/yaelcosset/"},
    {"title": "Tim Massa - Group VP HR - Kroger | LinkedIn",                                 "url": "https://www.linkedin.com/in/timmassa/"},
    {"title": "Jessica Adelman - Group VP Corporate Affairs - Kroger | LinkedIn",            "url": "https://www.linkedin.com/in/jessicaadelman/"},
    {"title": "Dan De La Rosa - Group VP Natural and Organic - Kroger | LinkedIn",           "url": "https://www.linkedin.com/in/dandelarosa-kroger/"},
    {"title": "Gabriel Arreaga - SVP Supply Chain - Kroger | LinkedIn",                      "url": "https://www.linkedin.com/in/gabrielarreaga/"},
    {"title": "Melissa Plaisance - VP Finance - Kroger | LinkedIn",                          "url": "https://www.linkedin.com/in/melissaplaisance/"},
], min_required=3, max_keep=10))

print("American Airlines:", ingest_profiles("American Airlines", [
    {"title": "Robert Isom - President and CEO - American Airlines | LinkedIn",              "url": "https://www.linkedin.com/in/robertisom/"},
    {"title": "Devon May - SVP and CFO - American Airlines | LinkedIn",                      "url": "https://www.linkedin.com/in/devonmay-aa/"},
    {"title": "David Seymour - COO - American Airlines | LinkedIn",                          "url": "https://www.linkedin.com/in/davidseymour-aa/"},
    {"title": "Maya Leibman - EVP and CTO - American Airlines | LinkedIn",                   "url": "https://www.linkedin.com/in/mayaleibman/"},
    {"title": "Priya Aiyar - EVP General Counsel - American Airlines | LinkedIn",            "url": "https://www.linkedin.com/in/priyaaiyar/"},
    {"title": "Julie Rath - SVP Customer Experience - American Airlines | LinkedIn",         "url": "https://www.linkedin.com/in/julierath-aa/"},
    {"title": "Shane Jones - SVP Employee Relations - American Airlines | LinkedIn",         "url": "https://www.linkedin.com/in/shanejones-aa/"},
    {"title": "Nate Gatten - SVP Government Affairs - American Airlines | LinkedIn",         "url": "https://www.linkedin.com/in/nategatten/"},
    {"title": "Vasu Raja - Chief Commercial Officer - American Airlines | LinkedIn",          "url": "https://www.linkedin.com/in/vasuraja/"},
    {"title": "Steve Johnson - EVP Corporate Affairs - American Airlines | LinkedIn",        "url": "https://www.linkedin.com/in/stevejohnson-aa/"},
], min_required=3, max_keep=10))

print("Delta Air Lines:", ingest_profiles("Delta Air Lines", [
    {"title": "Ed Bastian - CEO - Delta Air Lines | LinkedIn",                               "url": "https://www.linkedin.com/in/edbastian/"},
    {"title": "Dan Janki - EVP and CFO - Delta Air Lines | LinkedIn",                        "url": "https://www.linkedin.com/in/danjanki/"},
    {"title": "Glen Hauenstein - President - Delta Air Lines | LinkedIn",                    "url": "https://www.linkedin.com/in/glenhauenstein/"},
    {"title": "Joanne Smith - EVP Chief People Officer - Delta Air Lines | LinkedIn",        "url": "https://www.linkedin.com/in/joannesmith-delta/"},
    {"title": "Peter Carter - EVP Chief Legal Officer - Delta Air Lines | LinkedIn",         "url": "https://www.linkedin.com/in/petercarter-delta/"},
    {"title": "Allison Ausband - EVP Chief Customer Experience Officer - Delta | LinkedIn",  "url": "https://www.linkedin.com/in/allisonausband/"},
    {"title": "Rahul Samant - EVP Chief Information Officer - Delta Air Lines | LinkedIn",   "url": "https://www.linkedin.com/in/rahulsamant/"},
    {"title": "Eric Phillips - SVP Revenue Management - Delta Air Lines | LinkedIn",         "url": "https://www.linkedin.com/in/ericphillips-delta/"},
    {"title": "John Laughter - SVP Network Planning - Delta Air Lines | LinkedIn",           "url": "https://www.linkedin.com/in/johnlaughter-delta/"},
    {"title": "Gareth Joyce - President Delta Connection - Delta Air Lines | LinkedIn",      "url": "https://www.linkedin.com/in/garethjoyces/"},
], min_required=3, max_keep=10))

print("United Airlines:", ingest_profiles("United Airlines", [
    {"title": "Scott Kirby - CEO - United Airlines | LinkedIn",                              "url": "https://www.linkedin.com/in/scottkirby/"},
    {"title": "Gerald Laderman - EVP and CFO - United Airlines | LinkedIn",                  "url": "https://www.linkedin.com/in/geraldladerman/"},
    {"title": "Brett Hart - President - United Airlines | LinkedIn",                         "url": "https://www.linkedin.com/in/bretthart-united/"},
    {"title": "Andrew Nocella - EVP Chief Commercial Officer - United Airlines | LinkedIn",  "url": "https://www.linkedin.com/in/andrewnocella/"},
    {"title": "Kate Gebo - EVP HR and Labor Relations - United Airlines | LinkedIn",         "url": "https://www.linkedin.com/in/kategebo/"},
    {"title": "Kris Srikrishnan - EVP Chief Transformation and Digital Officer - United Airlines | LinkedIn","url": "https://www.linkedin.com/in/krissrikrishnan/"},
    {"title": "Todd Insler - SVP Flight Operations - United Airlines | LinkedIn",            "url": "https://www.linkedin.com/in/toddinsler/"},
    {"title": "David Kinzelman - EVP Chief Customer Officer - United Airlines | LinkedIn",   "url": "https://www.linkedin.com/in/davidkinzelman/"},
    {"title": "Sasha Johnson - SVP Operations - United Airlines | LinkedIn",                 "url": "https://www.linkedin.com/in/sashajohnson-united/"},
    {"title": "Michael Bonds - SVP Global Airport Operations - United Airlines | LinkedIn",  "url": "https://www.linkedin.com/in/michaelbonds-united/"},
], min_required=3, max_keep=10))

print("Hilton:", ingest_profiles("Hilton", [
    {"title": "Christopher Nassetta - President and CEO - Hilton | LinkedIn",                "url": "https://www.linkedin.com/in/christophernassetta/"},
    {"title": "Kevin Jacobs - CFO - Hilton | LinkedIn",                                      "url": "https://www.linkedin.com/in/kevinjacobs-hilton/"},
    {"title": "Chris Silcock - President Global Brands - Hilton | LinkedIn",                 "url": "https://www.linkedin.com/in/chrissilcock/"},
    {"title": "Laura Fuentes - Chief HR Officer - Hilton | LinkedIn",                        "url": "https://www.linkedin.com/in/laurafuentes-hilton/"},
    {"title": "Jonathan Witter - President Global Development - Hilton | LinkedIn",          "url": "https://www.linkedin.com/in/jonathanwitter/"},
    {"title": "Danny Hughes - President Hilton Americas - Hilton | LinkedIn",                "url": "https://www.linkedin.com/in/dannyhughes-hilton/"},
    {"title": "Simon Vincent - President EMEA and Asia Pacific - Hilton | LinkedIn",         "url": "https://www.linkedin.com/in/simonvincent-hilton/"},
    {"title": "Matt Schuyler - Chief Brand Officer - Hilton | LinkedIn",                     "url": "https://www.linkedin.com/in/mattschuyler/"},
    {"title": "Kristin Campbell - EVP General Counsel - Hilton | LinkedIn",                  "url": "https://www.linkedin.com/in/kristincampbell-hilton/"},
    {"title": "Michael Duffy - EVP Corporate Affairs - Hilton | LinkedIn",                   "url": "https://www.linkedin.com/in/michaelduffy-hilton/"},
], min_required=3, max_keep=10))

print("Hyatt Hotels:", ingest_profiles("Hyatt Hotels", [
    {"title": "Mark Hoplamazian - President and CEO - Hyatt Hotels | LinkedIn",              "url": "https://www.linkedin.com/in/markhoplamazian/"},
    {"title": "Joan Bottarini - CFO - Hyatt Hotels | LinkedIn",                              "url": "https://www.linkedin.com/in/joanbottarini/"},
    {"title": "Tom Pritzker - Executive Chairman - Hyatt Hotels | LinkedIn",                 "url": "https://www.linkedin.com/in/tompritzker/"},
    {"title": "Malaika Myers - Chief HR Officer - Hyatt Hotels | LinkedIn",                  "url": "https://www.linkedin.com/in/malaikamyers/"},
    {"title": "Mark Vondrasek - Chief Commercial Officer - Hyatt Hotels | LinkedIn",         "url": "https://www.linkedin.com/in/markvondrasek/"},
    {"title": "Heather Geisler - Chief Marketing Officer - Hyatt Hotels | LinkedIn",         "url": "https://www.linkedin.com/in/heathergeisler/"},
    {"title": "Jim Chu - EVP Global Real Estate and Capital Markets - Hyatt | LinkedIn",     "url": "https://www.linkedin.com/in/jimchu-hyatt/"},
    {"title": "Ginny Newman - General Counsel - Hyatt Hotels | LinkedIn",                    "url": "https://www.linkedin.com/in/ginnynewman-hyatt/"},
    {"title": "Amy Weinberg - SVP Loyalty Brand - Hyatt Hotels | LinkedIn",                  "url": "https://www.linkedin.com/in/amyweinberg-hyatt/"},
    {"title": "Pete Sears - Group President Americas - Hyatt Hotels | LinkedIn",             "url": "https://www.linkedin.com/in/petesears-hyatt/"},
], min_required=3, max_keep=10))

print("McDonald's:", ingest_profiles("McDonald's", [
    {"title": "Chris Kempczinski - President and CEO - McDonald's | LinkedIn",               "url": "https://www.linkedin.com/in/chriskempczinski/"},
    {"title": "Ian Borden - EVP and CFO - McDonald's | LinkedIn",                            "url": "https://www.linkedin.com/in/ianborden-mcdonalds/"},
    {"title": "Joe Erlinger - President McDonald's USA - McDonald's | LinkedIn",             "url": "https://www.linkedin.com/in/joeerlinger/"},
    {"title": "Manu Steijaert - EVP Chief Customer Officer - McDonald's | LinkedIn",         "url": "https://www.linkedin.com/in/manusteijaert/"},
    {"title": "Heidi Capozzi - EVP Chief People Officer - McDonald's | LinkedIn",            "url": "https://www.linkedin.com/in/heidicapozzi/"},
    {"title": "Brian Rice - EVP and CTO - McDonald's | LinkedIn",                            "url": "https://www.linkedin.com/in/brianrice-mcdonalds/"},
    {"title": "Marion Gross - EVP Chief Supply Chain Officer - McDonald's | LinkedIn",       "url": "https://www.linkedin.com/in/mariongross-mcdonalds/"},
    {"title": "Tariq Hassan - Chief Marketing and Customer Experience Officer - McDonald's | LinkedIn","url": "https://www.linkedin.com/in/tariqhassan/"},
    {"title": "Desiree Griffin - SVP HR Business Partners - McDonald's | LinkedIn",          "url": "https://www.linkedin.com/in/desireegriffin/"},
    {"title": "Jon Banner - EVP Chief Impact Officer - McDonald's | LinkedIn",               "url": "https://www.linkedin.com/in/jonbanner/"},
], min_required=3, max_keep=10))

print("Yum Brands:", ingest_profiles("Yum Brands", [
    {"title": "David Gibbs - CEO - Yum Brands | LinkedIn",                                   "url": "https://www.linkedin.com/in/davidgibbs-yum/"},
    {"title": "Chris Turner - CFO - Yum Brands | LinkedIn",                                  "url": "https://www.linkedin.com/in/christurner-yum/"},
    {"title": "Tracy Skeans - COO - Yum Brands | LinkedIn",                                  "url": "https://www.linkedin.com/in/tracyskeans/"},
    {"title": "Scott Catlett - Chief Legal Officer - Yum Brands | LinkedIn",                 "url": "https://www.linkedin.com/in/scottcatlett/"},
    {"title": "Monica Rothgery - Chief People Officer - Yum Brands | LinkedIn",              "url": "https://www.linkedin.com/in/monicarothgery/"},
    {"title": "Aaron Powell - President KFC Division - Yum Brands | LinkedIn",               "url": "https://www.linkedin.com/in/aaronpowell-kfc/"},
    {"title": "Mark King - CEO Taco Bell - Yum Brands | LinkedIn",                           "url": "https://www.linkedin.com/in/markking-tacobell/"},
    {"title": "Kevin Hochman - President KFC US - Yum Brands | LinkedIn",                    "url": "https://www.linkedin.com/in/kevinhochman/"},
    {"title": "Tabassum Zalotrawala - SVP Chief Development Officer - Yum Brands | LinkedIn","url": "https://www.linkedin.com/in/tabassum-zalotrawala/"},
    {"title": "Melissa Friebe - SVP Chief Brand Officer Taco Bell - Yum Brands | LinkedIn", "url": "https://www.linkedin.com/in/melissafriebe/"},
], min_required=3, max_keep=10))

print("General Mills:", ingest_profiles("General Mills", [
    {"title": "Jeff Harmening - Chairman and CEO - General Mills | LinkedIn",                "url": "https://www.linkedin.com/in/jeffharmening/"},
    {"title": "Kofi Bruce - CFO - General Mills | LinkedIn",                                 "url": "https://www.linkedin.com/in/kofibruce/"},
    {"title": "Dana McNabb - Group President North America Retail - General Mills | LinkedIn","url": "https://www.linkedin.com/in/danamcnabb/"},
    {"title": "Bethany Quam - Group President International and Pet - General Mills | LinkedIn","url": "https://www.linkedin.com/in/bethanyquam/"},
    {"title": "Jonathon Nudi - Group President North America Pet - General Mills | LinkedIn","url": "https://www.linkedin.com/in/jonathonnudi/"},
    {"title": "Shawn O'Grady - Chief Revenue Officer - General Mills | LinkedIn",            "url": "https://www.linkedin.com/in/shawnogrady/"},
    {"title": "Eric Dean - Chief Supply Chain Officer - General Mills | LinkedIn",           "url": "https://www.linkedin.com/in/ericdean-generalmills/"},
    {"title": "Jodi Benson - Chief HR Officer - General Mills | LinkedIn",                   "url": "https://www.linkedin.com/in/jodibenson-generalmills/"},
    {"title": "Jano Jimenez - Chief Marketing Officer - General Mills | LinkedIn",           "url": "https://www.linkedin.com/in/janojimenez/"},
    {"title": "Deidra Merriwether - SVP Strategy - General Mills | LinkedIn",                "url": "https://www.linkedin.com/in/deidra-merriwether/"},
], min_required=3, max_keep=10))

print("Kraft Heinz:", ingest_profiles("Kraft Heinz", [
    {"title": "Carlos Abrams-Rivera - CEO - Kraft Heinz | LinkedIn",                         "url": "https://www.linkedin.com/in/carlosabrams-rivera/"},
    {"title": "Andre Maciel - CFO - Kraft Heinz | LinkedIn",                                 "url": "https://www.linkedin.com/in/andremaciel-kh/"},
    {"title": "Rashida La Lande - EVP General Counsel - Kraft Heinz | LinkedIn",             "url": "https://www.linkedin.com/in/rashidalatande/"},
    {"title": "Marcos Eloi Lima - Chief People Officer - Kraft Heinz | LinkedIn",            "url": "https://www.linkedin.com/in/marcoseloilima/"},
    {"title": "Flavio Torres - President North America - Kraft Heinz | LinkedIn",            "url": "https://www.linkedin.com/in/flaviotorres-kh/"},
    {"title": "Nina Barton - President Global Platforms - Kraft Heinz | LinkedIn",           "url": "https://www.linkedin.com/in/ninabarton-kh/"},
    {"title": "Stephanie Slingerland - Chief Marketing Officer - Kraft Heinz | LinkedIn",    "url": "https://www.linkedin.com/in/stephanieslingerland/"},
    {"title": "Raja Subramanian - Chief Strategy Officer - Kraft Heinz | LinkedIn",          "url": "https://www.linkedin.com/in/rajasubramanian-kh/"},
    {"title": "Derek Hazzard - President International - Kraft Heinz | LinkedIn",            "url": "https://www.linkedin.com/in/derekhazzard/"},
    {"title": "Paulo Basilio - Global COO - Kraft Heinz | LinkedIn",                         "url": "https://www.linkedin.com/in/paulobasilio-kh/"},
], min_required=3, max_keep=10))

print("Tyson Foods:", ingest_profiles("Tyson Foods", [
    {"title": "Donnie King - President and CEO - Tyson Foods | LinkedIn",                    "url": "https://www.linkedin.com/in/donnieking-tyson/"},
    {"title": "John R. Tyson - CFO - Tyson Foods | LinkedIn",                               "url": "https://www.linkedin.com/in/johnrtyson/"},
    {"title": "John H. Tyson - Executive Chairman - Tyson Foods | LinkedIn",                 "url": "https://www.linkedin.com/in/johnhtyson/"},
    {"title": "Amy Tu - EVP General Counsel - Tyson Foods | LinkedIn",                       "url": "https://www.linkedin.com/in/amytu-tyson/"},
    {"title": "David Bray - President Fresh Meats - Tyson Foods | LinkedIn",                 "url": "https://www.linkedin.com/in/davidbray-tyson/"},
    {"title": "Wes Morris - President Prepared Foods - Tyson Foods | LinkedIn",              "url": "https://www.linkedin.com/in/wesmorris-tyson/"},
    {"title": "Chris Langholz - President Chicken - Tyson Foods | LinkedIn",                 "url": "https://www.linkedin.com/in/chrislangholz/"},
    {"title": "Noelle O'Mara - President International - Tyson Foods | LinkedIn",            "url": "https://www.linkedin.com/in/noelleomara-tyson/"},
    {"title": "Steve Stouffer - President Fresh Meats - Tyson Foods | LinkedIn",             "url": "https://www.linkedin.com/in/stevestouffer/"},
    {"title": "Brady Stewart - Chief People Officer - Tyson Foods | LinkedIn",               "url": "https://www.linkedin.com/in/bradystewart-tyson/"},
], min_required=3, max_keep=10))

print("AstraZeneca:", ingest_profiles("AstraZeneca", [
    {"title": "Pascal Soriot - CEO - AstraZeneca | LinkedIn",                                "url": "https://www.linkedin.com/in/pascalsoriot/"},
    {"title": "Aradhana Sarin - CFO - AstraZeneca | LinkedIn",                               "url": "https://www.linkedin.com/in/aradhanasarin/"},
    {"title": "Mene Pangalos - EVP Biopharmaceuticals R&D - AstraZeneca | LinkedIn",         "url": "https://www.linkedin.com/in/menepangalos/"},
    {"title": "Susan Galbraith - EVP Oncology R&D - AstraZeneca | LinkedIn",                 "url": "https://www.linkedin.com/in/susangalbraith-az/"},
    {"title": "Ruud Dobber - EVP Biopharmaceuticals Business - AstraZeneca | LinkedIn",      "url": "https://www.linkedin.com/in/ruuddobber/"},
    {"title": "Iskra Reic - EVP Europe and Canada - AstraZeneca | LinkedIn",                 "url": "https://www.linkedin.com/in/iskrereic/"},
    {"title": "Pam Cheng - EVP Global Operations - AstraZeneca | LinkedIn",                  "url": "https://www.linkedin.com/in/pamcheng-az/"},
    {"title": "Dave Fredrickson - EVP Oncology Business - AstraZeneca | LinkedIn",           "url": "https://www.linkedin.com/in/davefredrickson-az/"},
    {"title": "Fionnuala Moran - Chief People Officer - AstraZeneca | LinkedIn",             "url": "https://www.linkedin.com/in/fionnualamoran/"},
    {"title": "Mark Mallon - EVP BioPharmaceuticals - AstraZeneca | LinkedIn",               "url": "https://www.linkedin.com/in/markmallon-az/"},
], min_required=3, max_keep=10))

print("Bristol-Myers Squibb:", ingest_profiles("Bristol-Myers Squibb", [
    {"title": "Christopher Boerner - CEO - Bristol-Myers Squibb | LinkedIn",                 "url": "https://www.linkedin.com/in/christopherboerner-bms/"},
    {"title": "David Elkins - CFO - Bristol-Myers Squibb | LinkedIn",                        "url": "https://www.linkedin.com/in/davidelkins-bms/"},
    {"title": "Samit Hirawat - Chief Medical Officer - Bristol-Myers Squibb | LinkedIn",     "url": "https://www.linkedin.com/in/samithirawat/"},
    {"title": "Adam Lenkowsky - Chief Commercialization Officer - Bristol-Myers Squibb | LinkedIn","url": "https://www.linkedin.com/in/adamlenkowsky/"},
    {"title": "Giovanni Caforio - Executive Chairman - Bristol-Myers Squibb | LinkedIn",     "url": "https://www.linkedin.com/in/giovannibcaforio/"},
    {"title": "Robert Plenge - EVP Research - Bristol-Myers Squibb | LinkedIn",              "url": "https://www.linkedin.com/in/robertplenge/"},
    {"title": "Tom Lynch - EVP Chief Scientific Officer - Bristol-Myers Squibb | LinkedIn",  "url": "https://www.linkedin.com/in/tomlynch-bms/"},
    {"title": "Cynthia Guzzo - Chief People Officer - Bristol-Myers Squibb | LinkedIn",      "url": "https://www.linkedin.com/in/cynthiaguzzo/"},
    {"title": "Veronika von Niederhausern - EVP International - Bristol-Myers Squibb | LinkedIn","url": "https://www.linkedin.com/in/veronikavonniederhausern/"},
    {"title": "John Elicker - SVP Public Affairs - Bristol-Myers Squibb | LinkedIn",         "url": "https://www.linkedin.com/in/johnelicker/"},
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
