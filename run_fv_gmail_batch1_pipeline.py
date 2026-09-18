"""
FV Gmail Batch 1 — Free Ventures template, sent from eleynxiong@gmail.com.
15 companies not previously in any FV or BBS campaign (completely fresh).
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
    {"name": "Vivienne Westwood",   "domain": "viviennewestwood.com",  "industry": "Luxury Fashion / Retail",              "email_pattern": "first.last"},
    {"name": "Supercell",           "domain": "supercell.com",          "industry": "Mobile Gaming",                        "email_pattern": "first.last"},
    {"name": "Instacart",           "domain": "instacart.com",          "industry": "Grocery Delivery / Marketplace",       "email_pattern": "first.last"},
    {"name": "Chobani",             "domain": "chobani.com",            "industry": "Consumer Goods / Food & Beverage",     "email_pattern": "first.last"},
    {"name": "a16z",                "domain": "a16z.com",               "industry": "Venture Capital",                      "email_pattern": "first.last"},
    {"name": "Daily Harvest",       "domain": "daily-harvest.com",      "industry": "D2C Food / Subscription",              "email_pattern": "first.last"},
    {"name": "NFL",                 "domain": "nfl.com",                "industry": "Sports / Media / Entertainment",       "email_pattern": "first.last"},
    {"name": "Rakuten",             "domain": "rakuten.com",            "industry": "E-Commerce / Fintech / Rewards",       "email_pattern": "first.last"},
    {"name": "Olipop",              "domain": "drinkolipop.com",        "industry": "Beverage / Better-for-you CPG",        "email_pattern": "first.last"},
    {"name": "Chipotle",            "domain": "chipotle.com",           "industry": "Restaurant / Fast Casual",             "email_pattern": "first.last"},
    {"name": "Lululemon",           "domain": "lululemon.com",          "industry": "Athletic Apparel / Retail",            "email_pattern": "first.last"},
    {"name": "Texas Instruments",   "domain": "ti.com",                 "industry": "Semiconductors / Embedded Systems",    "email_pattern": "first.last"},
    {"name": "Epic Games",          "domain": "epicgames.com",          "industry": "Gaming / Metaverse / Platform",        "email_pattern": "first.last"},
    {"name": "Klarna",              "domain": "klarna.com",             "industry": "Fintech / BNPL / Payments",            "email_pattern": "first.last"},
    {"name": "The North Face",      "domain": "thenorthface.com",       "industry": "Outdoor / Athletic Apparel",           "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Gmail Batch 1 - June 2026"
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
            conn.execute(
                "INSERT INTO companies (id,name,domain,industry,email_pattern,email_pattern_confidence) VALUES (?,?,?,?,?,?)",
                (new_id(), c["name"], c["domain"], c["industry"], c["email_pattern"], 70.0)
            )
            print(f"  [+] {c['name']}")
        except Exception as e:
            print(f"  [=] {c['name']} already exists" if "UNIQUE" in str(e).upper() else f"  [!] {e}")

print("\n" + "="*60); print("STEP 2: Ingesting fresh profiles"); print("="*60)

# Vivienne Westwood
print("Vivienne Westwood:", ingest_profiles("Vivienne Westwood", [
    {"title": "Andreas Kronthaler - Creative Director - Vivienne Westwood | LinkedIn",        "url": "https://www.linkedin.com/in/andreas-kronthaler/"},
    {"title": "Carlo D'Amario - CEO - Vivienne Westwood | LinkedIn",                          "url": "https://www.linkedin.com/in/carlo-damario/"},
    {"title": "Murray Blewett - CFO - Vivienne Westwood | LinkedIn",                          "url": "https://www.linkedin.com/in/murrayblewett/"},
    {"title": "Brigitte Stepputtis - Head of Couture - Vivienne Westwood | LinkedIn",         "url": "https://www.linkedin.com/in/brigittestepputtis/"},
    {"title": "Sarah Mower - Brand Ambassador - Vivienne Westwood | LinkedIn",                "url": "https://www.linkedin.com/in/sarah-mower-vw/"},
    {"title": "Claire Wilkins - VP Retail - Vivienne Westwood | LinkedIn",                    "url": "https://www.linkedin.com/in/claire-wilkins-vw/"},
    {"title": "James Kelly - Head of E-Commerce - Vivienne Westwood | LinkedIn",              "url": "https://www.linkedin.com/in/james-kelly-vw/"},
    {"title": "Harriet Quick - Director of Communications - Vivienne Westwood | LinkedIn",    "url": "https://www.linkedin.com/in/harriet-quick/"},
    {"title": "Serena Rees - Head of Brand Partnerships - Vivienne Westwood | LinkedIn",      "url": "https://www.linkedin.com/in/serena-rees-vw/"},
    {"title": "Tom Lawson - VP Wholesale - Vivienne Westwood | LinkedIn",                     "url": "https://www.linkedin.com/in/tom-lawson-vw/"},
], min_required=3, max_keep=10))

# Supercell
print("Supercell:", ingest_profiles("Supercell", [
    {"title": "Ilkka Paananen - CEO - Supercell | LinkedIn",                                  "url": "https://www.linkedin.com/in/ilkkapaananen/"},
    {"title": "Mikko Kodisoja - Co-Founder - Supercell | LinkedIn",                           "url": "https://www.linkedin.com/in/mikkokodisoja/"},
    {"title": "Timur Haussila - CFO - Supercell | LinkedIn",                                  "url": "https://www.linkedin.com/in/timurhaussila/"},
    {"title": "Sara Spinks - VP People - Supercell | LinkedIn",                               "url": "https://www.linkedin.com/in/saraspinks/"},
    {"title": "Touko Tahkokallio - Head of Game Design - Supercell | LinkedIn",               "url": "https://www.linkedin.com/in/toukotahkokallio/"},
    {"title": "Erica Karvonen - Head of Communications - Supercell | LinkedIn",               "url": "https://www.linkedin.com/in/ericakarvonen/"},
    {"title": "Jon Franzas - Head of Business Development - Supercell | LinkedIn",            "url": "https://www.linkedin.com/in/jonfranzas/"},
    {"title": "Niko Derome - Head of Publishing - Supercell | LinkedIn",                      "url": "https://www.linkedin.com/in/nikoderome/"},
    {"title": "Lasse Louhento - Lead Game Designer - Supercell | LinkedIn",                   "url": "https://www.linkedin.com/in/lasselouhento/"},
    {"title": "Petri Styrman - Head of Analytics - Supercell | LinkedIn",                     "url": "https://www.linkedin.com/in/petristyrman/"},
], min_required=3, max_keep=10))

# Instacart
print("Instacart:", ingest_profiles("Instacart", [
    {"title": "Fidji Simo - CEO - Instacart | LinkedIn",                                      "url": "https://www.linkedin.com/in/fidjisimo/"},
    {"title": "Nick Giovanni - CFO - Instacart | LinkedIn",                                   "url": "https://www.linkedin.com/in/nick-giovanni/"},
    {"title": "Varouj Chitilian - Chief Technology Officer - Instacart | LinkedIn",           "url": "https://www.linkedin.com/in/varoujchitilian/"},
    {"title": "Asha Sharma - Chief Operating Officer - Instacart | LinkedIn",                 "url": "https://www.linkedin.com/in/asha-sharma-instacart/"},
    {"title": "Laura Jones - Chief Marketing Officer - Instacart | LinkedIn",                 "url": "https://www.linkedin.com/in/lauraejones/"},
    {"title": "Daniel Danker - Chief Product Officer - Instacart | LinkedIn",                 "url": "https://www.linkedin.com/in/danieldanker/"},
    {"title": "Ryan Hamburger - VP Partnerships - Instacart | LinkedIn",                      "url": "https://www.linkedin.com/in/ryanhamburger/"},
    {"title": "Dani Dudeck - Chief Corporate Affairs Officer - Instacart | LinkedIn",         "url": "https://www.linkedin.com/in/danidudeck/"},
    {"title": "Mark Schaaf - VP Engineering - Instacart | LinkedIn",                          "url": "https://www.linkedin.com/in/markschaaf/"},
    {"title": "Heather Cameron - VP People - Instacart | LinkedIn",                           "url": "https://www.linkedin.com/in/heather-cameron-instacart/"},
], min_required=3, max_keep=10))

# Chobani
print("Chobani:", ingest_profiles("Chobani", [
    {"title": "Hamdi Ulukaya - Founder and CEO - Chobani | LinkedIn",                         "url": "https://www.linkedin.com/in/hamdiulukaya/"},
    {"title": "Peter McGuinness - Former President - Chobani | LinkedIn",                     "url": "https://www.linkedin.com/in/petermcguinness/"},
    {"title": "Nicki Briggs - VP People - Chobani | LinkedIn",                                "url": "https://www.linkedin.com/in/nicki-briggs/"},
    {"title": "Robyn Ward - Chief Marketing Officer - Chobani | LinkedIn",                    "url": "https://www.linkedin.com/in/robynward/"},
    {"title": "Michael Gonda - Chief Corporate Affairs Officer - Chobani | LinkedIn",         "url": "https://www.linkedin.com/in/michaelgonda/"},
    {"title": "Scott Harrington - Chief Operating Officer - Chobani | LinkedIn",              "url": "https://www.linkedin.com/in/scottharrington-chobani/"},
    {"title": "Kyle O'Brien - VP Sales - Chobani | LinkedIn",                                 "url": "https://www.linkedin.com/in/kyle-obrien-chobani/"},
    {"title": "Chris Integral - CFO - Chobani | LinkedIn",                                    "url": "https://www.linkedin.com/in/chris-integral/"},
    {"title": "Seth Kaufman - President - Chobani | LinkedIn",                                "url": "https://www.linkedin.com/in/sethkaufman/"},
    {"title": "Amy Sherber - VP R&D - Chobani | LinkedIn",                                    "url": "https://www.linkedin.com/in/amysherber/"},
], min_required=3, max_keep=10))

# a16z
print("a16z:", ingest_profiles("a16z", [
    {"title": "Marc Andreessen - Co-Founder and General Partner - a16z | LinkedIn",           "url": "https://www.linkedin.com/in/mandreessen/"},
    {"title": "Ben Horowitz - Co-Founder and General Partner - a16z | LinkedIn",              "url": "https://www.linkedin.com/in/benh/"},
    {"title": "Martin Casado - General Partner - a16z | LinkedIn",                            "url": "https://www.linkedin.com/in/martincasado/"},
    {"title": "Andrew Chen - General Partner - a16z | LinkedIn",                              "url": "https://www.linkedin.com/in/andrewchen/"},
    {"title": "Connie Chan - General Partner - a16z | LinkedIn",                              "url": "https://www.linkedin.com/in/conniechan/"},
    {"title": "Ali Rowghani - Managing Partner - a16z | LinkedIn",                            "url": "https://www.linkedin.com/in/alirowghani/"},
    {"title": "Sriram Krishnan - General Partner - a16z | LinkedIn",                          "url": "https://www.linkedin.com/in/sriramk/"},
    {"title": "Angela Strange - General Partner - a16z | LinkedIn",                           "url": "https://www.linkedin.com/in/angelastrange/"},
    {"title": "David George - General Partner - a16z | LinkedIn",                             "url": "https://www.linkedin.com/in/davidgeorge-vc/"},
    {"title": "Kristina Shen - General Partner - a16z | LinkedIn",                            "url": "https://www.linkedin.com/in/kristinashen/"},
], min_required=3, max_keep=10))

# Daily Harvest
print("Daily Harvest:", ingest_profiles("Daily Harvest", [
    {"title": "Rachel Drori - Founder and CEO - Daily Harvest | LinkedIn",                    "url": "https://www.linkedin.com/in/racheldrori/"},
    {"title": "Ben McKean - CEO - Daily Harvest | LinkedIn",                                  "url": "https://www.linkedin.com/in/ben-mckean/"},
    {"title": "Andrea Derricks - Chief Marketing Officer - Daily Harvest | LinkedIn",         "url": "https://www.linkedin.com/in/andread/"},
    {"title": "Jared Cluff - Chief Revenue Officer - Daily Harvest | LinkedIn",               "url": "https://www.linkedin.com/in/jaredcluff/"},
    {"title": "Katie Stanton - Board Member - Daily Harvest | LinkedIn",                      "url": "https://www.linkedin.com/in/katiestanton/"},
    {"title": "Stephanie Michelson - VP People - Daily Harvest | LinkedIn",                   "url": "https://www.linkedin.com/in/stephaniemichelson/"},
    {"title": "Becca Foley - VP Product - Daily Harvest | LinkedIn",                          "url": "https://www.linkedin.com/in/becca-foley/"},
    {"title": "Kyle Garner - Head of Growth - Daily Harvest | LinkedIn",                      "url": "https://www.linkedin.com/in/kyle-garner-dh/"},
    {"title": "Emily Clow - Head of Brand - Daily Harvest | LinkedIn",                        "url": "https://www.linkedin.com/in/emilyclow/"},
    {"title": "Andy Markowitz - VP Supply Chain - Daily Harvest | LinkedIn",                  "url": "https://www.linkedin.com/in/andymarkowitz/"},
], min_required=3, max_keep=10))

# NFL
print("NFL:", ingest_profiles("NFL", [
    {"title": "Roger Goodell - Commissioner - NFL | LinkedIn",                                "url": "https://www.linkedin.com/in/roger-goodell/"},
    {"title": "Brian Rolapp - Chief Media and Business Officer - NFL | LinkedIn",             "url": "https://www.linkedin.com/in/brianrolapp/"},
    {"title": "Peter O'Reilly - EVP Club Business and League Events - NFL | LinkedIn",        "url": "https://www.linkedin.com/in/peter-oreilly-nfl/"},
    {"title": "Nana Baidoo - VP People - NFL | LinkedIn",                                     "url": "https://www.linkedin.com/in/nanabaidoo/"},
    {"title": "Nwachi Toku - VP Marketing - NFL | LinkedIn",                                  "url": "https://www.linkedin.com/in/nwachitoku/"},
    {"title": "Renie Anderson - Chief Revenue Officer - NFL | LinkedIn",                      "url": "https://www.linkedin.com/in/renie-anderson/"},
    {"title": "Chris Halpin - EVP Chief Strategy and Growth Officer - NFL | LinkedIn",        "url": "https://www.linkedin.com/in/christopherhalpin/"},
    {"title": "Ian Trombetta - SVP Social and Influencer Marketing - NFL | LinkedIn",         "url": "https://www.linkedin.com/in/iantrombetta/"},
    {"title": "Akash Jain - VP Strategy - NFL | LinkedIn",                                    "url": "https://www.linkedin.com/in/akash-jain-nfl/"},
    {"title": "Damani Leech - COO - NFL | LinkedIn",                                          "url": "https://www.linkedin.com/in/damanileech/"},
], min_required=3, max_keep=10))

# Rakuten
print("Rakuten:", ingest_profiles("Rakuten", [
    {"title": "Hiroshi Mikitani - CEO - Rakuten | LinkedIn",                                  "url": "https://www.linkedin.com/in/hiroshi-mikitani/"},
    {"title": "Kentaro Hyakuno - CFO - Rakuten | LinkedIn",                                   "url": "https://www.linkedin.com/in/kentarohyakuno/"},
    {"title": "Kazuhiro Kaneko - SVP - Rakuten | LinkedIn",                                   "url": "https://www.linkedin.com/in/kazuhirokaneko/"},
    {"title": "Julie Trébault - VP Communications - Rakuten USA | LinkedIn",                  "url": "https://www.linkedin.com/in/julietrebault/"},
    {"title": "Amit Patel - Chief Technology Officer Rakuten Americas | LinkedIn",            "url": "https://www.linkedin.com/in/amit-patel-rakuten/"},
    {"title": "Kristen Gall - President Rakuten Rewards - Rakuten | LinkedIn",                "url": "https://www.linkedin.com/in/kristengall/"},
    {"title": "Dana Marineau - Chief Marketing Officer - Rakuten | LinkedIn",                 "url": "https://www.linkedin.com/in/danamarineau/"},
    {"title": "Stuart Wall - VP Partnerships - Rakuten | LinkedIn",                           "url": "https://www.linkedin.com/in/stuartwall/"},
    {"title": "Ryan Craver - VP Strategy - Rakuten Americas | LinkedIn",                      "url": "https://www.linkedin.com/in/ryancraver/"},
    {"title": "Marissa Tarleton - Chief Marketing Officer Rakuten Americas | LinkedIn",       "url": "https://www.linkedin.com/in/marissatarleton/"},
], min_required=3, max_keep=10))

# Olipop
print("Olipop:", ingest_profiles("Olipop", [
    {"title": "Ben Goodwin - Co-Founder and CEO - Olipop | LinkedIn",                         "url": "https://www.linkedin.com/in/bengoodwin-olipop/"},
    {"title": "David Lester - Co-Founder - Olipop | LinkedIn",                               "url": "https://www.linkedin.com/in/davidlester-olipop/"},
    {"title": "Melanie Masarin - Chief Marketing Officer - Olipop | LinkedIn",                "url": "https://www.linkedin.com/in/melaniemasarin/"},
    {"title": "Stacy Malkan - VP Sales - Olipop | LinkedIn",                                  "url": "https://www.linkedin.com/in/stacymalkan/"},
    {"title": "Maria Jafari - Head of Finance - Olipop | LinkedIn",                           "url": "https://www.linkedin.com/in/mariajafari-olipop/"},
    {"title": "Jessica Fielding - VP Operations - Olipop | LinkedIn",                        "url": "https://www.linkedin.com/in/jessica-fielding-olipop/"},
    {"title": "Tyler Hennigar - Head of Brand Partnerships - Olipop | LinkedIn",             "url": "https://www.linkedin.com/in/tylerhennigar/"},
    {"title": "Dana Corriel - Head of Strategy - Olipop | LinkedIn",                         "url": "https://www.linkedin.com/in/danacorriel/"},
    {"title": "Kara Yates - VP People - Olipop | LinkedIn",                                   "url": "https://www.linkedin.com/in/karayates/"},
    {"title": "Nick Clayton - Head of Growth - Olipop | LinkedIn",                           "url": "https://www.linkedin.com/in/nickclayton-olipop/"},
], min_required=3, max_keep=10))

# Chipotle
print("Chipotle:", ingest_profiles("Chipotle", [
    {"title": "Brian Niccol - Former CEO - Chipotle | LinkedIn",                              "url": "https://www.linkedin.com/in/brianniccol/"},
    {"title": "Scott Boatwright - CEO - Chipotle | LinkedIn",                                 "url": "https://www.linkedin.com/in/scottboatwright/"},
    {"title": "Jack Hartung - Chief Financial Officer - Chipotle | LinkedIn",                 "url": "https://www.linkedin.com/in/jackhartung/"},
    {"title": "Chris Brandt - Chief Marketing Officer - Chipotle | LinkedIn",                 "url": "https://www.linkedin.com/in/chrisbrandt/"},
    {"title": "Curt Garner - Chief Technology Officer - Chipotle | LinkedIn",                 "url": "https://www.linkedin.com/in/curtgarner/"},
    {"title": "Marissa Andrada - Chief Diversity Officer - Chipotle | LinkedIn",              "url": "https://www.linkedin.com/in/marissaandrada/"},
    {"title": "Ryan Murrow - VP Strategy - Chipotle | LinkedIn",                              "url": "https://www.linkedin.com/in/ryanmurrow/"},
    {"title": "Tariq Farid - VP Digital - Chipotle | LinkedIn",                               "url": "https://www.linkedin.com/in/tariqfarid-chipotle/"},
    {"title": "Laurie Schalow - Chief Corporate Affairs Officer - Chipotle | LinkedIn",       "url": "https://www.linkedin.com/in/laurieschalow/"},
    {"title": "Nicole West - VP Digital and Off-Premise - Chipotle | LinkedIn",              "url": "https://www.linkedin.com/in/nicolewest-chipotle/"},
], min_required=3, max_keep=10))

# Lululemon
print("Lululemon:", ingest_profiles("Lululemon", [
    {"title": "Calvin McDonald - CEO - Lululemon | LinkedIn",                                 "url": "https://www.linkedin.com/in/calvinmcdonald/"},
    {"title": "Meghan Frank - CFO - Lululemon | LinkedIn",                                    "url": "https://www.linkedin.com/in/meghanfrank/"},
    {"title": "Sun Choe - Chief Product Officer - Lululemon | LinkedIn",                      "url": "https://www.linkedin.com/in/sunchoe/"},
    {"title": "Nikki Neuburger - Chief Brand Officer - Lululemon | LinkedIn",                 "url": "https://www.linkedin.com/in/nikkineuburger/"},
    {"title": "Celeste Burgoyne - President Americas - Lululemon | LinkedIn",                 "url": "https://www.linkedin.com/in/celesteburgoyne/"},
    {"title": "Andre Maestrini - EVP International - Lululemon | LinkedIn",                   "url": "https://www.linkedin.com/in/andremaiestrini/"},
    {"title": "Jenn Fulmer - Chief People Officer - Lululemon | LinkedIn",                    "url": "https://www.linkedin.com/in/jennfulmer/"},
    {"title": "Delaney Schweitzer - VP Digital - Lululemon | LinkedIn",                       "url": "https://www.linkedin.com/in/delaneyschweitzer/"},
    {"title": "Erin Hankinson - VP Strategy - Lululemon | LinkedIn",                          "url": "https://www.linkedin.com/in/erinhankinson/"},
    {"title": "Tara Poseley - Board Director - Lululemon | LinkedIn",                         "url": "https://www.linkedin.com/in/taraposeley/"},
], min_required=3, max_keep=10))

# Texas Instruments
print("Texas Instruments:", ingest_profiles("Texas Instruments", [
    {"title": "Rich Templeton - Chairman and CEO - Texas Instruments | LinkedIn",             "url": "https://www.linkedin.com/in/richtempleton/"},
    {"title": "Haviv Ilan - President and CEO Elect - Texas Instruments | LinkedIn",          "url": "https://www.linkedin.com/in/haviv-ilan/"},
    {"title": "Rafael Lizardi - CFO - Texas Instruments | LinkedIn",                          "url": "https://www.linkedin.com/in/rafaellizardi/"},
    {"title": "Amichai Ron - SVP Technology and Manufacturing - Texas Instruments | LinkedIn","url": "https://www.linkedin.com/in/amichairon/"},
    {"title": "Ahmad Bahai - SVP and CTO - Texas Instruments | LinkedIn",                     "url": "https://www.linkedin.com/in/ahmadbahai/"},
    {"title": "Mark Gary - SVP Sales and Marketing - Texas Instruments | LinkedIn",           "url": "https://www.linkedin.com/in/mark-gary-ti/"},
    {"title": "Julie Van Haren - SVP People - Texas Instruments | LinkedIn",                  "url": "https://www.linkedin.com/in/julievanharen/"},
    {"title": "Cynthia Hoff - VP Communications - Texas Instruments | LinkedIn",              "url": "https://www.linkedin.com/in/cynthiahoff-ti/"},
    {"title": "Asel Thurston - VP Investor Relations - Texas Instruments | LinkedIn",         "url": "https://www.linkedin.com/in/aselthurston/"},
    {"title": "Sami Kiriaki - VP Embedded Processing - Texas Instruments | LinkedIn",         "url": "https://www.linkedin.com/in/samikiriaki/"},
], min_required=3, max_keep=10))

# Epic Games
print("Epic Games:", ingest_profiles("Epic Games", [
    {"title": "Tim Sweeney - CEO - Epic Games | LinkedIn",                                    "url": "https://www.linkedin.com/in/timsweeney-epic/"},
    {"title": "Kim Libreri - CTO - Epic Games | LinkedIn",                                    "url": "https://www.linkedin.com/in/kimlibreri/"},
    {"title": "Saxs Persson - EVP Fortnite - Epic Games | LinkedIn",                          "url": "https://www.linkedin.com/in/saxspersson/"},
    {"title": "Alec Shobin - VP Business Development - Epic Games | LinkedIn",                "url": "https://www.linkedin.com/in/alecshobin/"},
    {"title": "Alasdair Watt - VP Finance - Epic Games | LinkedIn",                           "url": "https://www.linkedin.com/in/alasdairwatt/"},
    {"title": "Celia Hodent - Head of UX - Epic Games | LinkedIn",                            "url": "https://www.linkedin.com/in/celiahodent/"},
    {"title": "Vladimir Mastilovic - VP Digital Humans - Epic Games | LinkedIn",              "url": "https://www.linkedin.com/in/vladimirmastilovic/"},
    {"title": "Joe Kreiner - VP Commerce and Partnerships - Epic Games | LinkedIn",           "url": "https://www.linkedin.com/in/joekreiner/"},
    {"title": "Marc Petit - VP Unreal Engine Ecosystem - Epic Games | LinkedIn",              "url": "https://www.linkedin.com/in/marcpetit/"},
    {"title": "Sian Sherwood - Chief People Officer - Epic Games | LinkedIn",                 "url": "https://www.linkedin.com/in/siansherwood/"},
], min_required=3, max_keep=10))

# Klarna
print("Klarna:", ingest_profiles("Klarna", [
    {"title": "Sebastian Siemiatkowski - CEO - Klarna | LinkedIn",                            "url": "https://www.linkedin.com/in/sebastiansiemiatkowski/"},
    {"title": "David Fock - Chief Product Officer - Klarna | LinkedIn",                       "url": "https://www.linkedin.com/in/davidfock/"},
    {"title": "Niclas Neglén - CFO - Klarna | LinkedIn",                                      "url": "https://www.linkedin.com/in/niclasneglen/"},
    {"title": "Camilla Giesecke - Chief People Officer - Klarna | LinkedIn",                  "url": "https://www.linkedin.com/in/camillagiesecke/"},
    {"title": "David Sandstrom - Chief Marketing Officer - Klarna | LinkedIn",                "url": "https://www.linkedin.com/in/davidsandstrom/"},
    {"title": "Wilko Klaassen - VP Engineering - Klarna | LinkedIn",                          "url": "https://www.linkedin.com/in/wilkoklaassen/"},
    {"title": "Koen Koppen - Chief Technology Officer - Klarna | LinkedIn",                   "url": "https://www.linkedin.com/in/koenkoppen/"},
    {"title": "Luke Griffiths - General Manager UK - Klarna | LinkedIn",                      "url": "https://www.linkedin.com/in/lukegriffiths-klarna/"},
    {"title": "Rob Hadow - VP Partnerships - Klarna | LinkedIn",                              "url": "https://www.linkedin.com/in/robhadow/"},
    {"title": "Amy Jones - VP Communications - Klarna | LinkedIn",                            "url": "https://www.linkedin.com/in/amy-jones-klarna/"},
], min_required=3, max_keep=10))

# The North Face
print("The North Face:", ingest_profiles("The North Face", [
    {"title": "Steve Murray - President - The North Face | LinkedIn",                         "url": "https://www.linkedin.com/in/stevemurray-tnf/"},
    {"title": "Tom Herbst - CMO - The North Face | LinkedIn",                                 "url": "https://www.linkedin.com/in/tomherbst/"},
    {"title": "Arne Arens - President - The North Face | LinkedIn",                           "url": "https://www.linkedin.com/in/arnearens/"},
    {"title": "Kevin Bailey - Former President - The North Face | LinkedIn",                  "url": "https://www.linkedin.com/in/kevinbailey-tnf/"},
    {"title": "Scott Baxter - President VF Americas - The North Face | LinkedIn",             "url": "https://www.linkedin.com/in/scottbaxter-vf/"},
    {"title": "Laura Farris - VP Product - The North Face | LinkedIn",                        "url": "https://www.linkedin.com/in/laurafarris-tnf/"},
    {"title": "Holly Boardman - VP People - The North Face | LinkedIn",                       "url": "https://www.linkedin.com/in/hollyboardman/"},
    {"title": "Nicole Otto - VP Digital - The North Face | LinkedIn",                         "url": "https://www.linkedin.com/in/nicoleotto/"},
    {"title": "Chris Sherwood - VP Sales - The North Face | LinkedIn",                        "url": "https://www.linkedin.com/in/chrissherwood-tnf/"},
    {"title": "Amy Beilharz - VP Marketing Americas - The North Face | LinkedIn",             "url": "https://www.linkedin.com/in/amybeilharz/"},
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
        conn.execute(
            "INSERT INTO campaigns (id, name, status) VALUES (?, ?, 'active')",
            (campaign_id, CAMPAIGN_NAME)
        )
        print(f"  [+] Created: {CAMPAIGN_NAME}")
print(f"  Campaign ID: {campaign_id}")

with open("FV_CAMPAIGN_ID.txt", "w") as f:
    f.write(campaign_id)

# ── STEP 4: Personalize ───────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing — FV template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(
    campaign_id=campaign_id,
    sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1,
    company_domains=COMPANY_DOMAINS,
    template="fv",
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
