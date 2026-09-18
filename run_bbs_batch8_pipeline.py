"""BBS Batch 8 — 25 new Fortune 500 companies, 10 emails each, eleynxiong@berkeley.edu."""
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
    {"name": "Nucor",                   "domain": "nucor.com",                  "industry": "Steel Manufacturing / Recycling / Construction Materials",   "email_pattern": "first.last"},
    {"name": "LyondellBasell",          "domain": "lyondellbasell.com",         "industry": "Petrochemicals / Polymers / Refining / Clean Fuels",          "email_pattern": "first.last"},
    {"name": "Celanese",                "domain": "celanese.com",               "industry": "Specialty Chemicals / Engineered Materials / Acetate",         "email_pattern": "first.last"},
    {"name": "Air Products",            "domain": "airproducts.com",            "industry": "Industrial Gases / Clean Hydrogen / Clean Energy",            "email_pattern": "first.last"},
    {"name": "Avery Dennison",          "domain": "averydennison.com",          "industry": "Materials Science / Labeling / RFID / Packaging",             "email_pattern": "first.last"},
    {"name": "Snap-on",                 "domain": "snapon.com",                 "industry": "Professional Tools / Diagnostics / Equipment",                "email_pattern": "first.last"},
    {"name": "Dover Corporation",       "domain": "dovercorporation.com",       "industry": "Industrial Diversified / Pumps / Digital Printing / Retail",  "email_pattern": "first.last"},
    {"name": "AGCO Corporation",        "domain": "agcocorp.com",               "industry": "Agricultural Equipment / Precision Ag / Machinery",           "email_pattern": "first.last"},
    {"name": "VF Corporation",          "domain": "vfc.com",                    "industry": "Apparel / Footwear Brands (Vans, Timberland, Supreme)",        "email_pattern": "first.last"},
    {"name": "PVH Corp",                "domain": "pvh.com",                    "industry": "Fashion (Calvin Klein, Tommy Hilfiger) / Retail / Wholesale", "email_pattern": "first.last"},
    {"name": "Tapestry",                "domain": "tapestry.com",               "industry": "Luxury Accessories (Coach, Kate Spade, Stuart Weitzman)",      "email_pattern": "first.last"},
    {"name": "Bath and Body Works",     "domain": "bathandbodyworks.com",       "industry": "Personal Care / Fragrance / Specialty Retail",                "email_pattern": "first.last"},
    {"name": "Dick's Sporting Goods",   "domain": "dickssportinggoods.com",     "industry": "Sporting Goods / Outdoor / Fitness Retail",                   "email_pattern": "first.last"},
    {"name": "Foot Locker",             "domain": "footlocker.com",             "industry": "Footwear / Athletic Retail / Sneaker Marketplace",            "email_pattern": "first.last"},
    {"name": "Tractor Supply",          "domain": "tractorsupply.com",          "industry": "Rural Lifestyle / Farm / Pet / Home Improvement Retail",       "email_pattern": "first.last"},
    {"name": "Campbell Soup Company",   "domain": "campbellsoupcompany.com",    "industry": "Packaged Food / Soup / Snacks / Beverages",                   "email_pattern": "first.last"},
    {"name": "McCormick",               "domain": "mccormick.com",              "industry": "Spices / Condiments / Flavors / Seasonings",                  "email_pattern": "first.last"},
    {"name": "Hormel Foods",            "domain": "hormel.com",                 "industry": "Packaged Meat / Food Products / Brands",                      "email_pattern": "first.last"},
    {"name": "CBRE Group",              "domain": "cbre.com",                   "industry": "Commercial Real Estate / Advisory / Investment Management",    "email_pattern": "first.last"},
    {"name": "Jones Lang LaSalle",      "domain": "jll.com",                    "industry": "Real Estate Services / Property Management / Investment",      "email_pattern": "first.last"},
    {"name": "Iron Mountain",           "domain": "ironmountain.com",           "industry": "Data Storage / Records Management / Digital Transformation",  "email_pattern": "first.last"},
    {"name": "DXC Technology",          "domain": "dxc.com",                    "industry": "IT Services / Digital Transformation / Cloud / BPO",          "email_pattern": "first.last"},
    {"name": "Concentrix",              "domain": "concentrix.com",             "industry": "Customer Experience / BPO / CX Technology / Analytics",        "email_pattern": "first.last"},
    {"name": "Zimmer Biomet",           "domain": "zimmerbiomet.com",           "industry": "Orthopedic Medical Devices / Musculoskeletal Health",          "email_pattern": "first.last"},
    {"name": "Hologic",                 "domain": "hologic.com",                "industry": "Women's Health / Medical Devices / Diagnostics / Imaging",    "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 8 - July 2026"
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

print("Nucor:", ingest_profiles("Nucor", [
    {"title": "Leon Topalian - President and CEO - Nucor Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/leontopalian/"},
    {"title": "Steve Laxton - EVP and CFO - Nucor Corporation | LinkedIn",                         "url": "https://www.linkedin.com/in/stevelaxton-nucor/"},
    {"title": "MaryEmily Slate - EVP - Nucor Corporation | LinkedIn",                              "url": "https://www.linkedin.com/in/maryemilyslate/"},
    {"title": "Doug Jellison - VP Finance and CFO - Nucor Corporation | LinkedIn",                 "url": "https://www.linkedin.com/in/dougjellison-nucor/"},
    {"title": "Ladd Hall - EVP Downstream Products - Nucor Corporation | LinkedIn",                "url": "https://www.linkedin.com/in/laddhall-nucor/"},
    {"title": "Rex Query - EVP Sheet and Tubular Products - Nucor Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/rexquery-nucor/"},
    {"title": "Joseph Stratman - VP Investor Relations - Nucor Corporation | LinkedIn",            "url": "https://www.linkedin.com/in/josephstratman-nucor/"},
    {"title": "Amy Williams - Chief HR Officer - Nucor Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/amywilliams-nucor/"},
    {"title": "Chad Utermark - EVP New Markets and Industries - Nucor Corporation | LinkedIn",     "url": "https://www.linkedin.com/in/chadutermark-nucor/"},
    {"title": "Brad Ford - SVP Strategy - Nucor Corporation | LinkedIn",                           "url": "https://www.linkedin.com/in/bradford-nucor/"},
], min_required=3, max_keep=10))

print("LyondellBasell:", ingest_profiles("LyondellBasell", [
    {"title": "Peter Vanacker - CEO - LyondellBasell | LinkedIn",                                  "url": "https://www.linkedin.com/in/petervanacker/"},
    {"title": "Michael McMurray - EVP and CFO - LyondellBasell | LinkedIn",                        "url": "https://www.linkedin.com/in/michaelmcmurray-lyb/"},
    {"title": "Torkel Rhenman - EVP and COO - LyondellBasell | LinkedIn",                          "url": "https://www.linkedin.com/in/torkelrhenman/"},
    {"title": "Ken Lane - EVP Global Olefins and Polyolefins Americas - LyondellBasell | LinkedIn","url": "https://www.linkedin.com/in/kenlane-lyb/"},
    {"title": "Yvonne van der Linden - EVP and CHRO - LyondellBasell | LinkedIn",                  "url": "https://www.linkedin.com/in/yvonnevanderlinden-lyb/"},
    {"title": "James Guiliano - SVP Strategy and Digital - LyondellBasell | LinkedIn",             "url": "https://www.linkedin.com/in/jamesguiliano-lyb/"},
    {"title": "Jeffrey Kaplan - SVP and General Counsel - LyondellBasell | LinkedIn",              "url": "https://www.linkedin.com/in/jeffreykaplan-lyb/"},
    {"title": "Massimo Covezzi - EVP R&D and Technology - LyondellBasell | LinkedIn",              "url": "https://www.linkedin.com/in/massimocovezzi/"},
    {"title": "Neil Carr - EVP Circular and Low Carbon Solutions - LyondellBasell | LinkedIn",     "url": "https://www.linkedin.com/in/neilcarr-lyb/"},
    {"title": "David Kinney - VP Investor Relations - LyondellBasell | LinkedIn",                  "url": "https://www.linkedin.com/in/davidkinney-lyb/"},
], min_required=3, max_keep=10))

print("Celanese:", ingest_profiles("Celanese", [
    {"title": "Lori Ryerkerk - Chairman and CEO - Celanese | LinkedIn",                            "url": "https://www.linkedin.com/in/loriryerkerk/"},
    {"title": "Scott Richardson - EVP and CFO - Celanese | LinkedIn",                              "url": "https://www.linkedin.com/in/scottrichardson-celanese/"},
    {"title": "Chuck Kyrish - VP and Treasurer - Celanese | LinkedIn",                             "url": "https://www.linkedin.com/in/chuckkyrish-celanese/"},
    {"title": "Ashley Duffie - VP and General Counsel - Celanese | LinkedIn",                      "url": "https://www.linkedin.com/in/ashleyduffie-celanese/"},
    {"title": "Tom Kelly - SVP Engineered Materials - Celanese | LinkedIn",                        "url": "https://www.linkedin.com/in/tomkelly-celanese/"},
    {"title": "Sameer Bhargava - EVP Acetyls - Celanese | LinkedIn",                               "url": "https://www.linkedin.com/in/sameerbhargava-celanese/"},
    {"title": "Brandon Sellers - VP Investor Relations - Celanese | LinkedIn",                     "url": "https://www.linkedin.com/in/brandonsellers-celanese/"},
    {"title": "Kim Wehrenberg - EVP Chief HR Officer - Celanese | LinkedIn",                       "url": "https://www.linkedin.com/in/kimwehrenberg-celanese/"},
    {"title": "Michael Sansoucy - SVP Supply Chain - Celanese | LinkedIn",                         "url": "https://www.linkedin.com/in/michaelsansoucy-celanese/"},
    {"title": "Leland Weaver - SVP Strategy - Celanese | LinkedIn",                                "url": "https://www.linkedin.com/in/lelandweaver-celanese/"},
], min_required=3, max_keep=10))

print("Air Products:", ingest_profiles("Air Products", [
    {"title": "Seifi Ghasemi - Chairman President and CEO - Air Products | LinkedIn",               "url": "https://www.linkedin.com/in/seifighasemi/"},
    {"title": "Michael Siesser - SVP and CFO - Air Products | LinkedIn",                           "url": "https://www.linkedin.com/in/michaelsiesser-airproducts/"},
    {"title": "Samir Serhan - COO - Air Products | LinkedIn",                                      "url": "https://www.linkedin.com/in/samirserhan/"},
    {"title": "Sean Major - EVP General Counsel and Secretary - Air Products | LinkedIn",           "url": "https://www.linkedin.com/in/seanmajor-airproducts/"},
    {"title": "Jennifer Grant - SVP Chief HR Officer - Air Products | LinkedIn",                   "url": "https://www.linkedin.com/in/jennifergrant-airproducts/"},
    {"title": "Russell Flugel - VP Investor Relations - Air Products | LinkedIn",                  "url": "https://www.linkedin.com/in/russellflugel-airproducts/"},
    {"title": "Felix Rambert - SVP Europe and Africa - Air Products | LinkedIn",                   "url": "https://www.linkedin.com/in/felixrambert-airproducts/"},
    {"title": "Sunita Bhatt - SVP Asia - Air Products | LinkedIn",                                 "url": "https://www.linkedin.com/in/sunitabhatt-airproducts/"},
    {"title": "Mike Ressner - VP Industrial Gases Americas - Air Products | LinkedIn",             "url": "https://www.linkedin.com/in/mikeressner-airproducts/"},
    {"title": "Stacy Krause - SVP Strategy and Corporate Dev - Air Products | LinkedIn",           "url": "https://www.linkedin.com/in/stacykrause-airproducts/"},
], min_required=3, max_keep=10))

print("Avery Dennison:", ingest_profiles("Avery Dennison", [
    {"title": "Mitchell Butier - Chairman and CEO - Avery Dennison | LinkedIn",                    "url": "https://www.linkedin.com/in/mitchellbutier/"},
    {"title": "Gregory Lovins - SVP and CFO - Avery Dennison | LinkedIn",                          "url": "https://www.linkedin.com/in/gregorylovins/"},
    {"title": "Deon Stander - President and COO - Avery Dennison | LinkedIn",                      "url": "https://www.linkedin.com/in/deonstander/"},
    {"title": "Lori Templeton - SVP and General Counsel - Avery Dennison | LinkedIn",              "url": "https://www.linkedin.com/in/loritempleton-averydennison/"},
    {"title": "Michael Barber - SVP Chief HR Officer - Avery Dennison | LinkedIn",                 "url": "https://www.linkedin.com/in/michaelbarber-averydennison/"},
    {"title": "Georges Gravanis - SVP President Label and Graphic Materials - AD | LinkedIn",      "url": "https://www.linkedin.com/in/georgesgravanis/"},
    {"title": "Nick Colisto - VP and CIO - Avery Dennison | LinkedIn",                             "url": "https://www.linkedin.com/in/nickcolisto/"},
    {"title": "Christopher Horton - VP Investor Relations - Avery Dennison | LinkedIn",            "url": "https://www.linkedin.com/in/christopherhorton-averydennison/"},
    {"title": "Jeff Cyrkin - VP Strategy - Avery Dennison | LinkedIn",                             "url": "https://www.linkedin.com/in/jeffcyrkin-averydennison/"},
    {"title": "Rob Rhoads - President Retail Branding and Information Solutions - AD | LinkedIn",  "url": "https://www.linkedin.com/in/robrhoads-averydennison/"},
], min_required=3, max_keep=10))

print("Snap-on:", ingest_profiles("Snap-on", [
    {"title": "Nicholas Pinchuk - Chairman and CEO - Snap-on | LinkedIn",                          "url": "https://www.linkedin.com/in/nicholaspinchuk/"},
    {"title": "Aldo Pagliari - SVP Finance and CFO - Snap-on | LinkedIn",                          "url": "https://www.linkedin.com/in/aldopagliari/"},
    {"title": "Irwin Shur - VP General Counsel - Snap-on | LinkedIn",                              "url": "https://www.linkedin.com/in/irwinshur-snapon/"},
    {"title": "Thomas Mahoney - SVP HR - Snap-on | LinkedIn",                                      "url": "https://www.linkedin.com/in/thomasmahoney-snapon/"},
    {"title": "Jeanne Brady - VP IT and CIO - Snap-on | LinkedIn",                                 "url": "https://www.linkedin.com/in/jeannebrady-snapon/"},
    {"title": "Hy Grossman - SVP and President Commercial and Industrial Group - Snap-on | LinkedIn","url": "https://www.linkedin.com/in/hygrossman-snapon/"},
    {"title": "Walter Shepherd - SVP and President Snap-on Tools Group | LinkedIn",                "url": "https://www.linkedin.com/in/waltershepherd-snapon/"},
    {"title": "Hannu Ylanko - President Snap-on Equipment - Snap-on | LinkedIn",                   "url": "https://www.linkedin.com/in/hannuylanko-snapon/"},
    {"title": "Brad Tuohy - VP Investor Relations - Snap-on | LinkedIn",                           "url": "https://www.linkedin.com/in/bradtuohy-snapon/"},
    {"title": "Nate Mathews - SVP Operations - Snap-on | LinkedIn",                                "url": "https://www.linkedin.com/in/natemathews-snapon/"},
], min_required=3, max_keep=10))

print("Dover Corporation:", ingest_profiles("Dover Corporation", [
    {"title": "Richard Tobin - President and CEO - Dover Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/richardtobin-dover/"},
    {"title": "Andrey Galiuk - SVP and CFO - Dover Corporation | LinkedIn",                        "url": "https://www.linkedin.com/in/andreygaliuk/"},
    {"title": "William Spurgeon - SVP and General Counsel - Dover Corporation | LinkedIn",          "url": "https://www.linkedin.com/in/williamspurgeon-dover/"},
    {"title": "Soma Somasundaram - President and CEO Dover Engineered Products - Dover | LinkedIn", "url": "https://www.linkedin.com/in/somasomasundaram-dover/"},
    {"title": "Bill Chen - SVP Investor Relations - Dover Corporation | LinkedIn",                  "url": "https://www.linkedin.com/in/billchen-dover/"},
    {"title": "Jay Kunc - SVP HR - Dover Corporation | LinkedIn",                                   "url": "https://www.linkedin.com/in/jaykunc-dover/"},
    {"title": "Ivanka Zaneva - SVP Strategy - Dover Corporation | LinkedIn",                        "url": "https://www.linkedin.com/in/ivankazaneva-dover/"},
    {"title": "Girish Juneja - CTO and VP - Dover Corporation | LinkedIn",                          "url": "https://www.linkedin.com/in/girishjuneja-dover/"},
    {"title": "Gary Lockard - President Fueling Solutions - Dover Corporation | LinkedIn",          "url": "https://www.linkedin.com/in/garylockard-dover/"},
    {"title": "Adrian Saville - President Pumps and Process Solutions - Dover | LinkedIn",          "url": "https://www.linkedin.com/in/adriansaville-dover/"},
], min_required=3, max_keep=10))

print("AGCO Corporation:", ingest_profiles("AGCO Corporation", [
    {"title": "Eric Hansotia - Chairman President and CEO - AGCO Corporation | LinkedIn",           "url": "https://www.linkedin.com/in/erichansotia/"},
    {"title": "Damon Audia - SVP and CFO - AGCO Corporation | LinkedIn",                           "url": "https://www.linkedin.com/in/damonaudia/"},
    {"title": "Rob Smith - SVP Global Operations - AGCO Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/robsmith-agco/"},
    {"title": "Mallory Van Ness - SVP General Counsel - AGCO Corporation | LinkedIn",              "url": "https://www.linkedin.com/in/malloryvanness/"},
    {"title": "Rachel Bach - SVP Chief HR Officer - AGCO Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/rachelbach-agco/"},
    {"title": "Torsten Dehner - SVP Fendt Business Unit - AGCO Corporation | LinkedIn",            "url": "https://www.linkedin.com/in/torstendehner-agco/"},
    {"title": "Coen van Engelen - SVP Massey Ferguson Business Unit - AGCO | LinkedIn",            "url": "https://www.linkedin.com/in/coenvanengelen-agco/"},
    {"title": "Greg Peterson - VP Investor Relations - AGCO Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/gregpeterson-agco/"},
    {"title": "Seth Crawford - President Protein - AGCO Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/sethcrawford-agco/"},
    {"title": "Sven Bake - SVP GSI and Grain Systems - AGCO Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/svenbake-agco/"},
], min_required=3, max_keep=10))

print("VF Corporation:", ingest_profiles("VF Corporation", [
    {"title": "Bracken Darrell - President and CEO - VF Corporation | LinkedIn",                   "url": "https://www.linkedin.com/in/brackenDarrell/"},
    {"title": "Matt Puckett - EVP and CFO - VF Corporation | LinkedIn",                            "url": "https://www.linkedin.com/in/mattpuckett-vfc/"},
    {"title": "Sun Choe - Chief Product and Merchandising Officer - VF Corporation | LinkedIn",    "url": "https://www.linkedin.com/in/sunchoe-vfc/"},
    {"title": "Craig Zanon - Group President Americas - VF Corporation | LinkedIn",                "url": "https://www.linkedin.com/in/craigzanon-vfc/"},
    {"title": "Martino Scabbia Guerrini - Group President EMEA - VF Corporation | LinkedIn",       "url": "https://www.linkedin.com/in/martinoscabbiaGuerrini/"},
    {"title": "Caroline Brown - Chief Transformation Officer - VF Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/carolinebrown-vfc/"},
    {"title": "Bryan McDowell - General Counsel - VF Corporation | LinkedIn",                      "url": "https://www.linkedin.com/in/bryanmcdowell-vfc/"},
    {"title": "Laura Meagher - Chief HR Officer - VF Corporation | LinkedIn",                      "url": "https://www.linkedin.com/in/laurameagher-vfc/"},
    {"title": "Evan Gold - VP Investor Relations - VF Corporation | LinkedIn",                     "url": "https://www.linkedin.com/in/evangold-vfc/"},
    {"title": "Steve Rendle - Former Chairman and CEO - VF Corporation | LinkedIn",                "url": "https://www.linkedin.com/in/steverendle-vfc/"},
], min_required=3, max_keep=10))

print("PVH Corp:", ingest_profiles("PVH Corp", [
    {"title": "Stefan Larsson - President and CEO - PVH Corp | LinkedIn",                          "url": "https://www.linkedin.com/in/stefanlarsson-pvh/"},
    {"title": "Zac Coughlin - EVP and CFO - PVH Corp | LinkedIn",                                  "url": "https://www.linkedin.com/in/zaccoughlin-pvh/"},
    {"title": "Trish Donnelly - CEO Tommy Hilfiger Global - PVH Corp | LinkedIn",                  "url": "https://www.linkedin.com/in/trishdonnelly-pvh/"},
    {"title": "Eva Serrano - CEO Calvin Klein Global - PVH Corp | LinkedIn",                       "url": "https://www.linkedin.com/in/evaserrano-pvh/"},
    {"title": "David Savman - EVP Chief Supply Chain Officer - PVH Corp | LinkedIn",               "url": "https://www.linkedin.com/in/davidsavman-pvh/"},
    {"title": "Mark Fischer - EVP Chief People Officer - PVH Corp | LinkedIn",                     "url": "https://www.linkedin.com/in/markfischer-pvh/"},
    {"title": "Michael Shaffer - EVP Chief Operating and Financial Officer - PVH | LinkedIn",      "url": "https://www.linkedin.com/in/michaelshaffer-pvh/"},
    {"title": "Dana Perlman - SVP Investor Relations - PVH Corp | LinkedIn",                       "url": "https://www.linkedin.com/in/danaperlman-pvh/"},
    {"title": "Melissa Goldie - Chief Marketing Officer - PVH Corp | LinkedIn",                    "url": "https://www.linkedin.com/in/melissagoldie-pvh/"},
    {"title": "Mark Brashear - President Tommy Hilfiger Americas - PVH Corp | LinkedIn",           "url": "https://www.linkedin.com/in/markbrashear-pvh/"},
], min_required=3, max_keep=10))

print("Tapestry:", ingest_profiles("Tapestry", [
    {"title": "Joanne Crevoiserat - CEO - Tapestry | LinkedIn",                                    "url": "https://www.linkedin.com/in/joannecrevoiserat/"},
    {"title": "Scott Roe - EVP and CFO - Tapestry | LinkedIn",                                     "url": "https://www.linkedin.com/in/scottroe-tapestry/"},
    {"title": "Todd Kahn - CEO Coach Brand - Tapestry | LinkedIn",                                 "url": "https://www.linkedin.com/in/toddkahn-tapestry/"},
    {"title": "Liz Fraser - CEO Kate Spade Brand - Tapestry | LinkedIn",                           "url": "https://www.linkedin.com/in/lizfraser-tapestry/"},
    {"title": "Jennifer Bewley - EVP and Chief Communication Officer - Tapestry | LinkedIn",       "url": "https://www.linkedin.com/in/jenniferbewley-tapestry/"},
    {"title": "Noelle Mykolenko - EVP Chief HR Officer - Tapestry | LinkedIn",                     "url": "https://www.linkedin.com/in/noellemykolenko-tapestry/"},
    {"title": "Brian Hawkins - EVP General Counsel - Tapestry | LinkedIn",                         "url": "https://www.linkedin.com/in/brianhawkins-tapestry/"},
    {"title": "Ike Boruchow - VP Investor Relations - Tapestry | LinkedIn",                        "url": "https://www.linkedin.com/in/ikeboruchow-tapestry/"},
    {"title": "Greg Pol - EVP Chief Digital Officer - Tapestry | LinkedIn",                        "url": "https://www.linkedin.com/in/gregpol-tapestry/"},
    {"title": "Carlos Netto - EVP Chief Supply Chain Officer - Tapestry | LinkedIn",               "url": "https://www.linkedin.com/in/carlosnetto-tapestry/"},
], min_required=3, max_keep=10))

print("Bath and Body Works:", ingest_profiles("Bath and Body Works", [
    {"title": "Gina Boswell - CEO - Bath and Body Works | LinkedIn",                               "url": "https://www.linkedin.com/in/ginaboswell/"},
    {"title": "Eva Boratto - EVP and CFO - Bath and Body Works | LinkedIn",                        "url": "https://www.linkedin.com/in/evaboratto/"},
    {"title": "Maurice Cooper - EVP Chief Customer Officer - Bath and Body Works | LinkedIn",      "url": "https://www.linkedin.com/in/mauricecooper-bbw/"},
    {"title": "Deon Riley - EVP Chief HR Officer - Bath and Body Works | LinkedIn",                "url": "https://www.linkedin.com/in/deonriley-bbw/"},
    {"title": "James Chambers - EVP General Counsel - Bath and Body Works | LinkedIn",             "url": "https://www.linkedin.com/in/jameschambers-bbw/"},
    {"title": "Belinda Doke - EVP Chief Supply Chain Officer - Bath and Body Works | LinkedIn",    "url": "https://www.linkedin.com/in/belindadoke-bbw/"},
    {"title": "Chris Cramer - EVP Chief Merchandising Officer - Bath and Body Works | LinkedIn",   "url": "https://www.linkedin.com/in/chriscramer-bbw/"},
    {"title": "Mike Ardrey - SVP Investor Relations - Bath and Body Works | LinkedIn",             "url": "https://www.linkedin.com/in/mikeardrey-bbw/"},
    {"title": "Frank Basha - SVP Store Operations - Bath and Body Works | LinkedIn",               "url": "https://www.linkedin.com/in/frankbasha-bbw/"},
    {"title": "Julia Dagnon - SVP Digital - Bath and Body Works | LinkedIn",                       "url": "https://www.linkedin.com/in/juliadagnon-bbw/"},
], min_required=3, max_keep=10))

print("Dick's Sporting Goods:", ingest_profiles("Dick's Sporting Goods", [
    {"title": "Lauren Hobart - President and CEO - Dick's Sporting Goods | LinkedIn",              "url": "https://www.linkedin.com/in/laurenhobart/"},
    {"title": "Navdeep Gupta - EVP and CFO - Dick's Sporting Goods | LinkedIn",                    "url": "https://www.linkedin.com/in/navdeepgupta-dicks/"},
    {"title": "Ed Stack - Executive Chairman - Dick's Sporting Goods | LinkedIn",                  "url": "https://www.linkedin.com/in/edstack-dicks/"},
    {"title": "Lee Belitsky - EVP and Chief Administrative Officer - Dick's | LinkedIn",           "url": "https://www.linkedin.com/in/leebelitsky-dicks/"},
    {"title": "Brian Unmacht - EVP Store Operations - Dick's Sporting Goods | LinkedIn",           "url": "https://www.linkedin.com/in/brianunmacht-dicks/"},
    {"title": "Mel Tucker - EVP and Chief Merchandising Officer - Dick's | LinkedIn",              "url": "https://www.linkedin.com/in/meltucker-dicks/"},
    {"title": "Carrie Ask - EVP Chief HR Officer - Dick's Sporting Goods | LinkedIn",              "url": "https://www.linkedin.com/in/carrieask-dicks/"},
    {"title": "Justin Schafer - EVP General Counsel - Dick's Sporting Goods | LinkedIn",           "url": "https://www.linkedin.com/in/justinschafer-dicks/"},
    {"title": "Nate Gilch - SVP Digital Commerce - Dick's Sporting Goods | LinkedIn",              "url": "https://www.linkedin.com/in/nategilch-dicks/"},
    {"title": "Thomas Gentes - VP Investor Relations - Dick's Sporting Goods | LinkedIn",          "url": "https://www.linkedin.com/in/thomasgentes-dicks/"},
], min_required=3, max_keep=10))

print("Foot Locker:", ingest_profiles("Foot Locker", [
    {"title": "Mary Dillon - President and CEO - Foot Locker | LinkedIn",                          "url": "https://www.linkedin.com/in/marydillon/"},
    {"title": "Mike Baughn - EVP and CFO - Foot Locker | LinkedIn",                               "url": "https://www.linkedin.com/in/mikebaughn-footlocker/"},
    {"title": "Mel Tucker - EVP Chief Merchandising Officer - Foot Locker | LinkedIn",             "url": "https://www.linkedin.com/in/meltucker-footlocker/"},
    {"title": "Andrew Page - EVP Chief Digital Officer - Foot Locker | LinkedIn",                  "url": "https://www.linkedin.com/in/andrewpage-footlocker/"},
    {"title": "Sheilagh Mahon - EVP Chief HR Officer - Foot Locker | LinkedIn",                    "url": "https://www.linkedin.com/in/sheilaghMahon-footlocker/"},
    {"title": "Giovanna Cipriano - EVP General Counsel - Foot Locker | LinkedIn",                  "url": "https://www.linkedin.com/in/giovannacIPriano-footlocker/"},
    {"title": "Frank Bracken - EVP President North America - Foot Locker | LinkedIn",              "url": "https://www.linkedin.com/in/frankbracken-footlocker/"},
    {"title": "Alison Rosenthal - SVP Investor Relations - Foot Locker | LinkedIn",                "url": "https://www.linkedin.com/in/alisonrosenthal-footlocker/"},
    {"title": "Emanuel Chirico - Board Chair - Foot Locker | LinkedIn",                            "url": "https://www.linkedin.com/in/emanuelchirico-footlocker/"},
    {"title": "John Maurer - SVP Strategy - Foot Locker | LinkedIn",                               "url": "https://www.linkedin.com/in/johnmaurer-footlocker/"},
], min_required=3, max_keep=10))

print("Tractor Supply:", ingest_profiles("Tractor Supply", [
    {"title": "Hal Lawton - President and CEO - Tractor Supply Company | LinkedIn",                "url": "https://www.linkedin.com/in/hallawton/"},
    {"title": "Kurt Barton - EVP and CFO - Tractor Supply Company | LinkedIn",                     "url": "https://www.linkedin.com/in/kurtbarton-tsc/"},
    {"title": "Kimberley Gardiner - EVP Chief Marketing Officer - Tractor Supply | LinkedIn",      "url": "https://www.linkedin.com/in/kimberleygardiner-tsc/"},
    {"title": "Christie Sherrill - EVP Chief People Officer - Tractor Supply | LinkedIn",          "url": "https://www.linkedin.com/in/christiesherrill-tsc/"},
    {"title": "Seth Estep - EVP Chief Merchandising Officer - Tractor Supply | LinkedIn",          "url": "https://www.linkedin.com/in/sethestep-tsc/"},
    {"title": "Colin Yankee - EVP Chief Supply Chain Officer - Tractor Supply | LinkedIn",         "url": "https://www.linkedin.com/in/colinyankee-tsc/"},
    {"title": "Mary Winn Pilkington - VP Investor Relations - Tractor Supply | LinkedIn",          "url": "https://www.linkedin.com/in/maryWinnpilkington/"},
    {"title": "Roberto Vazquez - SVP General Counsel - Tractor Supply | LinkedIn",                 "url": "https://www.linkedin.com/in/robertovazquez-tsc/"},
    {"title": "Jason Foisie - EVP Store Operations - Tractor Supply | LinkedIn",                   "url": "https://www.linkedin.com/in/jasonfoisie-tsc/"},
    {"title": "Rob Mills - EVP Chief Digital and Technology Officer - Tractor Supply | LinkedIn",  "url": "https://www.linkedin.com/in/robmills-tsc/"},
], min_required=3, max_keep=10))

print("Campbell Soup Company:", ingest_profiles("Campbell Soup Company", [
    {"title": "Mark Clouse - President and CEO - Campbell Soup Company | LinkedIn",                "url": "https://www.linkedin.com/in/markclouse-campbell/"},
    {"title": "Carrie Anderson - EVP and CFO - Campbell Soup Company | LinkedIn",                  "url": "https://www.linkedin.com/in/carrieanderson-campbell/"},
    {"title": "Carlos Abrams-Rivera - EVP President Snacks - Campbell Soup Company | LinkedIn",   "url": "https://www.linkedin.com/in/carlosabrams-rivera/"},
    {"title": "Valerie Oswalt - EVP President Meals and Beverages - Campbell | LinkedIn",          "url": "https://www.linkedin.com/in/valerieoswalt-campbell/"},
    {"title": "Mick Beekhuizen - SVP Chief Strategy Officer - Campbell Soup Company | LinkedIn",   "url": "https://www.linkedin.com/in/mickbeekhuizen/"},
    {"title": "Linda Deluca - SVP Chief HR Officer - Campbell Soup Company | LinkedIn",            "url": "https://www.linkedin.com/in/lindadeluca-campbell/"},
    {"title": "Adam Cirone - SVP General Counsel - Campbell Soup Company | LinkedIn",              "url": "https://www.linkedin.com/in/adamcirone-campbell/"},
    {"title": "Rebecca Gardy - SVP Investor Relations - Campbell Soup Company | LinkedIn",         "url": "https://www.linkedin.com/in/rebeccagardy-campbell/"},
    {"title": "Daniel Kubiak - SVP Chief Supply Chain Officer - Campbell Soup | LinkedIn",         "url": "https://www.linkedin.com/in/danielkubiak-campbell/"},
    {"title": "Marybeth Thorsgaard - SVP Chief Growth and Digital Officer - Campbell | LinkedIn",  "url": "https://www.linkedin.com/in/marybeththorsgaard-campbell/"},
], min_required=3, max_keep=10))

print("McCormick:", ingest_profiles("McCormick", [
    {"title": "Brendan Foley - President and CEO - McCormick and Company | LinkedIn",              "url": "https://www.linkedin.com/in/brendanfoley-mccormick/"},
    {"title": "Mike Smith - EVP and CFO - McCormick and Company | LinkedIn",                       "url": "https://www.linkedin.com/in/mikesmith-mccormick/"},
    {"title": "Nneka Rimmer - EVP Strategy and Global Enablement - McCormick | LinkedIn",          "url": "https://www.linkedin.com/in/nnekarimmer/"},
    {"title": "Lawrence Kurzius - Executive Chairman - McCormick and Company | LinkedIn",          "url": "https://www.linkedin.com/in/lawrencekurzius/"},
    {"title": "Avery Haines - EVP Chief HR Officer - McCormick and Company | LinkedIn",            "url": "https://www.linkedin.com/in/averyhaines-mccormick/"},
    {"title": "Kasey Jenkins - EVP and Chief Marketing Officer - McCormick | LinkedIn",            "url": "https://www.linkedin.com/in/kaseyjenkins-mccormick/"},
    {"title": "Lisa Macpherson - VP and General Counsel - McCormick | LinkedIn",                   "url": "https://www.linkedin.com/in/lisamacpherson-mccormick/"},
    {"title": "Marcos Carril - President EMEA - McCormick and Company | LinkedIn",                 "url": "https://www.linkedin.com/in/marcoscarril-mccormick/"},
    {"title": "Fisk Johnson - VP Investor Relations - McCormick and Company | LinkedIn",           "url": "https://www.linkedin.com/in/fiskjohnson-mccormick/"},
    {"title": "Ericka Anderson - SVP Consumer Business Americas - McCormick | LinkedIn",           "url": "https://www.linkedin.com/in/erickaanderson-mccormick/"},
], min_required=3, max_keep=10))

print("Hormel Foods:", ingest_profiles("Hormel Foods", [
    {"title": "Jim Snee - Chairman President and CEO - Hormel Foods | LinkedIn",                   "url": "https://www.linkedin.com/in/jimsnee/"},
    {"title": "Jacinth Smiley - Group VP and CFO - Hormel Foods | LinkedIn",                       "url": "https://www.linkedin.com/in/jacinthsmiley-hormel/"},
    {"title": "Mark Coffey - Group VP Supply Chain - Hormel Foods | LinkedIn",                     "url": "https://www.linkedin.com/in/markcoffey-hormel/"},
    {"title": "Glenn Leitch - Group VP Refrigerated Foods - Hormel Foods | LinkedIn",              "url": "https://www.linkedin.com/in/glennleitch-hormel/"},
    {"title": "Wendy Barcus - VP Chief HR Officer - Hormel Foods | LinkedIn",                      "url": "https://www.linkedin.com/in/wendybarcus-hormel/"},
    {"title": "Larry Vorpahl - Group VP International - Hormel Foods | LinkedIn",                  "url": "https://www.linkedin.com/in/larryvorpahl-hormel/"},
    {"title": "Tom Day - Group VP Foodservice - Hormel Foods | LinkedIn",                          "url": "https://www.linkedin.com/in/tomday-hormel/"},
    {"title": "David Dahlstrom - Group VP Grocery Products - Hormel Foods | LinkedIn",             "url": "https://www.linkedin.com/in/daviddahlstrom-hormel/"},
    {"title": "Nathan Annis - VP Chief Marketing Officer - Hormel Foods | LinkedIn",               "url": "https://www.linkedin.com/in/nathanannis-hormel/"},
    {"title": "David Biegger - Senior VP Chief Supply Chain Officer - Hormel | LinkedIn",          "url": "https://www.linkedin.com/in/davidbiegger-hormel/"},
], min_required=3, max_keep=10))

print("CBRE Group:", ingest_profiles("CBRE Group", [
    {"title": "Bob Sulentic - President and CEO - CBRE Group | LinkedIn",                          "url": "https://www.linkedin.com/in/bobsulentic/"},
    {"title": "Emma Giamartino - EVP and CFO - CBRE Group | LinkedIn",                             "url": "https://www.linkedin.com/in/emmagiamartino/"},
    {"title": "Leah Stearns - EVP and Chief Accounting Officer - CBRE Group | LinkedIn",           "url": "https://www.linkedin.com/in/leahstearns-cbre/"},
    {"title": "Vikram Kohli - EVP Chief Operating Officer - CBRE Group | LinkedIn",                "url": "https://www.linkedin.com/in/vikramkohli-cbre/"},
    {"title": "John Campbell - EVP Chief HR Officer - CBRE Group | LinkedIn",                      "url": "https://www.linkedin.com/in/johncampbell-cbre/"},
    {"title": "Bill Concannon - EVP Global Workplace Solutions - CBRE Group | LinkedIn",           "url": "https://www.linkedin.com/in/billconcannon-cbre/"},
    {"title": "Danny Queenan - EVP Real Estate Investments - CBRE Group | LinkedIn",               "url": "https://www.linkedin.com/in/dannyqueenan-cbre/"},
    {"title": "Tim Dismond - EVP and CLO - CBRE Group | LinkedIn",                                 "url": "https://www.linkedin.com/in/timdismond-cbre/"},
    {"title": "Bill Foley - VP Investor Relations - CBRE Group | LinkedIn",                        "url": "https://www.linkedin.com/in/billfoley-cbre/"},
    {"title": "Kimberly Sheehy - SVP Data and Intelligence - CBRE Group | LinkedIn",               "url": "https://www.linkedin.com/in/kimberlysheehy-cbre/"},
], min_required=3, max_keep=10))

print("Jones Lang LaSalle:", ingest_profiles("Jones Lang LaSalle", [
    {"title": "Christian Ulbrich - President and CEO - JLL | LinkedIn",                            "url": "https://www.linkedin.com/in/christianulbrich/"},
    {"title": "Karen Brennan - CFO - JLL | LinkedIn",                                              "url": "https://www.linkedin.com/in/karenbrennan-jll/"},
    {"title": "Siddharth Taparia - EVP Chief Marketing Officer - JLL | LinkedIn",                  "url": "https://www.linkedin.com/in/siddharth-taparia/"},
    {"title": "Richard Bloxam - CEO Capital Markets - JLL | LinkedIn",                             "url": "https://www.linkedin.com/in/richardbloxam-jll/"},
    {"title": "Mihail Popescu - CEO Work Dynamics - JLL | LinkedIn",                               "url": "https://www.linkedin.com/in/mihailpopescu-jll/"},
    {"title": "Amber Schiada - Head of Work Dynamics Research - JLL | LinkedIn",                   "url": "https://www.linkedin.com/in/amberschiada-jll/"},
    {"title": "Stephanie Plaines - EVP Chief HR Officer - JLL | LinkedIn",                         "url": "https://www.linkedin.com/in/stephanieplaines-jll/"},
    {"title": "Scott Parsons - EVP Chief Legal Officer - JLL | LinkedIn",                          "url": "https://www.linkedin.com/in/scottparsons-jll/"},
    {"title": "Felecia Peyser - VP Investor Relations - JLL | LinkedIn",                           "url": "https://www.linkedin.com/in/felecIApeyser-jll/"},
    {"title": "Tsuyoshi Okamoto - CEO Asia Pacific - JLL | LinkedIn",                              "url": "https://www.linkedin.com/in/tsuyoshiokamoto-jll/"},
], min_required=3, max_keep=10))

print("Iron Mountain:", ingest_profiles("Iron Mountain", [
    {"title": "William Meaney - President and CEO - Iron Mountain | LinkedIn",                     "url": "https://www.linkedin.com/in/williammeaney/"},
    {"title": "Barry Hytinen - EVP and CFO - Iron Mountain | LinkedIn",                            "url": "https://www.linkedin.com/in/barryhytinen/"},
    {"title": "Patrick Keddy - EVP Chief Commercial Officer - Iron Mountain | LinkedIn",            "url": "https://www.linkedin.com/in/patrickkeddy-ironmountain/"},
    {"title": "Mark Kidd - EVP Global Data Center Solutions - Iron Mountain | LinkedIn",           "url": "https://www.linkedin.com/in/markkidd-ironmountain/"},
    {"title": "Deirdre Evens - EVP Chief HR Officer - Iron Mountain | LinkedIn",                   "url": "https://www.linkedin.com/in/deirdreevens-ironmountain/"},
    {"title": "Ernest Cloutier - EVP General Counsel - Iron Mountain | LinkedIn",                  "url": "https://www.linkedin.com/in/ernestcloutier-ironmountain/"},
    {"title": "Stewart Coss - EVP Technology - Iron Mountain | LinkedIn",                          "url": "https://www.linkedin.com/in/stewartcoss-ironmountain/"},
    {"title": "Deborah Bhatt - EVP Chief Customer Officer - Iron Mountain | LinkedIn",             "url": "https://www.linkedin.com/in/deborahbhatt-ironmountain/"},
    {"title": "Gillian Tans - Board Member - Iron Mountain | LinkedIn",                            "url": "https://www.linkedin.com/in/gilliantans/"},
    {"title": "Heather Furnas - VP Investor Relations - Iron Mountain | LinkedIn",                 "url": "https://www.linkedin.com/in/heatherfurnas-ironmountain/"},
], min_required=3, max_keep=10))

print("DXC Technology:", ingest_profiles("DXC Technology", [
    {"title": "Raul Fernandez - President and CEO - DXC Technology | LinkedIn",                    "url": "https://www.linkedin.com/in/raulfernandez-dxc/"},
    {"title": "Rob Del Bene - EVP and CFO - DXC Technology | LinkedIn",                           "url": "https://www.linkedin.com/in/robdelbene-dxc/"},
    {"title": "Mary Finch - EVP Chief HR Officer - DXC Technology | LinkedIn",                     "url": "https://www.linkedin.com/in/maryfinch-dxc/"},
    {"title": "Leonard Livschitz - EVP and CTO - DXC Technology | LinkedIn",                       "url": "https://www.linkedin.com/in/leonardlivschitz-dxc/"},
    {"title": "Bill Deckelman - EVP General Counsel - DXC Technology | LinkedIn",                  "url": "https://www.linkedin.com/in/billdeckelman-dxc/"},
    {"title": "Chris Drumgoole - EVP and COO - DXC Technology | LinkedIn",                         "url": "https://www.linkedin.com/in/chrisdrumgoole-dxc/"},
    {"title": "Vinod Bagal - EVP Transformation - DXC Technology | LinkedIn",                     "url": "https://www.linkedin.com/in/vinodbagal-dxc/"},
    {"title": "Justin Murfin - EVP Global Sales - DXC Technology | LinkedIn",                      "url": "https://www.linkedin.com/in/justinmurfin-dxc/"},
    {"title": "Ken Haller - SVP Investor Relations - DXC Technology | LinkedIn",                   "url": "https://www.linkedin.com/in/kenhaller-dxc/"},
    {"title": "Thomas Van Itallie - EVP Global Delivery - DXC Technology | LinkedIn",              "url": "https://www.linkedin.com/in/thomasvanitallie-dxc/"},
], min_required=3, max_keep=10))

print("Concentrix:", ingest_profiles("Concentrix", [
    {"title": "Chris Caldwell - President and CEO - Concentrix | LinkedIn",                        "url": "https://www.linkedin.com/in/chriscaldwell-concentrix/"},
    {"title": "Andre Valentine - EVP and CFO - Concentrix | LinkedIn",                             "url": "https://www.linkedin.com/in/andrevalentine-concentrix/"},
    {"title": "Tony Speelman - EVP Chief Operating Officer - Concentrix | LinkedIn",               "url": "https://www.linkedin.com/in/tonyspeelman-concentrix/"},
    {"title": "Carey Andrews - EVP Chief HR Officer - Concentrix | LinkedIn",                      "url": "https://www.linkedin.com/in/careyandrews-concentrix/"},
    {"title": "Richard Bram - EVP and General Counsel - Concentrix | LinkedIn",                    "url": "https://www.linkedin.com/in/richardbram-concentrix/"},
    {"title": "Vikas Bhatt - EVP Strategy - Concentrix | LinkedIn",                                "url": "https://www.linkedin.com/in/vikasbhatt-concentrix/"},
    {"title": "Patrick Tyrrell - EVP Sales - Concentrix | LinkedIn",                               "url": "https://www.linkedin.com/in/patricktyrrell-concentrix/"},
    {"title": "David Buell - EVP Chief Marketing Officer - Concentrix | LinkedIn",                 "url": "https://www.linkedin.com/in/davidbuell-concentrix/"},
    {"title": "Jarrod Morris - SVP Investor Relations - Concentrix | LinkedIn",                    "url": "https://www.linkedin.com/in/jarrodmorris-concentrix/"},
    {"title": "Amy Messano - EVP Global Business Services - Concentrix | LinkedIn",                "url": "https://www.linkedin.com/in/amymessano-concentrix/"},
], min_required=3, max_keep=10))

print("Zimmer Biomet:", ingest_profiles("Zimmer Biomet", [
    {"title": "Ivan Tornos - President and CEO - Zimmer Biomet | LinkedIn",                        "url": "https://www.linkedin.com/in/ivantornos/"},
    {"title": "Suky Upadhyay - EVP and CFO - Zimmer Biomet | LinkedIn",                            "url": "https://www.linkedin.com/in/sukyupadhyay/"},
    {"title": "Lior Zeitoun - EVP and President Americas - Zimmer Biomet | LinkedIn",              "url": "https://www.linkedin.com/in/liorzeitoun-zimmerbiomet/"},
    {"title": "Sang Yi - EVP and President APAC - Zimmer Biomet | LinkedIn",                       "url": "https://www.linkedin.com/in/sangyi-zimmerbiomet/"},
    {"title": "Didier Deltort - EVP and President EMEA - Zimmer Biomet | LinkedIn",                "url": "https://www.linkedin.com/in/didierdeltort-zimmerbiomet/"},
    {"title": "Chris Barry - EVP Chief Operating Officer - Zimmer Biomet | LinkedIn",              "url": "https://www.linkedin.com/in/chrisbarry-zimmerbiomet/"},
    {"title": "Heather Kidwell - SVP and General Counsel - Zimmer Biomet | LinkedIn",              "url": "https://www.linkedin.com/in/heatherkidwell-zimmerbiomet/"},
    {"title": "Sheri Dodd - SVP Chief Marketing Officer - Zimmer Biomet | LinkedIn",               "url": "https://www.linkedin.com/in/sheridodd-zimmerbiomet/"},
    {"title": "Keri Mattox - SVP Chief People Officer - Zimmer Biomet | LinkedIn",                 "url": "https://www.linkedin.com/in/kerimattox-zimmerbiomet/"},
    {"title": "Kevin Beaty - VP Investor Relations - Zimmer Biomet | LinkedIn",                    "url": "https://www.linkedin.com/in/kevinbeaty-zimmerbiomet/"},
], min_required=3, max_keep=10))

print("Hologic:", ingest_profiles("Hologic", [
    {"title": "Steve MacMillan - Chairman President and CEO - Hologic | LinkedIn",                 "url": "https://www.linkedin.com/in/stevemacmillan-hologic/"},
    {"title": "Karleen Oberton - EVP and CFO - Hologic | LinkedIn",                                "url": "https://www.linkedin.com/in/karleenoberton-hologic/"},
    {"title": "Jan Verstreken - EVP President International - Hologic | LinkedIn",                 "url": "https://www.linkedin.com/in/janverstreken-hologic/"},
    {"title": "Eric Compton - EVP President Breast and Skeletal Health - Hologic | LinkedIn",     "url": "https://www.linkedin.com/in/ericcompton-hologic/"},
    {"title": "John Pekarsky - EVP and Chief Revenue Officer - Hologic | LinkedIn",               "url": "https://www.linkedin.com/in/johnpekarsky-hologic/"},
    {"title": "Suzanne Zaccour - EVP and General Counsel - Hologic | LinkedIn",                   "url": "https://www.linkedin.com/in/suzannezaccour-hologic/"},
    {"title": "Renae Busch - EVP and Chief HR Officer - Hologic | LinkedIn",                       "url": "https://www.linkedin.com/in/renaebusch-hologic/"},
    {"title": "Mike Watts - SVP and Chief Marketing Officer - Hologic | LinkedIn",                 "url": "https://www.linkedin.com/in/mikewatts-hologic/"},
    {"title": "Ryan Simon - VP Investor Relations - Hologic | LinkedIn",                           "url": "https://www.linkedin.com/in/ryansimon-hologic/"},
    {"title": "Tom West - EVP President Diagnostics - Hologic | LinkedIn",                         "url": "https://www.linkedin.com/in/tomwest-hologic/"},
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
