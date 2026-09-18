"""FV Gmail Batch 2 — 30 new companies not previously in any FV campaign, eleynxiong@gmail.com."""
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
    {"name": "Mercedes-Benz",          "domain": "mercedes-benz.com",    "industry": "Automotive / Luxury",                  "email_pattern": "first.last"},
    {"name": "PlayStation",            "domain": "playstation.com",       "industry": "Gaming / Consumer Electronics",        "email_pattern": "first.last"},
    {"name": "Vercel",                 "domain": "vercel.com",            "industry": "Cloud / Developer Platform / AI",      "email_pattern": "first.last"},
    {"name": "CVS Health",             "domain": "cvshealth.com",         "industry": "Healthcare / Pharmacy / Insurance",    "email_pattern": "first.last"},
    {"name": "American Express",       "domain": "americanexpress.com",   "industry": "Financial Services / Payments",        "email_pattern": "first.last"},
    {"name": "Atlassian",              "domain": "atlassian.com",         "industry": "Developer Tools / Enterprise SaaS",    "email_pattern": "first.last"},
    {"name": "Brex",                   "domain": "brex.com",              "industry": "Fintech / Corporate Cards / Spend Mgmt","email_pattern": "first.last"},
    {"name": "Shopify",                "domain": "shopify.com",           "industry": "E-Commerce Platform / SaaS",           "email_pattern": "first.last"},
    {"name": "Slack",                  "domain": "slack.com",             "industry": "Enterprise SaaS / Collaboration",      "email_pattern": "first.last"},
    {"name": "L'Oreal",                "domain": "loreal.com",            "industry": "Beauty / Consumer Goods",              "email_pattern": "first.last"},
    {"name": "Lyft",                   "domain": "lyft.com",              "industry": "Rideshare / Mobility Tech",            "email_pattern": "first.last"},
    {"name": "Pinterest",              "domain": "pinterest.com",         "industry": "Social Media / Visual Discovery",      "email_pattern": "first.last"},
    {"name": "HubSpot",                "domain": "hubspot.com",           "industry": "CRM / Marketing SaaS",                 "email_pattern": "first.last"},
    {"name": "Cloudflare",             "domain": "cloudflare.com",        "industry": "Network Security / CDN",               "email_pattern": "first.last"},
    {"name": "Palo Alto Networks",     "domain": "paloaltonetworks.com",  "industry": "Cybersecurity / Enterprise Security",  "email_pattern": "first.last"},
    {"name": "Replit",                 "domain": "replit.com",            "industry": "AI Dev Tools / Cloud IDE",             "email_pattern": "first.last"},
    {"name": "eBay",                   "domain": "ebay.com",              "industry": "E-Commerce / Marketplace",             "email_pattern": "first.last"},
    {"name": "Duolingo",               "domain": "duolingo.com",          "industry": "EdTech / Consumer App",                "email_pattern": "first.last"},
    {"name": "NBA",                    "domain": "nba.com",               "industry": "Sports / Media / Entertainment",       "email_pattern": "first.last"},
    {"name": "Thermo Fisher Scientific","domain": "thermofisher.com",     "industry": "Life Sciences / Lab Equipment",        "email_pattern": "first.last"},
    {"name": "Tesla",                  "domain": "tesla.com",             "industry": "Electric Vehicles / Energy / AI",      "email_pattern": "first.last"},
    {"name": "SAP",                    "domain": "sap.com",               "industry": "Enterprise Software / ERP / Cloud",    "email_pattern": "first.last"},
    {"name": "Marriott",               "domain": "marriott.com",          "industry": "Hospitality / Hotels / Travel",        "email_pattern": "first.last"},
    {"name": "Coinbase",               "domain": "coinbase.com",          "industry": "Crypto / Fintech / Web3",              "email_pattern": "first.last"},
    {"name": "Qualcomm",               "domain": "qualcomm.com",          "industry": "Semiconductors / Wireless / Mobile",   "email_pattern": "first.last"},
    {"name": "Reddit",                 "domain": "reddit.com",            "industry": "Social Media / Community Platform",    "email_pattern": "first.last"},
    {"name": "Samsung",                "domain": "samsung.com",           "industry": "Consumer Electronics / Semiconductors","email_pattern": "first.last"},
    {"name": "CrowdStrike",            "domain": "crowdstrike.com",       "industry": "Cybersecurity / Endpoint Protection",  "email_pattern": "first.last"},
    {"name": "Datadog",                "domain": "datadoghq.com",         "industry": "Observability / Cloud Monitoring",     "email_pattern": "first.last"},
    {"name": "Confluent",              "domain": "confluent.io",          "industry": "Data Streaming / Kafka / Cloud",       "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Gmail Batch 2 - June 2026"
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

print("\n" + "="*60); print("STEP 2: Ingesting fresh profiles"); print("="*60)

print("Mercedes-Benz:", ingest_profiles("Mercedes-Benz", [
    {"title": "Ola Kallenius - CEO - Mercedes-Benz | LinkedIn",                          "url": "https://www.linkedin.com/in/olakallaenius/"},
    {"title": "Harald Wilhelm - CFO - Mercedes-Benz | LinkedIn",                         "url": "https://www.linkedin.com/in/haraldwilhelm/"},
    {"title": "Markus Schaefer - CTO - Mercedes-Benz | LinkedIn",                        "url": "https://www.linkedin.com/in/markusschaefer-mb/"},
    {"title": "Sabine Kohleisen - Chief HR Officer - Mercedes-Benz | LinkedIn",          "url": "https://www.linkedin.com/in/sabinekohleisen/"},
    {"title": "Britta Seeger - Board Member Sales - Mercedes-Benz | LinkedIn",           "url": "https://www.linkedin.com/in/brittaseeger/"},
    {"title": "Renata Jungo Brungger - Board Member Integrity - Mercedes-Benz | LinkedIn","url": "https://www.linkedin.com/in/renatajungobrunger/"},
    {"title": "Magnus Ostberg - Chief Software Officer - Mercedes-Benz | LinkedIn",      "url": "https://www.linkedin.com/in/magnusostberg/"},
    {"title": "Dimitris Psillakis - President Mercedes-Benz USA | LinkedIn",             "url": "https://www.linkedin.com/in/dimitrispsillakis/"},
    {"title": "Aarti Shah - VP Strategy Americas - Mercedes-Benz | LinkedIn",            "url": "https://www.linkedin.com/in/aartishahmbusa/"},
    {"title": "Drew Slaven - VP Marketing - Mercedes-Benz USA | LinkedIn",               "url": "https://www.linkedin.com/in/drewslaven/"},
], min_required=3, max_keep=10))

print("PlayStation:", ingest_profiles("PlayStation", [
    {"title": "Hermen Hulst - Head of PlayStation Studios - PlayStation | LinkedIn",     "url": "https://www.linkedin.com/in/hermenhulst/"},
    {"title": "Jim Ryan - Former President - PlayStation | LinkedIn",                    "url": "https://www.linkedin.com/in/jimryan-playstation/"},
    {"title": "Hideaki Nishino - CEO PlayStation - PlayStation | LinkedIn",              "url": "https://www.linkedin.com/in/hideakinishino/"},
    {"title": "Veronica Rogers - Chief Revenue Officer - PlayStation | LinkedIn",        "url": "https://www.linkedin.com/in/veronicarogers/"},
    {"title": "Alvin Hung - VP Finance - PlayStation | LinkedIn",                        "url": "https://www.linkedin.com/in/alvinhung-playstation/"},
    {"title": "Eric Lempel - VP Marketing - PlayStation | LinkedIn",                     "url": "https://www.linkedin.com/in/ericlempel/"},
    {"title": "Mary Yee - VP Global Marketing - PlayStation | LinkedIn",                 "url": "https://www.linkedin.com/in/maryyee-playstation/"},
    {"title": "Jeff Ross - Head of PlayStation Network - PlayStation | LinkedIn",        "url": "https://www.linkedin.com/in/jeffross-psn/"},
    {"title": "Grace Chen - VP Developer Relations - PlayStation | LinkedIn",            "url": "https://www.linkedin.com/in/gracechen-playstation/"},
    {"title": "Nate Fox - Creative Director - PlayStation | LinkedIn",                   "url": "https://www.linkedin.com/in/natefox/"},
], min_required=3, max_keep=10))

print("Vercel:", ingest_profiles("Vercel", [
    {"title": "Guillermo Rauch - CEO - Vercel | LinkedIn",                               "url": "https://www.linkedin.com/in/guillermo-rauch/"},
    {"title": "Zack Proser - Head of Developer Relations - Vercel | LinkedIn",           "url": "https://www.linkedin.com/in/zackproser/"},
    {"title": "Lee Robinson - VP Developer Experience - Vercel | LinkedIn",              "url": "https://www.linkedin.com/in/leerob/"},
    {"title": "Malte Ubl - CTO - Vercel | LinkedIn",                                     "url": "https://www.linkedin.com/in/malteubl/"},
    {"title": "Liz Heller - VP Marketing - Vercel | LinkedIn",                           "url": "https://www.linkedin.com/in/lizheller-vercel/"},
    {"title": "Lydia Hallie - Developer Advocate - Vercel | LinkedIn",                   "url": "https://www.linkedin.com/in/lydiahallie/"},
    {"title": "Ashley Peacock - Head of People - Vercel | LinkedIn",                     "url": "https://www.linkedin.com/in/ashleypeacock/"},
    {"title": "Tom Occhino - VP Product - Vercel | LinkedIn",                            "url": "https://www.linkedin.com/in/tomocchino/"},
    {"title": "Nick Nisi - Head of Growth - Vercel | LinkedIn",                          "url": "https://www.linkedin.com/in/nicknisi/"},
    {"title": "Isaac Manwaring - VP Sales - Vercel | LinkedIn",                          "url": "https://www.linkedin.com/in/isaacmanwaring/"},
], min_required=3, max_keep=10))

print("CVS Health:", ingest_profiles("CVS Health", [
    {"title": "Karen Lynch - Former CEO - CVS Health | LinkedIn",                        "url": "https://www.linkedin.com/in/karenlynch-cvs/"},
    {"title": "David Joyner - CEO - CVS Health | LinkedIn",                              "url": "https://www.linkedin.com/in/davidjoyner-cvs/"},
    {"title": "Thomas Cowhey - CFO - CVS Health | LinkedIn",                             "url": "https://www.linkedin.com/in/thomascowhey/"},
    {"title": "Prem Shah - President Pharmacy and Consumer Wellness - CVS | LinkedIn",   "url": "https://www.linkedin.com/in/premshah-cvs/"},
    {"title": "Sree Chaguturu - Chief Medical Officer - CVS Health | LinkedIn",          "url": "https://www.linkedin.com/in/sreechaguturu/"},
    {"title": "Dan Finke - President Health Services - CVS Health | LinkedIn",           "url": "https://www.linkedin.com/in/danfinke/"},
    {"title": "Creighton Welch - VP Digital Experience - CVS Health | LinkedIn",         "url": "https://www.linkedin.com/in/creightonwelch/"},
    {"title": "Amy Lanctot - Chief Communications Officer - CVS Health | LinkedIn",      "url": "https://www.linkedin.com/in/amylanctot/"},
    {"title": "Lisa Bisaccia - Chief HR Officer - CVS Health | LinkedIn",                "url": "https://www.linkedin.com/in/lisabisaccia/"},
    {"title": "Neela Montgomery - EVP Retail - CVS Health | LinkedIn",                   "url": "https://www.linkedin.com/in/neelamontgomery/"},
], min_required=3, max_keep=10))

print("American Express:", ingest_profiles("American Express", [
    {"title": "Stephen Squeri - Chairman and CEO - American Express | LinkedIn",         "url": "https://www.linkedin.com/in/stephensqueri/"},
    {"title": "Christophe Le Caillec - CFO - American Express | LinkedIn",               "url": "https://www.linkedin.com/in/christophelecaillec/"},
    {"title": "Monique Herena - Chief Colleague Experience Officer - AmEx | LinkedIn",   "url": "https://www.linkedin.com/in/moniqueherena/"},
    {"title": "Elizabeth Rutledge - Chief Marketing Officer - AmEx | LinkedIn",          "url": "https://www.linkedin.com/in/elizabethrutledge/"},
    {"title": "Howard Grosfield - President US Consumer Services - AmEx | LinkedIn",     "url": "https://www.linkedin.com/in/howardgrosfield/"},
    {"title": "Anre Williams - President Global Merchant Services - AmEx | LinkedIn",    "url": "https://www.linkedin.com/in/anrewilliams/"},
    {"title": "Raymond Joabar - President Global Services - AmEx | LinkedIn",            "url": "https://www.linkedin.com/in/raymondjoabar/"},
    {"title": "Deborah Gillotti - VP Strategy - American Express | LinkedIn",            "url": "https://www.linkedin.com/in/deborahgillotti/"},
    {"title": "Glenda McNeal - Chief Partner Officer - AmEx | LinkedIn",                 "url": "https://www.linkedin.com/in/glendamcneal/"},
    {"title": "Luke Gebb - President Amex Digital Labs - AmEx | LinkedIn",               "url": "https://www.linkedin.com/in/lukegebb/"},
], min_required=3, max_keep=10))

print("Atlassian:", ingest_profiles("Atlassian", [
    {"title": "Mike Cannon-Brookes - CEO - Atlassian | LinkedIn",                        "url": "https://www.linkedin.com/in/mike-cannon-brookes/"},
    {"title": "Cameron Deatsch - Chief Revenue Officer - Atlassian | LinkedIn",          "url": "https://www.linkedin.com/in/camerondeatsch/"},
    {"title": "Anu Bharadwaj - President - Atlassian | LinkedIn",                        "url": "https://www.linkedin.com/in/anubharadwaj/"},
    {"title": "Andrew Donalds - CFO - Atlassian | LinkedIn",                             "url": "https://www.linkedin.com/in/andrewdonalds/"},
    {"title": "Joff Redfern - Chief Product Officer - Atlassian | LinkedIn",             "url": "https://www.linkedin.com/in/joffredfern/"},
    {"title": "Erika Trautman - VP Product - Atlassian | LinkedIn",                      "url": "https://www.linkedin.com/in/erikatrautman/"},
    {"title": "Avani Prabhakar - Chief People Officer - Atlassian | LinkedIn",           "url": "https://www.linkedin.com/in/avaniprabhakar/"},
    {"title": "Tom Kennedy - VP Sales AMER - Atlassian | LinkedIn",                      "url": "https://www.linkedin.com/in/tomkennedy-atlassian/"},
    {"title": "Steve Goldsmith - VP Partner Solutions - Atlassian | LinkedIn",           "url": "https://www.linkedin.com/in/stevegoldsmith-atlassian/"},
    {"title": "Bonnie Dowling - VP Research - Atlassian | LinkedIn",                     "url": "https://www.linkedin.com/in/bonniedownling/"},
], min_required=3, max_keep=10))

print("Brex:", ingest_profiles("Brex", [
    {"title": "Henrique Dubugras - CEO - Brex | LinkedIn",                               "url": "https://www.linkedin.com/in/henriquedubugras/"},
    {"title": "Pedro Franceschi - CTO - Brex | LinkedIn",                                "url": "https://www.linkedin.com/in/pedrofranceschi/"},
    {"title": "Michael Tannenbaum - Former CFO - Brex | LinkedIn",                       "url": "https://www.linkedin.com/in/michaeltannenbaum/"},
    {"title": "Karandeep Anand - President - Brex | LinkedIn",                           "url": "https://www.linkedin.com/in/karandeepanand/"},
    {"title": "Rahul Vohra - Board Member - Brex | LinkedIn",                            "url": "https://www.linkedin.com/in/rahulvohra/"},
    {"title": "Camila Bernal - Chief People Officer - Brex | LinkedIn",                  "url": "https://www.linkedin.com/in/camilabernal/"},
    {"title": "Sam Blond - Chief Sales Officer - Brex | LinkedIn",                       "url": "https://www.linkedin.com/in/samblond/"},
    {"title": "Erin Fuchs - VP Legal - Brex | LinkedIn",                                 "url": "https://www.linkedin.com/in/erinfuchs-brex/"},
    {"title": "Armando Mann - Chief Revenue Officer - Brex | LinkedIn",                  "url": "https://www.linkedin.com/in/armandomann/"},
    {"title": "Layla Shaikley - VP Marketing - Brex | LinkedIn",                         "url": "https://www.linkedin.com/in/laylashaikley/"},
], min_required=3, max_keep=10))

print("Shopify:", ingest_profiles("Shopify", [
    {"title": "Tobi Lutke - CEO - Shopify | LinkedIn",                                   "url": "https://www.linkedin.com/in/tobiaslutke/"},
    {"title": "Harley Finkelstein - President - Shopify | LinkedIn",                     "url": "https://www.linkedin.com/in/harleyf/"},
    {"title": "Jeff Hoffmeister - CFO - Shopify | LinkedIn",                             "url": "https://www.linkedin.com/in/jeffhoffmeister/"},
    {"title": "Kaz Nejatian - VP Product and COO - Shopify | LinkedIn",                  "url": "https://www.linkedin.com/in/kaznejatian/"},
    {"title": "Bobby Morrison - Chief Revenue Officer - Shopify | LinkedIn",             "url": "https://www.linkedin.com/in/bobby-morrison/"},
    {"title": "Glen Coates - VP Product - Shopify | LinkedIn",                           "url": "https://www.linkedin.com/in/glencoates/"},
    {"title": "Loren Padelford - VP Enterprise - Shopify | LinkedIn",                    "url": "https://www.linkedin.com/in/lorenpadelford/"},
    {"title": "Carl Rivera - VP Merchant Experience - Shopify | LinkedIn",               "url": "https://www.linkedin.com/in/carlrivera/"},
    {"title": "Christopher Nolan - Chief Legal Officer - Shopify | LinkedIn",            "url": "https://www.linkedin.com/in/christopher-nolan-shopify/"},
    {"title": "Vanessa Lee - VP Talent - Shopify | LinkedIn",                            "url": "https://www.linkedin.com/in/vanessalee-shopify/"},
], min_required=3, max_keep=10))

print("Slack:", ingest_profiles("Slack", [
    {"title": "Denise Dresser - CEO - Slack | LinkedIn",                                 "url": "https://www.linkedin.com/in/denisedresser/"},
    {"title": "Brian Elliott - SVP and GM - Slack | LinkedIn",                           "url": "https://www.linkedin.com/in/briandelliott/"},
    {"title": "Noah Weiss - Chief Product Officer - Slack | LinkedIn",                   "url": "https://www.linkedin.com/in/noahweiss/"},
    {"title": "Ali Rayl - VP Customer Experience - Slack | LinkedIn",                    "url": "https://www.linkedin.com/in/alirayl/"},
    {"title": "Tamar Yehoshua - Former CPO - Slack | LinkedIn",                          "url": "https://www.linkedin.com/in/tamaryehoshua/"},
    {"title": "April Underwood - Former VP Product - Slack | LinkedIn",                  "url": "https://www.linkedin.com/in/aprilunderwood/"},
    {"title": "Robert Frati - Chief Sales Officer - Slack | LinkedIn",                   "url": "https://www.linkedin.com/in/robert-frati/"},
    {"title": "Jonathan Prince - VP Communications - Slack | LinkedIn",                  "url": "https://www.linkedin.com/in/jonathan-prince/"},
    {"title": "Brad Armstrong - VP Legal - Slack | LinkedIn",                            "url": "https://www.linkedin.com/in/brad-armstrong-slack/"},
    {"title": "Sarah Friar - Former CFO - Slack | LinkedIn",                             "url": "https://www.linkedin.com/in/sarahfriar/"},
], min_required=3, max_keep=10))

print("L'Oreal:", ingest_profiles("L'Oreal", [
    {"title": "Nicolas Hieronimus - CEO - L'Oreal | LinkedIn",                           "url": "https://www.linkedin.com/in/nicolas-hieronimus/"},
    {"title": "Barbara Lavernos - Deputy CEO - L'Oreal | LinkedIn",                      "url": "https://www.linkedin.com/in/barbara-lavernos/"},
    {"title": "Stephane Rinderknech - President L'Oreal USA | LinkedIn",                 "url": "https://www.linkedin.com/in/stephanerinderknech/"},
    {"title": "Asmita Dubey - Chief Digital and Marketing Officer - L'Oreal | LinkedIn", "url": "https://www.linkedin.com/in/asmita-dubey/"},
    {"title": "Nathalie Roos - President Professional Products - L'Oreal | LinkedIn",   "url": "https://www.linkedin.com/in/nathalie-roos/"},
    {"title": "Vianney Derville - President Europe - L'Oreal | LinkedIn",                "url": "https://www.linkedin.com/in/vianneyderville/"},
    {"title": "Alexis Perakis-Valat - President Consumer Products - L'Oreal | LinkedIn","url": "https://www.linkedin.com/in/alexis-perakis-valat/"},
    {"title": "Delphine Viguier-Hovasse - President L'Oreal Paris | LinkedIn",          "url": "https://www.linkedin.com/in/delphineviguierhovasse/"},
    {"title": "Carol Hamilton - Group President L'Oreal USA | LinkedIn",                 "url": "https://www.linkedin.com/in/carol-hamilton-loreal/"},
    {"title": "David Greenberg - President Consumer Products Americas | LinkedIn",       "url": "https://www.linkedin.com/in/david-greenberg-loreal/"},
], min_required=3, max_keep=10))

print("Lyft:", ingest_profiles("Lyft", [
    {"title": "David Risher - CEO - Lyft | LinkedIn",                                    "url": "https://www.linkedin.com/in/davidrisher/"},
    {"title": "Erin Brewer - CFO - Lyft | LinkedIn",                                     "url": "https://www.linkedin.com/in/erin-brewer-lyft/"},
    {"title": "Kristin Sverchek - President - Lyft | LinkedIn",                          "url": "https://www.linkedin.com/in/kristinsverchek/"},
    {"title": "Melissa Waters - CMO - Lyft | LinkedIn",                                  "url": "https://www.linkedin.com/in/melissawaters/"},
    {"title": "Rohan Bhobe - VP Product - Lyft | LinkedIn",                              "url": "https://www.linkedin.com/in/rohanbhobe/"},
    {"title": "Faye Thieman - Chief People Officer - Lyft | LinkedIn",                   "url": "https://www.linkedin.com/in/fayethieman/"},
    {"title": "Ishaan Bhola - VP Strategy - Lyft | LinkedIn",                            "url": "https://www.linkedin.com/in/ishaanbhola/"},
    {"title": "Matt Kallman - VP Communications - Lyft | LinkedIn",                      "url": "https://www.linkedin.com/in/mattkallman/"},
    {"title": "Ashwin Raj - VP Engineering - Lyft | LinkedIn",                           "url": "https://www.linkedin.com/in/ashwin-raj-lyft/"},
    {"title": "Joao Machado - VP Driver Experience - Lyft | LinkedIn",                   "url": "https://www.linkedin.com/in/joao-machado-lyft/"},
], min_required=3, max_keep=10))

print("Pinterest:", ingest_profiles("Pinterest", [
    {"title": "Bill Ready - CEO - Pinterest | LinkedIn",                                  "url": "https://www.linkedin.com/in/billready/"},
    {"title": "Julia Donnelly - CFO - Pinterest | LinkedIn",                              "url": "https://www.linkedin.com/in/juliadonnelly/"},
    {"title": "Sabrina Ellis - Chief Product Officer - Pinterest | LinkedIn",             "url": "https://www.linkedin.com/in/sabrinaellis/"},
    {"title": "Malik Ducard - Chief Content Officer - Pinterest | LinkedIn",              "url": "https://www.linkedin.com/in/malikducard/"},
    {"title": "Naveen Gavini - Chief Revenue Officer - Pinterest | LinkedIn",             "url": "https://www.linkedin.com/in/naveengavini/"},
    {"title": "Katie Clow - VP Marketing - Pinterest | LinkedIn",                         "url": "https://www.linkedin.com/in/katieclow/"},
    {"title": "Pam Kaufman - Chief Marketing Officer - Pinterest | LinkedIn",             "url": "https://www.linkedin.com/in/pamkaufman/"},
    {"title": "Cristina Schreib - VP People - Pinterest | LinkedIn",                     "url": "https://www.linkedin.com/in/cristinaschreib/"},
    {"title": "Andrei Hagiu - Chief Strategy Officer - Pinterest | LinkedIn",             "url": "https://www.linkedin.com/in/andreihagiu/"},
    {"title": "Jon Kaplan - Chief Revenue Officer - Pinterest | LinkedIn",                "url": "https://www.linkedin.com/in/jonkaplan/"},
], min_required=3, max_keep=10))

print("HubSpot:", ingest_profiles("HubSpot", [
    {"title": "Yamini Rangan - CEO - HubSpot | LinkedIn",                                "url": "https://www.linkedin.com/in/yamini-rangan/"},
    {"title": "Dharmesh Shah - Co-Founder and CTO - HubSpot | LinkedIn",                 "url": "https://www.linkedin.com/in/dharmesh/"},
    {"title": "Kate Bueker - CFO - HubSpot | LinkedIn",                                  "url": "https://www.linkedin.com/in/kate-bueker/"},
    {"title": "Andy Pitre - EVP Product - HubSpot | LinkedIn",                           "url": "https://www.linkedin.com/in/andypitre/"},
    {"title": "Kieran Flanagan - SVP Marketing - HubSpot | LinkedIn",                    "url": "https://www.linkedin.com/in/kieranflanagan/"},
    {"title": "Alison Elworthy - EVP Customer Success - HubSpot | LinkedIn",             "url": "https://www.linkedin.com/in/alisonelworthy/"},
    {"title": "Hunter Madeley - Chief Sales Officer - HubSpot | LinkedIn",               "url": "https://www.linkedin.com/in/huntermadeley/"},
    {"title": "Mark Roberge - CRO Emeritus - HubSpot | LinkedIn",                        "url": "https://www.linkedin.com/in/markroberge/"},
    {"title": "Michael Redbord - SVP Customer Platform - HubSpot | LinkedIn",            "url": "https://www.linkedin.com/in/mredbord/"},
    {"title": "Annette Rippert - Chief People Officer - HubSpot | LinkedIn",             "url": "https://www.linkedin.com/in/annetterippert/"},
], min_required=3, max_keep=10))

print("Cloudflare:", ingest_profiles("Cloudflare", [
    {"title": "Matthew Prince - Co-Founder and CEO - Cloudflare | LinkedIn",             "url": "https://www.linkedin.com/in/matthewprince/"},
    {"title": "Michelle Zatlyn - Co-Founder and President - Cloudflare | LinkedIn",      "url": "https://www.linkedin.com/in/michellezatlyn/"},
    {"title": "Thomas Seifert - CFO - Cloudflare | LinkedIn",                            "url": "https://www.linkedin.com/in/thomasseifert/"},
    {"title": "Marc Boroditsky - Chief Revenue Officer - Cloudflare | LinkedIn",         "url": "https://www.linkedin.com/in/marcboroditsky/"},
    {"title": "Jen Taylor - Chief Product Officer - Cloudflare | LinkedIn",              "url": "https://www.linkedin.com/in/jentaylor/"},
    {"title": "Grant Bourzikas - Chief Security Officer - Cloudflare | LinkedIn",        "url": "https://www.linkedin.com/in/grantbourzikas/"},
    {"title": "Dane Knecht - SVP Product - Cloudflare | LinkedIn",                       "url": "https://www.linkedin.com/in/daneknecht/"},
    {"title": "Robert Blumofe - EVP Technology and CTO - Cloudflare | LinkedIn",         "url": "https://www.linkedin.com/in/rblumofe/"},
    {"title": "Vanessa Larco - Board Director - Cloudflare | LinkedIn",                  "url": "https://www.linkedin.com/in/vanessalarco/"},
    {"title": "Steve Rein - VP Sales Americas - Cloudflare | LinkedIn",                  "url": "https://www.linkedin.com/in/steverein-cloudflare/"},
], min_required=3, max_keep=10))

print("Palo Alto Networks:", ingest_profiles("Palo Alto Networks", [
    {"title": "Nikesh Arora - Chairman and CEO - Palo Alto Networks | LinkedIn",         "url": "https://www.linkedin.com/in/nikesharora/"},
    {"title": "Dipak Golechha - CFO - Palo Alto Networks | LinkedIn",                    "url": "https://www.linkedin.com/in/dipak-golechha/"},
    {"title": "BJ Jenkins - President - Palo Alto Networks | LinkedIn",                  "url": "https://www.linkedin.com/in/bjjenkins/"},
    {"title": "Lee Klarich - Chief Product Officer - Palo Alto Networks | LinkedIn",     "url": "https://www.linkedin.com/in/leeklarich/"},
    {"title": "Wendy Bahr - Chief Partner Officer - Palo Alto Networks | LinkedIn",      "url": "https://www.linkedin.com/in/wendybahr/"},
    {"title": "Liane Hornsey - Chief People Officer - Palo Alto Networks | LinkedIn",   "url": "https://www.linkedin.com/in/lianehornsey/"},
    {"title": "Helmut Reisinger - CEO EMEA and LATAM - Palo Alto Networks | LinkedIn",  "url": "https://www.linkedin.com/in/helmutreisinger/"},
    {"title": "Simon Green - President JAPAC - Palo Alto Networks | LinkedIn",           "url": "https://www.linkedin.com/in/simon-green-panw/"},
    {"title": "Anand Oswal - SVP Network Security - Palo Alto Networks | LinkedIn",     "url": "https://www.linkedin.com/in/anandoswal/"},
    {"title": "Amit Singh - President Google Cloud - Palo Alto Networks | LinkedIn",    "url": "https://www.linkedin.com/in/amitsingh-panw/"},
], min_required=3, max_keep=10))

print("Replit:", ingest_profiles("Replit", [
    {"title": "Amjad Masad - CEO - Replit | LinkedIn",                                   "url": "https://www.linkedin.com/in/amasad/"},
    {"title": "Haya Odeh - Co-founder and COO - Replit | LinkedIn",                      "url": "https://www.linkedin.com/in/hayaodeh/"},
    {"title": "Michele Catasta - VP AI - Replit | LinkedIn",                             "url": "https://www.linkedin.com/in/pirroh/"},
    {"title": "Faris Masad - Head of Growth - Replit | LinkedIn",                        "url": "https://www.linkedin.com/in/faris-masad/"},
    {"title": "David Hershey - VP Engineering - Replit | LinkedIn",                      "url": "https://www.linkedin.com/in/david-hershey/"},
    {"title": "Connor Brewster - Head of Infrastructure - Replit | LinkedIn",            "url": "https://www.linkedin.com/in/connor-brewster/"},
    {"title": "Matt Iselin - Head of Partnerships - Replit | LinkedIn",                  "url": "https://www.linkedin.com/in/mattiselin/"},
    {"title": "Barron Webster - Head of Design - Replit | LinkedIn",                     "url": "https://www.linkedin.com/in/barron-webster/"},
    {"title": "Talor Browne - Head of Marketing - Replit | LinkedIn",                    "url": "https://www.linkedin.com/in/talor-browne/"},
    {"title": "Lena Ye - Head of Product - Replit | LinkedIn",                           "url": "https://www.linkedin.com/in/lenaye/"},
], min_required=3, max_keep=10))

print("eBay:", ingest_profiles("eBay", [
    {"title": "Jamie Iannone - President and CEO - eBay | LinkedIn",                     "url": "https://www.linkedin.com/in/jamieiannone/"},
    {"title": "Steve Priest - CFO - eBay | LinkedIn",                                    "url": "https://www.linkedin.com/in/steve-priest-ebay/"},
    {"title": "Jordan Sweetnam - SVP General Manager Americas - eBay | LinkedIn",        "url": "https://www.linkedin.com/in/jordansweetnam/"},
    {"title": "Cornelius Boone - Chief People Officer - eBay | LinkedIn",                "url": "https://www.linkedin.com/in/corneliusboone/"},
    {"title": "Victor Iannello - CTO - eBay | LinkedIn",                                 "url": "https://www.linkedin.com/in/victoriannello/"},
    {"title": "Alyssa Simpson Rochwerger - VP AI and Data - eBay | LinkedIn",            "url": "https://www.linkedin.com/in/alyssasimpsonrochwerger/"},
    {"title": "Peter Thompson - VP Product Management - eBay | LinkedIn",                "url": "https://www.linkedin.com/in/peter-thompson-ebay/"},
    {"title": "Andrea Stairs - VP and MD Canada - eBay | LinkedIn",                      "url": "https://www.linkedin.com/in/andreastairs/"},
    {"title": "Dawn Britt - SVP General Manager Europe - eBay | LinkedIn",               "url": "https://www.linkedin.com/in/dawn-britt/"},
    {"title": "Joele Frank - VP Communications - eBay | LinkedIn",                       "url": "https://www.linkedin.com/in/joele-frank/"},
], min_required=3, max_keep=10))

print("Duolingo:", ingest_profiles("Duolingo", [
    {"title": "Luis von Ahn - CEO - Duolingo | LinkedIn",                                "url": "https://www.linkedin.com/in/luisvonahn/"},
    {"title": "Matthew Rubinstein - CTO - Duolingo | LinkedIn",                          "url": "https://www.linkedin.com/in/matthewrubinstein/"},
    {"title": "Cem Kansu - Chief Product Officer - Duolingo | LinkedIn",                 "url": "https://www.linkedin.com/in/cemkansu/"},
    {"title": "Severin Hacker - Co-founder - Duolingo | LinkedIn",                       "url": "https://www.linkedin.com/in/severinhacker/"},
    {"title": "Bob Meese - Chief Business Officer - Duolingo | LinkedIn",                "url": "https://www.linkedin.com/in/bobmeese/"},
    {"title": "Kara McWilliams - VP People - Duolingo | LinkedIn",                       "url": "https://www.linkedin.com/in/kara-mcwilliams/"},
    {"title": "Zaria Parveen - VP Marketing - Duolingo | LinkedIn",                      "url": "https://www.linkedin.com/in/zaria-parveen/"},
    {"title": "Michael Uhl - VP Revenue - Duolingo | LinkedIn",                          "url": "https://www.linkedin.com/in/michaeluhl/"},
    {"title": "Nate Uy - Director of Product - Duolingo | LinkedIn",                     "url": "https://www.linkedin.com/in/nateuy/"},
    {"title": "Jackson Shuttleworth - Director Growth - Duolingo | LinkedIn",            "url": "https://www.linkedin.com/in/jackson-shuttleworth/"},
], min_required=3, max_keep=10))

print("NBA:", ingest_profiles("NBA", [
    {"title": "Adam Silver - Commissioner - NBA | LinkedIn",                              "url": "https://www.linkedin.com/in/adam-silver-nba/"},
    {"title": "Mark Tatum - Deputy Commissioner - NBA | LinkedIn",                       "url": "https://www.linkedin.com/in/mark-tatum/"},
    {"title": "Kerry Tatlock - EVP Chief Marketing Officer - NBA | LinkedIn",            "url": "https://www.linkedin.com/in/kerry-tatlock/"},
    {"title": "Kathy Behrens - President Social Responsibility - NBA | LinkedIn",        "url": "https://www.linkedin.com/in/kathy-behrens/"},
    {"title": "Dan Rossomondo - VP Media Strategy - NBA | LinkedIn",                     "url": "https://www.linkedin.com/in/danrossomondo/"},
    {"title": "David Denenberg - VP Strategy and Innovation - NBA | LinkedIn",           "url": "https://www.linkedin.com/in/daviddenenberg/"},
    {"title": "Jeff Thomas - VP Partnerships - NBA | LinkedIn",                          "url": "https://www.linkedin.com/in/jeff-thomas-nba/"},
    {"title": "Naz Long - VP Player Engagement - NBA | LinkedIn",                        "url": "https://www.linkedin.com/in/naz-long/"},
    {"title": "Akash Jain - VP Strategy - NBA | LinkedIn",                               "url": "https://www.linkedin.com/in/akash-jain-nfl/"},
    {"title": "Damani Leech - Chief Operating Officer - NBA | LinkedIn",                 "url": "https://www.linkedin.com/in/damanileech/"},
], min_required=3, max_keep=10))

print("Thermo Fisher Scientific:", ingest_profiles("Thermo Fisher Scientific", [
    {"title": "Marc Casper - Chairman President and CEO - Thermo Fisher | LinkedIn",     "url": "https://www.linkedin.com/in/marc-casper/"},
    {"title": "Stephen Williamson - SVP and CFO - Thermo Fisher | LinkedIn",             "url": "https://www.linkedin.com/in/stephen-williamson-tmo/"},
    {"title": "Michel Lagarde - EVP and COO - Thermo Fisher | LinkedIn",                 "url": "https://www.linkedin.com/in/michel-lagarde-tmo/"},
    {"title": "Fred Lowenbraun - EVP Chief Commercial Officer - Thermo Fisher | LinkedIn","url": "https://www.linkedin.com/in/fred-lowenbraun/"},
    {"title": "Gianluca Pettiti - SVP Life Sciences - Thermo Fisher | LinkedIn",         "url": "https://www.linkedin.com/in/gianluca-pettiti/"},
    {"title": "Peter Hornstra - VP Global Marketing - Thermo Fisher | LinkedIn",         "url": "https://www.linkedin.com/in/peter-hornstra/"},
    {"title": "Sanjiv Bhatt - VP Strategy - Thermo Fisher | LinkedIn",                  "url": "https://www.linkedin.com/in/sanjiv-bhatt-tmo/"},
    {"title": "Rebecca Scheuneman - VP Investor Relations - Thermo Fisher | LinkedIn",   "url": "https://www.linkedin.com/in/rebeccascheuneman/"},
    {"title": "Brenda Furlow - VP Associate General Counsel - Thermo Fisher | LinkedIn", "url": "https://www.linkedin.com/in/brendafurlow/"},
    {"title": "Lisa Bicker - VP HR Americas - Thermo Fisher | LinkedIn",                 "url": "https://www.linkedin.com/in/lisa-bicker/"},
], min_required=3, max_keep=10))

print("Tesla:", ingest_profiles("Tesla", [
    {"title": "Vaibhav Taneja - CFO - Tesla | LinkedIn",                                 "url": "https://www.linkedin.com/in/vaibhavtaneja/"},
    {"title": "Tom Zhu - SVP Automotive - Tesla | LinkedIn",                             "url": "https://www.linkedin.com/in/tomzhu-tesla/"},
    {"title": "Drew Baglino - SVP Powertrain - Tesla | LinkedIn",                        "url": "https://www.linkedin.com/in/drewbaglino/"},
    {"title": "Rohan Patel - VP Public Policy - Tesla | LinkedIn",                       "url": "https://www.linkedin.com/in/rohanpatel-tesla/"},
    {"title": "Grace Tao - VP Communications - Tesla | LinkedIn",                        "url": "https://www.linkedin.com/in/gracetao/"},
    {"title": "Felicia Mayo - Chief People Officer - Tesla | LinkedIn",                  "url": "https://www.linkedin.com/in/feliciamayo/"},
    {"title": "Omead Afshar - VP Operations - Tesla | LinkedIn",                         "url": "https://www.linkedin.com/in/omeadafshar/"},
    {"title": "Lars Moravy - VP Vehicle Engineering - Tesla | LinkedIn",                 "url": "https://www.linkedin.com/in/larsmorаvy/"},
    {"title": "Zachary Kirkhorn - Former CFO - Tesla | LinkedIn",                        "url": "https://www.linkedin.com/in/zacharykirkhorn/"},
    {"title": "Phil Kassouf - VP Starlink Sales - Tesla | LinkedIn",                     "url": "https://www.linkedin.com/in/philkassouf/"},
], min_required=3, max_keep=10))

print("SAP:", ingest_profiles("SAP", [
    {"title": "Christian Klein - CEO - SAP | LinkedIn",                                  "url": "https://www.linkedin.com/in/christianklein/"},
    {"title": "Dominik Asam - CFO - SAP | LinkedIn",                                     "url": "https://www.linkedin.com/in/dominikasam/"},
    {"title": "Thomas Saueressig - President Product Engineering - SAP | LinkedIn",     "url": "https://www.linkedin.com/in/thomassaueressig/"},
    {"title": "Scott Russell - President Customer Success - SAP | LinkedIn",             "url": "https://www.linkedin.com/in/scottrussell-sap/"},
    {"title": "Julia White - Chief Marketing Officer - SAP | LinkedIn",                  "url": "https://www.linkedin.com/in/juliawhite/"},
    {"title": "Muhammad Alam - President Industries - SAP | LinkedIn",                   "url": "https://www.linkedin.com/in/muhammadalam-sap/"},
    {"title": "Juergen Mueller - CTO - SAP | LinkedIn",                                  "url": "https://www.linkedin.com/in/juergenmueller-sap/"},
    {"title": "Sabine Bendiek - Chief People Officer - SAP | LinkedIn",                  "url": "https://www.linkedin.com/in/sabinebendiek/"},
    {"title": "Adaire Fox-Martin - President EMEA - SAP | LinkedIn",                    "url": "https://www.linkedin.com/in/adairefoxmartin/"},
    {"title": "Naz Stoelinga - General Counsel - SAP | LinkedIn",                        "url": "https://www.linkedin.com/in/nazstoelinga/"},
], min_required=3, max_keep=10))

print("Marriott:", ingest_profiles("Marriott", [
    {"title": "Anthony Capuano - President and CEO - Marriott | LinkedIn",               "url": "https://www.linkedin.com/in/anthony-capuano/"},
    {"title": "Leeny Oberg - CFO - Marriott | LinkedIn",                                 "url": "https://www.linkedin.com/in/leenyoberg/"},
    {"title": "Drew Pinto - EVP Global Operations - Marriott | LinkedIn",                "url": "https://www.linkedin.com/in/drewpinto/"},
    {"title": "David Rodriguez - EVP Chief HR Officer - Marriott | LinkedIn",            "url": "https://www.linkedin.com/in/davidrodriguez-marriott/"},
    {"title": "Julius Robinson - Chief Sales and Marketing Officer - Marriott | LinkedIn","url": "https://www.linkedin.com/in/juliusrobinson/"},
    {"title": "Craig Smith - EVP International - Marriott | LinkedIn",                   "url": "https://www.linkedin.com/in/craigsmith-marriott/"},
    {"title": "Carlton Ervin - EVP Lodging Development - Marriott | LinkedIn",           "url": "https://www.linkedin.com/in/carltonervin/"},
    {"title": "Tina Edmundson - Chief Brand Officer - Marriott | LinkedIn",              "url": "https://www.linkedin.com/in/tinaedmundson/"},
    {"title": "Karin Timpone - Global CMO - Marriott | LinkedIn",                        "url": "https://www.linkedin.com/in/karintimpone/"},
    {"title": "Stephanie Linnartz - Former President - Marriott | LinkedIn",             "url": "https://www.linkedin.com/in/stephanielinnartz/"},
], min_required=3, max_keep=10))

print("Coinbase:", ingest_profiles("Coinbase", [
    {"title": "Brian Armstrong - CEO - Coinbase | LinkedIn",                             "url": "https://www.linkedin.com/in/barmstrong/"},
    {"title": "Alesia Haas - CFO - Coinbase | LinkedIn",                                 "url": "https://www.linkedin.com/in/alesiahaas/"},
    {"title": "Emilie Choi - President and COO - Coinbase | LinkedIn",                   "url": "https://www.linkedin.com/in/emiliechoi/"},
    {"title": "L.J. Brock - Chief People Officer - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/ljbrock/"},
    {"title": "Paul Grewal - Chief Legal Officer - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/paulgrewal/"},
    {"title": "Surojit Chatterjee - Chief Product Officer - Coinbase | LinkedIn",        "url": "https://www.linkedin.com/in/surojitchatterjee/"},
    {"title": "Tom Duff Gordon - VP Commercial - Coinbase | LinkedIn",                   "url": "https://www.linkedin.com/in/tomduffgordon/"},
    {"title": "Max Branzburg - VP Product Consumer - Coinbase | LinkedIn",               "url": "https://www.linkedin.com/in/maxbranzburg/"},
    {"title": "Nana Murugesan - VP International - Coinbase | LinkedIn",                 "url": "https://www.linkedin.com/in/nanamurugesan/"},
    {"title": "Jeff Haul - VP Engineering - Coinbase | LinkedIn",                        "url": "https://www.linkedin.com/in/jeffhaul/"},
], min_required=3, max_keep=10))

print("Qualcomm:", ingest_profiles("Qualcomm", [
    {"title": "Cristiano Amon - President and CEO - Qualcomm | LinkedIn",                "url": "https://www.linkedin.com/in/cristiano-amon/"},
    {"title": "Akash Palkhiwala - CFO - Qualcomm | LinkedIn",                            "url": "https://www.linkedin.com/in/akashpalkhiwala/"},
    {"title": "Alex Katouzian - SVP Mobile - Qualcomm | LinkedIn",                       "url": "https://www.linkedin.com/in/alexkatouzian/"},
    {"title": "Don McGuire - Chief Marketing Officer - Qualcomm | LinkedIn",             "url": "https://www.linkedin.com/in/donmcguire-qualcomm/"},
    {"title": "Judy Brown - Chief People Officer - Qualcomm | LinkedIn",                 "url": "https://www.linkedin.com/in/judybrown-qualcomm/"},
    {"title": "Nakul Duggal - SVP Automotive - Qualcomm | LinkedIn",                     "url": "https://www.linkedin.com/in/nakulduggal/"},
    {"title": "Raj Talluri - SVP Industrial IoT - Qualcomm | LinkedIn",                  "url": "https://www.linkedin.com/in/rajtalluri/"},
    {"title": "Durga Malladi - SVP Engineering 5G - Qualcomm | LinkedIn",                "url": "https://www.linkedin.com/in/durgamalladi/"},
    {"title": "Francisco Jeronimo - VP Strategy EMEA - Qualcomm | LinkedIn",            "url": "https://www.linkedin.com/in/franciscojeronimo/"},
    {"title": "Brian Modoff - VP Investor Relations - Qualcomm | LinkedIn",              "url": "https://www.linkedin.com/in/brianmodoff/"},
], min_required=3, max_keep=10))

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
    {"title": "Tariq Hassan - CMO - Reddit | LinkedIn",                                  "url": "https://www.linkedin.com/in/tariqhassan/"},
], min_required=3, max_keep=10))

print("Samsung:", ingest_profiles("Samsung", [
    {"title": "TM Roh - President Mobile - Samsung Electronics | LinkedIn",              "url": "https://www.linkedin.com/in/tmroh/"},
    {"title": "Mark Holloway - VP Corporate Marketing Americas - Samsung | LinkedIn",   "url": "https://www.linkedin.com/in/markholloway-samsung/"},
    {"title": "Stephanie Choi - EVP CMO Samsung Mobile | LinkedIn",                     "url": "https://www.linkedin.com/in/stephaniechoi-samsung/"},
    {"title": "Mike Lawrie - SVP Samsung Americas | LinkedIn",                           "url": "https://www.linkedin.com/in/mikelawrie-samsung/"},
    {"title": "Jon Gabay - VP Business Development Samsung Semiconductor | LinkedIn",   "url": "https://www.linkedin.com/in/jongabay/"},
    {"title": "Sangjoon Park - President Samsung Research America | LinkedIn",           "url": "https://www.linkedin.com/in/sangjoonpark/"},
    {"title": "Patrick Chomet - EVP Customer Experience - Samsung Mobile | LinkedIn",   "url": "https://www.linkedin.com/in/patrickchomet/"},
    {"title": "Yongin Park - VP Strategy - Samsung Electronics | LinkedIn",              "url": "https://www.linkedin.com/in/yonginpark/"},
    {"title": "KH Kim - Vice Chairman - Samsung Electronics | LinkedIn",                 "url": "https://www.linkedin.com/in/khkim-samsung/"},
    {"title": "Victor Chang - VP Developer Programs - Samsung | LinkedIn",               "url": "https://www.linkedin.com/in/victorchang-samsung/"},
], min_required=3, max_keep=10))

print("CrowdStrike:", ingest_profiles("CrowdStrike", [
    {"title": "George Kurtz - CEO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/georgekurtz/"},
    {"title": "Burt Podbere - CFO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/burtpodbere/"},
    {"title": "Mike Sentonas - President - CrowdStrike | LinkedIn",                      "url": "https://www.linkedin.com/in/mikesentonas/"},
    {"title": "Shawn Henry - President Field Operations - CrowdStrike | LinkedIn",       "url": "https://www.linkedin.com/in/shawnhenry/"},
    {"title": "Elia Zaitsev - CTO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/eliazaitsev/"},
    {"title": "Raj Rajamani - CPO - CrowdStrike | LinkedIn",                             "url": "https://www.linkedin.com/in/rajrajamani/"},
    {"title": "TJ Erickson - Chief People Officer - CrowdStrike | LinkedIn",             "url": "https://www.linkedin.com/in/tjerickson/"},
    {"title": "Daniel Bernard - Chief Business Officer - CrowdStrike | LinkedIn",        "url": "https://www.linkedin.com/in/danielbernard-crwd/"},
    {"title": "Drew Bagley - VP Privacy and Cyber Policy - CrowdStrike | LinkedIn",     "url": "https://www.linkedin.com/in/drewbagley/"},
    {"title": "Jenny Menna - VP Public Sector - CrowdStrike | LinkedIn",                 "url": "https://www.linkedin.com/in/jennymenna/"},
], min_required=3, max_keep=10))

print("Datadog:", ingest_profiles("Datadog", [
    {"title": "Olivier Pomel - CEO - Datadog | LinkedIn",                                "url": "https://www.linkedin.com/in/olivierpomel/"},
    {"title": "David Obstler - CFO - Datadog | LinkedIn",                                "url": "https://www.linkedin.com/in/davidobstler/"},
    {"title": "Alexis Le-Quoc - CTO - Datadog | LinkedIn",                               "url": "https://www.linkedin.com/in/alexislequoc/"},
    {"title": "Dan Fougere - Chief Revenue Officer - Datadog | LinkedIn",                "url": "https://www.linkedin.com/in/danfougere/"},
    {"title": "Amanda Kleha - Chief Customer Officer - Datadog | LinkedIn",              "url": "https://www.linkedin.com/in/amandakleha/"},
    {"title": "Alex Rosemblat - VP Marketing - Datadog | LinkedIn",                      "url": "https://www.linkedin.com/in/alexrosemblat/"},
    {"title": "Jay Snyder - SVP Global Sales - Datadog | LinkedIn",                      "url": "https://www.linkedin.com/in/jaysnyder-datadog/"},
    {"title": "Ilan Rabinovitch - SVP Product - Datadog | LinkedIn",                     "url": "https://www.linkedin.com/in/irabinovitch/"},
    {"title": "Yrieix Garnier - VP People - Datadog | LinkedIn",                         "url": "https://www.linkedin.com/in/yrieixgarnier/"},
    {"title": "Renaud Bouchard - VP Engineering - Datadog | LinkedIn",                   "url": "https://www.linkedin.com/in/renaudbouchard/"},
], min_required=3, max_keep=10))

print("Confluent:", ingest_profiles("Confluent", [
    {"title": "Jay Kreps - CEO - Confluent | LinkedIn",                                  "url": "https://www.linkedin.com/in/jaykreps/"},
    {"title": "Rohan Sivaram - CFO - Confluent | LinkedIn",                              "url": "https://www.linkedin.com/in/rohansivaram/"},
    {"title": "Erica Schultz - President Field Operations - Confluent | LinkedIn",       "url": "https://www.linkedin.com/in/ericaschultz/"},
    {"title": "Greg Mefford - Chief Revenue Officer - Confluent | LinkedIn",             "url": "https://www.linkedin.com/in/gregmefford/"},
    {"title": "Hima Garimella - VP Engineering - Confluent | LinkedIn",                  "url": "https://www.linkedin.com/in/himagarimella/"},
    {"title": "Chad Verbowski - VP Product - Confluent | LinkedIn",                      "url": "https://www.linkedin.com/in/chadverbowski/"},
    {"title": "Will LaForest - VP Technology Strategy - Confluent | LinkedIn",           "url": "https://www.linkedin.com/in/willlaforest/"},
    {"title": "Laura King - Chief People Officer - Confluent | LinkedIn",                "url": "https://www.linkedin.com/in/lauraking-confluent/"},
    {"title": "Krish Krishnan - VP Sales - Confluent | LinkedIn",                        "url": "https://www.linkedin.com/in/krishkrishnan-confluent/"},
    {"title": "Shayde Christian - Chief Data Officer - Confluent | LinkedIn",            "url": "https://www.linkedin.com/in/shaydechristian/"},
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
print("\n" + "="*60); print("STEP 4: Personalizing — FV template"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="fv",
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
