"""FV Batch 6 — 25 new tech/innovation companies, 10 emails each, eleynxiong@berkeley.edu."""
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
    {"name": "Canva",                        "domain": "canva.com",             "industry": "Design Platform / Creative Tools / SaaS",          "email_pattern": "first.last"},
    {"name": "Asana",                        "domain": "asana.com",             "industry": "Project Management / Work Management / SaaS",       "email_pattern": "first.last"},
    {"name": "Monday.com",                   "domain": "monday.com",            "industry": "Work OS / Project Management / Collaboration",      "email_pattern": "first.last"},
    {"name": "Klaviyo",                      "domain": "klaviyo.com",           "industry": "Email Marketing / SMS / Customer Data Platform",    "email_pattern": "first.last"},
    {"name": "Twilio",                       "domain": "twilio.com",            "industry": "Communications API / CPaaS / Messaging",            "email_pattern": "first.last"},
    {"name": "Zendesk",                      "domain": "zendesk.com",           "industry": "Customer Experience / CRM / Support Software",      "email_pattern": "first.last"},
    {"name": "Okta",                         "domain": "okta.com",              "industry": "Identity / Zero Trust / Security / SaaS",           "email_pattern": "first.last"},
    {"name": "PagerDuty",                    "domain": "pagerduty.com",         "industry": "DevOps / Incident Management / AIOps",              "email_pattern": "first.last"},
    {"name": "UiPath",                       "domain": "uipath.com",            "industry": "RPA / Process Automation / AI Agents",              "email_pattern": "first.last"},
    {"name": "C3.ai",                        "domain": "c3.ai",                 "industry": "Enterprise AI / Machine Learning / SaaS",           "email_pattern": "first.last"},
    {"name": "Samsara",                      "domain": "samsara.com",           "industry": "IoT / Fleet Management / Connected Operations",      "email_pattern": "first.last"},
    {"name": "Anyscale",                     "domain": "anyscale.com",          "industry": "ML Infrastructure / Distributed Computing / AI",    "email_pattern": "first.last"},
    {"name": "Weights and Biases",           "domain": "wandb.ai",             "industry": "MLOps / AI Developer Tools / Experiment Tracking",  "email_pattern": "first.last"},
    {"name": "Character.ai",                 "domain": "character.ai",          "industry": "Consumer AI / Conversational AI / LLMs",            "email_pattern": "first.last"},
    {"name": "Benchling",                    "domain": "benchling.com",         "industry": "Life Sciences R&D / Biotech SaaS / Lab Software",   "email_pattern": "first.last"},
    {"name": "Recursion Pharmaceuticals",    "domain": "recursion.com",         "industry": "AI Drug Discovery / Biotech / Clinical Research",   "email_pattern": "first.last"},
    {"name": "Toast",                        "domain": "toasttab.com",          "industry": "Restaurant Tech / POS / Hospitality SaaS",          "email_pattern": "first.last"},
    {"name": "Mixpanel",                     "domain": "mixpanel.com",          "industry": "Product Analytics / Event Tracking / SaaS",         "email_pattern": "first.last"},
    {"name": "Miro",                         "domain": "miro.com",              "industry": "Visual Collaboration / Whiteboard / SaaS",          "email_pattern": "first.last"},
    {"name": "Airtable",                     "domain": "airtable.com",          "industry": "No-Code Database / Work Platform / SaaS",           "email_pattern": "first.last"},
    {"name": "Webflow",                      "domain": "webflow.com",           "industry": "No-Code Web Dev / CMS / Visual Development",        "email_pattern": "first.last"},
    {"name": "Carta",                        "domain": "carta.com",             "industry": "Cap Table / Equity Management / VC/Startup Tools",  "email_pattern": "first.last"},
    {"name": "Lattice",                      "domain": "lattice.com",           "industry": "People Management / Performance / HR Tech",         "email_pattern": "first.last"},
    {"name": "Culture Amp",                  "domain": "cultureamp.com",        "industry": "Employee Experience / HR Analytics / Engagement",   "email_pattern": "first.last"},
    {"name": "Descript",                     "domain": "descript.com",          "industry": "AI Video/Audio Editing / Content Creation / SaaS",  "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Batch 6 - July 2026"
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

print("Canva:", ingest_profiles("Canva", [
    {"title": "Melanie Perkins - Co-Founder and CEO - Canva | LinkedIn",                           "url": "https://www.linkedin.com/in/melanieperkins/"},
    {"title": "Cliff Obrecht - Co-Founder and COO - Canva | LinkedIn",                             "url": "https://www.linkedin.com/in/cliffobrecht/"},
    {"title": "Cameron Adams - Co-Founder and CPO - Canva | LinkedIn",                             "url": "https://www.linkedin.com/in/cameronadams/"},
    {"title": "Rob Kawalsky - CFO - Canva | LinkedIn",                                             "url": "https://www.linkedin.com/in/robkawalsky/"},
    {"title": "Jennie Rogerson - Chief People Officer - Canva | LinkedIn",                         "url": "https://www.linkedin.com/in/jennierogerson/"},
    {"title": "Juliet Scott-Croxford - Chief Revenue Officer - Canva | LinkedIn",                  "url": "https://www.linkedin.com/in/julietscottcroxford/"},
    {"title": "David Tse - SVP Engineering - Canva | LinkedIn",                                    "url": "https://www.linkedin.com/in/davidtse-canva/"},
    {"title": "Zach Kitschke - Chief Marketing Officer - Canva | LinkedIn",                        "url": "https://www.linkedin.com/in/zachkitschke/"},
    {"title": "Nicolas Chu - SVP Enterprise - Canva | LinkedIn",                                   "url": "https://www.linkedin.com/in/nicolaschu-canva/"},
    {"title": "Magnus Mahieu - VP Sales EMEA - Canva | LinkedIn",                                  "url": "https://www.linkedin.com/in/magnusmahieu-canva/"},
], min_required=3, max_keep=10))

print("Asana:", ingest_profiles("Asana", [
    {"title": "Dustin Moskovitz - Co-Founder and CEO - Asana | LinkedIn",                          "url": "https://www.linkedin.com/in/dustinmoskovitz/"},
    {"title": "Tim Wan - CFO - Asana | LinkedIn",                                                  "url": "https://www.linkedin.com/in/timwan-asana/"},
    {"title": "Chris Farinacci - COO - Asana | LinkedIn",                                          "url": "https://www.linkedin.com/in/chrisfarinacci/"},
    {"title": "Alex Hood - Chief Product Officer - Asana | LinkedIn",                              "url": "https://www.linkedin.com/in/alexhood-asana/"},
    {"title": "Sonya Dhar - Chief People Officer - Asana | LinkedIn",                              "url": "https://www.linkedin.com/in/sonyadhar-asana/"},
    {"title": "Dave King - Chief Revenue Officer - Asana | LinkedIn",                              "url": "https://www.linkedin.com/in/daveking-asana/"},
    {"title": "Shannon Stubo - Chief Marketing Officer - Asana | LinkedIn",                        "url": "https://www.linkedin.com/in/shannonstubo/"},
    {"title": "Oliver Jay - SVP APAC and EMEA Sales - Asana | LinkedIn",                          "url": "https://www.linkedin.com/in/oliverjay-asana/"},
    {"title": "Rebecca Hinds - VP Research - Asana | LinkedIn",                                    "url": "https://www.linkedin.com/in/rebeccahinds-asana/"},
    {"title": "JP Maheu - Chief Customer Officer - Asana | LinkedIn",                              "url": "https://www.linkedin.com/in/jpmaheu-asana/"},
], min_required=3, max_keep=10))

print("Monday.com:", ingest_profiles("Monday.com", [
    {"title": "Roy Mann - Co-CEO and Co-Founder - Monday.com | LinkedIn",                          "url": "https://www.linkedin.com/in/roymann/"},
    {"title": "Eran Zinman - Co-CEO and Co-Founder - Monday.com | LinkedIn",                       "url": "https://www.linkedin.com/in/eranzinman/"},
    {"title": "Eliran Glazer - CFO - Monday.com | LinkedIn",                                       "url": "https://www.linkedin.com/in/eliranglazer/"},
    {"title": "Yoni Osherov - Chief Revenue Officer - Monday.com | LinkedIn",                      "url": "https://www.linkedin.com/in/yoniosherov/"},
    {"title": "Adi Sherzer - Chief Product Officer - Monday.com | LinkedIn",                       "url": "https://www.linkedin.com/in/adisherzer-monday/"},
    {"title": "Lior Cohen - VP Sales - Monday.com | LinkedIn",                                     "url": "https://www.linkedin.com/in/liorcohen-monday/"},
    {"title": "Hila Shitrit Nissim - Chief HR Officer - Monday.com | LinkedIn",                    "url": "https://www.linkedin.com/in/hilashitritmondaydotcom/"},
    {"title": "Emily Kramer - VP Marketing - Monday.com | LinkedIn",                               "url": "https://www.linkedin.com/in/emilykramer-monday/"},
    {"title": "Tomer Cohen - Chief Technology Officer - Monday.com | LinkedIn",                    "url": "https://www.linkedin.com/in/tomercohen-monday/"},
    {"title": "Yaniv Yarmak - VP Enterprise Sales - Monday.com | LinkedIn",                        "url": "https://www.linkedin.com/in/yanivyarmak/"},
], min_required=3, max_keep=10))

print("Klaviyo:", ingest_profiles("Klaviyo", [
    {"title": "Andrew Bialecki - Co-Founder and CEO - Klaviyo | LinkedIn",                         "url": "https://www.linkedin.com/in/andrewbialecki/"},
    {"title": "Ed Hallen - Co-Founder and CPO - Klaviyo | LinkedIn",                               "url": "https://www.linkedin.com/in/edhallen/"},
    {"title": "Amanda Whalen - CFO - Klaviyo | LinkedIn",                                          "url": "https://www.linkedin.com/in/amandawhalen-klaviyo/"},
    {"title": "Bjoern Westermann - Chief Revenue Officer - Klaviyo | LinkedIn",                    "url": "https://www.linkedin.com/in/bjoernwestermann/"},
    {"title": "Ashley Grech - Chief People Officer - Klaviyo | LinkedIn",                          "url": "https://www.linkedin.com/in/ashleygrech-klaviyo/"},
    {"title": "Alex Muldaur - Chief Marketing Officer - Klaviyo | LinkedIn",                       "url": "https://www.linkedin.com/in/alexmuldaur-klaviyo/"},
    {"title": "Panos Siozos - Chief Technology Officer - Klaviyo | LinkedIn",                      "url": "https://www.linkedin.com/in/panossiozos/"},
    {"title": "Grant Deken - VP Partnerships - Klaviyo | LinkedIn",                                "url": "https://www.linkedin.com/in/grantdeken-klaviyo/"},
    {"title": "Steve Cannon - VP Enterprise Sales - Klaviyo | LinkedIn",                           "url": "https://www.linkedin.com/in/stevecannon-klaviyo/"},
    {"title": "Katie Reps - VP Customer Success - Klaviyo | LinkedIn",                             "url": "https://www.linkedin.com/in/katiereps-klaviyo/"},
], min_required=3, max_keep=10))

print("Twilio:", ingest_profiles("Twilio", [
    {"title": "Khozema Shipchandler - CEO - Twilio | LinkedIn",                                    "url": "https://www.linkedin.com/in/khozemashipchandler/"},
    {"title": "Aidan Viggiano - CFO - Twilio | LinkedIn",                                          "url": "https://www.linkedin.com/in/aidanviggiano/"},
    {"title": "Inbal Shani - Chief Product Officer - Twilio | LinkedIn",                           "url": "https://www.linkedin.com/in/inbalshani/"},
    {"title": "Thomas Hadfield - SVP Engineering - Twilio | LinkedIn",                             "url": "https://www.linkedin.com/in/thomashadfield-twilio/"},
    {"title": "Dana Wagner - Chief Legal Officer - Twilio | LinkedIn",                             "url": "https://www.linkedin.com/in/danawagner-twilio/"},
    {"title": "Joyce Kim - Chief Marketing Officer - Twilio | LinkedIn",                           "url": "https://www.linkedin.com/in/joycewkim/"},
    {"title": "Simonetta Turek - Chief Product and Engineering Officer - Twilio | LinkedIn",       "url": "https://www.linkedin.com/in/simonettaturek/"},
    {"title": "Mark Lindsey - Chief Revenue Officer - Twilio | LinkedIn",                          "url": "https://www.linkedin.com/in/marklindsey-twilio/"},
    {"title": "Kathryn Murphy - Chief Customer Experience Officer - Twilio | LinkedIn",            "url": "https://www.linkedin.com/in/kathrynmurphy-twilio/"},
    {"title": "Tyler Renner - Chief People Officer - Twilio | LinkedIn",                           "url": "https://www.linkedin.com/in/tylerrenner-twilio/"},
], min_required=3, max_keep=10))

print("Zendesk:", ingest_profiles("Zendesk", [
    {"title": "Tom Eggemeier - CEO - Zendesk | LinkedIn",                                          "url": "https://www.linkedin.com/in/tomeggemeier/"},
    {"title": "Shawn Price - President - Zendesk | LinkedIn",                                      "url": "https://www.linkedin.com/in/shawnprice-zendesk/"},
    {"title": "Caitlin Fennessy - Chief People Officer - Zendesk | LinkedIn",                      "url": "https://www.linkedin.com/in/caitlinfennessy/"},
    {"title": "Malcolm Bain - Chief Legal Officer - Zendesk | LinkedIn",                           "url": "https://www.linkedin.com/in/malcolmbain-zendesk/"},
    {"title": "Adrian McDermott - Chief Technology Officer - Zendesk | LinkedIn",                  "url": "https://www.linkedin.com/in/adrianmcdermott-zendesk/"},
    {"title": "Jeff Titterton - Chief Operating Officer - Zendesk | LinkedIn",                     "url": "https://www.linkedin.com/in/jefftitterton-zendesk/"},
    {"title": "Karen Muldoon - Chief Financial Officer - Zendesk | LinkedIn",                      "url": "https://www.linkedin.com/in/karenmuldoon-zendesk/"},
    {"title": "Kate Ahlering - Chief Revenue Officer - Zendesk | LinkedIn",                        "url": "https://www.linkedin.com/in/kateahlering/"},
    {"title": "Colleen Berube - Former CIO - Zendesk | LinkedIn",                                  "url": "https://www.linkedin.com/in/colleenberube/"},
    {"title": "Christine Hespe - SVP Marketing - Zendesk | LinkedIn",                              "url": "https://www.linkedin.com/in/christinehespe-zendesk/"},
], min_required=3, max_keep=10))

print("Okta:", ingest_profiles("Okta", [
    {"title": "Todd McKinnon - Co-Founder and CEO - Okta | LinkedIn",                              "url": "https://www.linkedin.com/in/toddmckinnon/"},
    {"title": "Brett Tighe - CFO - Okta | LinkedIn",                                               "url": "https://www.linkedin.com/in/bretttighe/"},
    {"title": "J.J. Agha - Chief Customer Officer - Okta | LinkedIn",                             "url": "https://www.linkedin.com/in/jjagha/"},
    {"title": "Eunice Kim - Chief Product Officer - Okta | LinkedIn",                              "url": "https://www.linkedin.com/in/eunicek/"},
    {"title": "Sagnik Nandy - President Technology - Okta | LinkedIn",                             "url": "https://www.linkedin.com/in/sagniknandy/"},
    {"title": "Angela Moran - Chief People Officer - Okta | LinkedIn",                             "url": "https://www.linkedin.com/in/angelamoran-okta/"},
    {"title": "Jon Siegler - Chief Legal Officer - Okta | LinkedIn",                               "url": "https://www.linkedin.com/in/jonsiegler-okta/"},
    {"title": "Brian Goldfarb - Chief Marketing Officer - Okta | LinkedIn",                        "url": "https://www.linkedin.com/in/briangoldfarb/"},
    {"title": "Steve Rowland - Chief Revenue Officer - Okta | LinkedIn",                           "url": "https://www.linkedin.com/in/steverowland-okta/"},
    {"title": "Frederic Kerrest - Co-Founder and Vice Chairman - Okta | LinkedIn",                 "url": "https://www.linkedin.com/in/fkerrest/"},
], min_required=3, max_keep=10))

print("PagerDuty:", ingest_profiles("PagerDuty", [
    {"title": "Jennifer Tejada - Chairwoman and CEO - PagerDuty | LinkedIn",                       "url": "https://www.linkedin.com/in/jennitertejada/"},
    {"title": "Howard Wilson - CFO - PagerDuty | LinkedIn",                                        "url": "https://www.linkedin.com/in/howardwilson-pagerduty/"},
    {"title": "Tina Hsiao - Chief People Officer - PagerDuty | LinkedIn",                          "url": "https://www.linkedin.com/in/tinahsiao-pagerduty/"},
    {"title": "Sean Scott - Chief Product and Technology Officer - PagerDuty | LinkedIn",          "url": "https://www.linkedin.com/in/seanscott-pagerduty/"},
    {"title": "Dave Justice - Chief Revenue Officer - PagerDuty | LinkedIn",                       "url": "https://www.linkedin.com/in/davejustice-pagerduty/"},
    {"title": "Shelby Vetter - Chief Marketing Officer - PagerDuty | LinkedIn",                    "url": "https://www.linkedin.com/in/shelbyvetter-pagerduty/"},
    {"title": "Stacey Giamalis - Chief Customer Officer - PagerDuty | LinkedIn",                   "url": "https://www.linkedin.com/in/staceygiamalis/"},
    {"title": "James Peal - Chief Legal Officer - PagerDuty | LinkedIn",                           "url": "https://www.linkedin.com/in/jamespeal-pagerduty/"},
    {"title": "Jeff Lawson - Former CEO and Co-Founder - PagerDuty | LinkedIn",                   "url": "https://www.linkedin.com/in/jefflawsontwilio/"},
    {"title": "Alex Solomon - Co-Founder and CTO - PagerDuty | LinkedIn",                         "url": "https://www.linkedin.com/in/alexsolomon-pagerduty/"},
], min_required=3, max_keep=10))

print("UiPath:", ingest_profiles("UiPath", [
    {"title": "Daniel Dines - Founder and Chief Innovation Officer - UiPath | LinkedIn",           "url": "https://www.linkedin.com/in/danieldines/"},
    {"title": "Rob Enslin - CEO - UiPath | LinkedIn",                                              "url": "https://www.linkedin.com/in/robenslin/"},
    {"title": "Ashim Gupta - CFO - UiPath | LinkedIn",                                             "url": "https://www.linkedin.com/in/ashimgupta/"},
    {"title": "Graham Sheldon - Chief Product Officer - UiPath | LinkedIn",                        "url": "https://www.linkedin.com/in/grahamsheldon-uipath/"},
    {"title": "Marius Tirca - Chief Technology Officer - UiPath | LinkedIn",                       "url": "https://www.linkedin.com/in/mariustirca/"},
    {"title": "Carol Sawdye - Chief Operating Officer - UiPath | LinkedIn",                        "url": "https://www.linkedin.com/in/carolsawdye/"},
    {"title": "Brigette McInnis-Day - Chief People Officer - UiPath | LinkedIn",                   "url": "https://www.linkedin.com/in/brigette-day/"},
    {"title": "Raghu Subramanian - SVP Revenue Acceleration - UiPath | LinkedIn",                  "url": "https://www.linkedin.com/in/raghusubramanian-uipath/"},
    {"title": "Thomas Hansen - Chief Revenue Officer - UiPath | LinkedIn",                         "url": "https://www.linkedin.com/in/thomashansen-uipath/"},
    {"title": "Christopher Weber - SVP General Counsel - UiPath | LinkedIn",                       "url": "https://www.linkedin.com/in/christopherweber-uipath/"},
], min_required=3, max_keep=10))

print("C3.ai:", ingest_profiles("C3.ai", [
    {"title": "Tom Siebel - Chairman and CEO - C3.ai | LinkedIn",                                  "url": "https://www.linkedin.com/in/tomsiebel/"},
    {"title": "Juho Parkkinen - CFO - C3.ai | LinkedIn",                                           "url": "https://www.linkedin.com/in/juhoparkkinen/"},
    {"title": "Houman Behzadi - Chief AI Officer - C3.ai | LinkedIn",                              "url": "https://www.linkedin.com/in/houmanb/"},
    {"title": "Ed Abbo - President and CTO - C3.ai | LinkedIn",                                    "url": "https://www.linkedin.com/in/edabbo/"},
    {"title": "Clint Sherrill - SVP Sales - C3.ai | LinkedIn",                                     "url": "https://www.linkedin.com/in/clintsherrill/"},
    {"title": "Prithviraj Maitra - SVP Products - C3.ai | LinkedIn",                               "url": "https://www.linkedin.com/in/prithvirajmaitra/"},
    {"title": "Anne Teutschbein - SVP General Counsel - C3.ai | LinkedIn",                         "url": "https://www.linkedin.com/in/anneteutschbein/"},
    {"title": "Vince Campisi - COO - C3.ai | LinkedIn",                                            "url": "https://www.linkedin.com/in/vincecampisi/"},
    {"title": "Susan Carstensen - SVP Finance - C3.ai | LinkedIn",                                 "url": "https://www.linkedin.com/in/susancarstensen-c3/"},
    {"title": "Cate White - VP Marketing - C3.ai | LinkedIn",                                      "url": "https://www.linkedin.com/in/catewhite-c3ai/"},
], min_required=3, max_keep=10))

print("Samsara:", ingest_profiles("Samsara", [
    {"title": "Sanjit Biswas - Co-Founder and CEO - Samsara | LinkedIn",                           "url": "https://www.linkedin.com/in/sanjitbiswas/"},
    {"title": "Kiren Sekar - Co-Founder and CPO - Samsara | LinkedIn",                             "url": "https://www.linkedin.com/in/kirensekar/"},
    {"title": "Dominic Phillips - CFO - Samsara | LinkedIn",                                       "url": "https://www.linkedin.com/in/dominicphillips-samsara/"},
    {"title": "Sarah Patterson - COO - Samsara | LinkedIn",                                        "url": "https://www.linkedin.com/in/sarahpatterson-samsara/"},
    {"title": "Jeff Hausman - Chief Product Officer - Samsara | LinkedIn",                         "url": "https://www.linkedin.com/in/jeffhausman/"},
    {"title": "Maggie Hott - VP Sales - Samsara | LinkedIn",                                       "url": "https://www.linkedin.com/in/maggiehott-samsara/"},
    {"title": "Stephanie Schnabel - Chief Marketing Officer - Samsara | LinkedIn",                 "url": "https://www.linkedin.com/in/stephanieschnabel-samsara/"},
    {"title": "Jim Kapteyn - VP Business Development - Samsara | LinkedIn",                        "url": "https://www.linkedin.com/in/jimkapteyn-samsara/"},
    {"title": "Sheila Lam - VP Engineering - Samsara | LinkedIn",                                  "url": "https://www.linkedin.com/in/sheilalam-samsara/"},
    {"title": "Lauren Spiteri - VP People - Samsara | LinkedIn",                                   "url": "https://www.linkedin.com/in/laurenspiteri-samsara/"},
], min_required=3, max_keep=10))

print("Anyscale:", ingest_profiles("Anyscale", [
    {"title": "Robert Nishihara - Co-Founder and CEO - Anyscale | LinkedIn",                       "url": "https://www.linkedin.com/in/robertnishihara/"},
    {"title": "Ion Stoica - Co-Founder and Board Member - Anyscale | LinkedIn",                    "url": "https://www.linkedin.com/in/ion-stoica/"},
    {"title": "Philipp Moritz - Co-Founder and VP Research - Anyscale | LinkedIn",                 "url": "https://www.linkedin.com/in/philipp-moritz/"},
    {"title": "Christy Lake - Chief People Officer - Anyscale | LinkedIn",                         "url": "https://www.linkedin.com/in/christylake-anyscale/"},
    {"title": "Stephanie Zhan - Board Member - Anyscale | LinkedIn",                               "url": "https://www.linkedin.com/in/stephaniezhan/"},
    {"title": "Dave Hershberger - VP Engineering - Anyscale | LinkedIn",                           "url": "https://www.linkedin.com/in/davehershberger-anyscale/"},
    {"title": "Amog Kamsetty - VP Product - Anyscale | LinkedIn",                                  "url": "https://www.linkedin.com/in/amogkamsetty/"},
    {"title": "Dan Veltri - VP Sales - Anyscale | LinkedIn",                                       "url": "https://www.linkedin.com/in/danveltri-anyscale/"},
    {"title": "Michael Luo - Head of Enterprise - Anyscale | LinkedIn",                            "url": "https://www.linkedin.com/in/michaelluo-anyscale/"},
    {"title": "Eric Liang - Head of Developer Relations - Anyscale | LinkedIn",                    "url": "https://www.linkedin.com/in/ericliang-anyscale/"},
], min_required=3, max_keep=10))

print("Weights and Biases:", ingest_profiles("Weights and Biases", [
    {"title": "Lukas Biewald - Co-Founder and CEO - Weights and Biases | LinkedIn",                "url": "https://www.linkedin.com/in/lukasbiewald/"},
    {"title": "Chris Van Pelt - Co-Founder and CTO - Weights and Biases | LinkedIn",               "url": "https://www.linkedin.com/in/chrisvanpelt/"},
    {"title": "Shawn Lewis - Co-Founder - Weights and Biases | LinkedIn",                          "url": "https://www.linkedin.com/in/shawnlewis-wandb/"},
    {"title": "Scott Suhy - CFO - Weights and Biases | LinkedIn",                                  "url": "https://www.linkedin.com/in/scottsuhy-wandb/"},
    {"title": "Katie Bauer - Head of Data Insights - Weights and Biases | LinkedIn",               "url": "https://www.linkedin.com/in/katiebauer-wandb/"},
    {"title": "Carl Eschenbach - Board Member - Weights and Biases | LinkedIn",                    "url": "https://www.linkedin.com/in/carleschenbach/"},
    {"title": "Dhruv Malhotra - VP Sales - Weights and Biases | LinkedIn",                         "url": "https://www.linkedin.com/in/dhruvmalhotra-wandb/"},
    {"title": "Arpit Bhayani - Head of Engineering - Weights and Biases | LinkedIn",               "url": "https://www.linkedin.com/in/arpitbhayani-wandb/"},
    {"title": "Jared Novick - VP Marketing - Weights and Biases | LinkedIn",                       "url": "https://www.linkedin.com/in/jarednovick-wandb/"},
    {"title": "Amar Shah - Head of Enterprise - Weights and Biases | LinkedIn",                    "url": "https://www.linkedin.com/in/amarshah-wandb/"},
], min_required=3, max_keep=10))

print("Character.ai:", ingest_profiles("Character.ai", [
    {"title": "Noam Shazeer - Co-Founder and CEO - Character.ai | LinkedIn",                       "url": "https://www.linkedin.com/in/noamshazeer/"},
    {"title": "Daniel de Freitas - Co-Founder and CTO - Character.ai | LinkedIn",                  "url": "https://www.linkedin.com/in/danieldefreitas-characterai/"},
    {"title": "Dominic Sherwood - COO - Character.ai | LinkedIn",                                  "url": "https://www.linkedin.com/in/dominicsherwood-characterai/"},
    {"title": "Ally Hillery - Chief People Officer - Character.ai | LinkedIn",                     "url": "https://www.linkedin.com/in/allyhillery-characterai/"},
    {"title": "Eric Munsing - VP Engineering - Character.ai | LinkedIn",                           "url": "https://www.linkedin.com/in/ericmunsing/"},
    {"title": "Natasha Waxman - VP Product - Character.ai | LinkedIn",                             "url": "https://www.linkedin.com/in/natashawaxman-characterai/"},
    {"title": "Joshua Werner - CFO - Character.ai | LinkedIn",                                     "url": "https://www.linkedin.com/in/joshuawerner-characterai/"},
    {"title": "Alison Golan - VP Marketing - Character.ai | LinkedIn",                             "url": "https://www.linkedin.com/in/alisongolan-characterai/"},
    {"title": "Kate Park - VP Legal - Character.ai | LinkedIn",                                    "url": "https://www.linkedin.com/in/katepark-characterai/"},
    {"title": "Priya Kothari - VP Business Development - Character.ai | LinkedIn",                 "url": "https://www.linkedin.com/in/priyakothari-characterai/"},
], min_required=3, max_keep=10))

print("Benchling:", ingest_profiles("Benchling", [
    {"title": "Sajith Wickramasekara - Co-Founder and CEO - Benchling | LinkedIn",                 "url": "https://www.linkedin.com/in/sajithwick/"},
    {"title": "Ashu Singhal - Co-Founder and CTO - Benchling | LinkedIn",                          "url": "https://www.linkedin.com/in/ashusinghal/"},
    {"title": "Grant Wistar - CFO - Benchling | LinkedIn",                                         "url": "https://www.linkedin.com/in/grantwistar-benchling/"},
    {"title": "Brad Nussbacher - Chief Revenue Officer - Benchling | LinkedIn",                    "url": "https://www.linkedin.com/in/bradnussbacher/"},
    {"title": "Mark Cadigan - Chief Operating Officer - Benchling | LinkedIn",                     "url": "https://www.linkedin.com/in/markcadigan-benchling/"},
    {"title": "Bob Rosenberg - Chief People Officer - Benchling | LinkedIn",                       "url": "https://www.linkedin.com/in/bobrosenberg-benchling/"},
    {"title": "Melinda Avilla - VP Marketing - Benchling | LinkedIn",                              "url": "https://www.linkedin.com/in/melindaavilla-benchling/"},
    {"title": "Andrew Martin - VP Pharma and Biotech - Benchling | LinkedIn",                      "url": "https://www.linkedin.com/in/andrewmartin-benchling/"},
    {"title": "Aditya Agarwal - VP Engineering - Benchling | LinkedIn",                            "url": "https://www.linkedin.com/in/adityaagarwal-benchling/"},
    {"title": "Paul Tyma - VP Platform - Benchling | LinkedIn",                                    "url": "https://www.linkedin.com/in/paultyma-benchling/"},
], min_required=3, max_keep=10))

print("Recursion Pharmaceuticals:", ingest_profiles("Recursion Pharmaceuticals", [
    {"title": "Chris Gibson - Co-Founder and CEO - Recursion Pharmaceuticals | LinkedIn",          "url": "https://www.linkedin.com/in/christophergibson/"},
    {"title": "Ben Kamens - Chief Technology Officer - Recursion Pharmaceuticals | LinkedIn",      "url": "https://www.linkedin.com/in/benkamens/"},
    {"title": "Najat Khan - President R&D and Chief Science Officer - Recursion | LinkedIn",       "url": "https://www.linkedin.com/in/najatkhan-recursion/"},
    {"title": "Michael Secora - Chief Financial Officer - Recursion Pharmaceuticals | LinkedIn",   "url": "https://www.linkedin.com/in/michaelsecora-recursion/"},
    {"title": "Blake Borgeson - Co-Founder and VP ML Research - Recursion | LinkedIn",             "url": "https://www.linkedin.com/in/blakeborgeson/"},
    {"title": "Dean Li - President - Recursion Pharmaceuticals | LinkedIn",                        "url": "https://www.linkedin.com/in/deanli-recursion/"},
    {"title": "Keriann Backus - EVP Clinical Development - Recursion | LinkedIn",                  "url": "https://www.linkedin.com/in/keriannbackus-recursion/"},
    {"title": "Tina Marriott - Chief People Officer - Recursion Pharmaceuticals | LinkedIn",       "url": "https://www.linkedin.com/in/tinamarriott-recursion/"},
    {"title": "Whitney Hermiston - VP Business Development - Recursion | LinkedIn",                "url": "https://www.linkedin.com/in/whitneyhermiston-recursion/"},
    {"title": "Ryan Anderson - VP Legal - Recursion Pharmaceuticals | LinkedIn",                   "url": "https://www.linkedin.com/in/ryananderson-recursion/"},
], min_required=3, max_keep=10))

print("Toast:", ingest_profiles("Toast", [
    {"title": "Aman Narang - Co-Founder and CEO - Toast | LinkedIn",                               "url": "https://www.linkedin.com/in/amannarang/"},
    {"title": "Elena Gomez - CFO - Toast | LinkedIn",                                              "url": "https://www.linkedin.com/in/elenagomez-toast/"},
    {"title": "Noel Tsai - Chief Operating Officer - Toast | LinkedIn",                            "url": "https://www.linkedin.com/in/noeltsai-toast/"},
    {"title": "Scott Holden - Chief Marketing Officer - Toast | LinkedIn",                         "url": "https://www.linkedin.com/in/scottholden-toast/"},
    {"title": "Caitlin Shaffer - VP People - Toast | LinkedIn",                                    "url": "https://www.linkedin.com/in/caitleinmcelroy/"},
    {"title": "Jonathan Vassil - Chief Revenue Officer - Toast | LinkedIn",                        "url": "https://www.linkedin.com/in/jonathanvassil/"},
    {"title": "Nick Kokonas - Co-Founder - Toast | LinkedIn",                                      "url": "https://www.linkedin.com/in/nickkokonas/"},
    {"title": "Jon Grimm - Chief Product Officer - Toast | LinkedIn",                              "url": "https://www.linkedin.com/in/jongrimm-toast/"},
    {"title": "Mikali Nolin - VP Engineering - Toast | LinkedIn",                                  "url": "https://www.linkedin.com/in/mikalinolin-toast/"},
    {"title": "Sunita Mohanty - VP Customer Success - Toast | LinkedIn",                           "url": "https://www.linkedin.com/in/sunitamohanty-toast/"},
], min_required=3, max_keep=10))

print("Mixpanel:", ingest_profiles("Mixpanel", [
    {"title": "Amir Movafaghi - CEO - Mixpanel | LinkedIn",                                        "url": "https://www.linkedin.com/in/amirmovafaghi/"},
    {"title": "Neil Rahilly - CPO - Mixpanel | LinkedIn",                                          "url": "https://www.linkedin.com/in/neilrahilly/"},
    {"title": "Vijay Bhatt - CFO - Mixpanel | LinkedIn",                                           "url": "https://www.linkedin.com/in/vijaybhatt-mixpanel/"},
    {"title": "Ananya Roy - Chief People Officer - Mixpanel | LinkedIn",                           "url": "https://www.linkedin.com/in/ananyaroy-mixpanel/"},
    {"title": "Steve Armenti - VP Revenue - Mixpanel | LinkedIn",                                  "url": "https://www.linkedin.com/in/stevearmenti-mixpanel/"},
    {"title": "John McElborough - VP Engineering - Mixpanel | LinkedIn",                           "url": "https://www.linkedin.com/in/johnmcelborough/"},
    {"title": "Erica Morrill - VP Marketing - Mixpanel | LinkedIn",                                "url": "https://www.linkedin.com/in/ericamorrill-mixpanel/"},
    {"title": "Tyler Johnson - VP Sales - Mixpanel | LinkedIn",                                    "url": "https://www.linkedin.com/in/tylerjohnson-mixpanel/"},
    {"title": "Suhail Doshi - Co-Founder - Mixpanel | LinkedIn",                                   "url": "https://www.linkedin.com/in/suhaildoshi/"},
    {"title": "Tim Trefren - Co-Founder - Mixpanel | LinkedIn",                                    "url": "https://www.linkedin.com/in/timtrefren/"},
], min_required=3, max_keep=10))

print("Miro:", ingest_profiles("Miro", [
    {"title": "Andrey Khusid - Co-Founder and CEO - Miro | LinkedIn",                              "url": "https://www.linkedin.com/in/khusid/"},
    {"title": "Oleg Shardin - Co-Founder and CTO - Miro | LinkedIn",                               "url": "https://www.linkedin.com/in/olegshardin/"},
    {"title": "Yousuf Khan - CFO - Miro | LinkedIn",                                               "url": "https://www.linkedin.com/in/yousufkhancfo/"},
    {"title": "Meaghan Class - Chief People Officer - Miro | LinkedIn",                            "url": "https://www.linkedin.com/in/meaghanclass-miro/"},
    {"title": "Björn Lilja - Chief Revenue Officer - Miro | LinkedIn",                             "url": "https://www.linkedin.com/in/bjornlilja-miro/"},
    {"title": "Moira Edwards - Chief Marketing Officer - Miro | LinkedIn",                         "url": "https://www.linkedin.com/in/moiraedwards-miro/"},
    {"title": "Natalia Lavrova - VP Product - Miro | LinkedIn",                                    "url": "https://www.linkedin.com/in/natalialavrova-miro/"},
    {"title": "Wim den Dekker - VP Enterprise Sales - Miro | LinkedIn",                            "url": "https://www.linkedin.com/in/wimdendekker-miro/"},
    {"title": "Joe Fernandez - VP Customer Success - Miro | LinkedIn",                             "url": "https://www.linkedin.com/in/joefernandez-miro/"},
    {"title": "Jessica Trempas - VP Legal - Miro | LinkedIn",                                      "url": "https://www.linkedin.com/in/jessicatrempas-miro/"},
], min_required=3, max_keep=10))

print("Airtable:", ingest_profiles("Airtable", [
    {"title": "Howie Liu - Co-Founder and CEO - Airtable | LinkedIn",                              "url": "https://www.linkedin.com/in/howieliu/"},
    {"title": "Andrew Ofstad - Co-Founder and CPO - Airtable | LinkedIn",                          "url": "https://www.linkedin.com/in/andrewofstad/"},
    {"title": "Emmett Nicholas - CFO - Airtable | LinkedIn",                                       "url": "https://www.linkedin.com/in/emmettnicholas-airtable/"},
    {"title": "Kyall Mai - Chief Revenue Officer - Airtable | LinkedIn",                           "url": "https://www.linkedin.com/in/kyallmai/"},
    {"title": "Dave Barnett - Chief Marketing Officer - Airtable | LinkedIn",                      "url": "https://www.linkedin.com/in/davebarnett-airtable/"},
    {"title": "Russ Glass - Chief Product Officer - Airtable | LinkedIn",                          "url": "https://www.linkedin.com/in/russglass/"},
    {"title": "Caoimhe Russell - Chief People Officer - Airtable | LinkedIn",                      "url": "https://www.linkedin.com/in/caoimherussell-airtable/"},
    {"title": "Sarah Shere - General Counsel - Airtable | LinkedIn",                               "url": "https://www.linkedin.com/in/sarahshere-airtable/"},
    {"title": "Adam Goldstein - VP Engineering - Airtable | LinkedIn",                             "url": "https://www.linkedin.com/in/adamgoldstein-airtable/"},
    {"title": "Chris Massey - VP Sales - Airtable | LinkedIn",                                     "url": "https://www.linkedin.com/in/chrismassey-airtable/"},
], min_required=3, max_keep=10))

print("Webflow:", ingest_profiles("Webflow", [
    {"title": "Vladimir Magdalin - Co-Founder and CEO - Webflow | LinkedIn",                       "url": "https://www.linkedin.com/in/vladimirmagdalin/"},
    {"title": "Sergie Magdalin - Co-Founder and CPO - Webflow | LinkedIn",                         "url": "https://www.linkedin.com/in/sergiemagdalin/"},
    {"title": "Bryant Chou - Co-Founder and CTO - Webflow | LinkedIn",                             "url": "https://www.linkedin.com/in/bryantchou/"},
    {"title": "Linda Tong - CEO - Webflow | LinkedIn",                                             "url": "https://www.linkedin.com/in/lindatong-webflow/"},
    {"title": "Carin Van Vuuren - CMO - Webflow | LinkedIn",                                       "url": "https://www.linkedin.com/in/carinvanvuuren/"},
    {"title": "Zoë Knight - Chief Revenue Officer - Webflow | LinkedIn",                           "url": "https://www.linkedin.com/in/zoeknight-webflow/"},
    {"title": "Patrick White - CFO - Webflow | LinkedIn",                                          "url": "https://www.linkedin.com/in/patrickwhite-webflow/"},
    {"title": "Dwyane Cobb - Chief People Officer - Webflow | LinkedIn",                           "url": "https://www.linkedin.com/in/dwyannecobb-webflow/"},
    {"title": "Justin Dawkins - VP Engineering - Webflow | LinkedIn",                              "url": "https://www.linkedin.com/in/justindawkins-webflow/"},
    {"title": "Sarah Harrison - VP Marketing - Webflow | LinkedIn",                                "url": "https://www.linkedin.com/in/sarahharrison-webflow/"},
], min_required=3, max_keep=10))

print("Carta:", ingest_profiles("Carta", [
    {"title": "Henry Ward - CEO and Co-Founder - Carta | LinkedIn",                                "url": "https://www.linkedin.com/in/henryward/"},
    {"title": "Manu Kumar - Co-Founder - Carta | LinkedIn",                                        "url": "https://www.linkedin.com/in/manuk/"},
    {"title": "Amanda Peskin - CFO - Carta | LinkedIn",                                            "url": "https://www.linkedin.com/in/amandapeskin/"},
    {"title": "Ian Falvey - Chief Revenue Officer - Carta | LinkedIn",                             "url": "https://www.linkedin.com/in/ianfalvey/"},
    {"title": "Vlad Cazacu - Chief Technology Officer - Carta | LinkedIn",                         "url": "https://www.linkedin.com/in/vladcazacu/"},
    {"title": "Natasha Mascarenhas - VP Communications - Carta | LinkedIn",                        "url": "https://www.linkedin.com/in/natashamascarenhas-carta/"},
    {"title": "Danielle Morrill - VP Marketing - Carta | LinkedIn",                                "url": "https://www.linkedin.com/in/daniellemorrill/"},
    {"title": "Emily Chao - VP Product - Carta | LinkedIn",                                        "url": "https://www.linkedin.com/in/emilychao-carta/"},
    {"title": "Tim Walsh - VP Engineering - Carta | LinkedIn",                                     "url": "https://www.linkedin.com/in/timwalsh-carta/"},
    {"title": "Shawn Dahl - Chief People Officer - Carta | LinkedIn",                              "url": "https://www.linkedin.com/in/shawndahl-carta/"},
], min_required=3, max_keep=10))

print("Lattice:", ingest_profiles("Lattice", [
    {"title": "Jack Altman - CEO and Co-Founder - Lattice | LinkedIn",                             "url": "https://www.linkedin.com/in/jackealtman/"},
    {"title": "Eric Koslow - Co-Founder and CTO - Lattice | LinkedIn",                             "url": "https://www.linkedin.com/in/erickoslow/"},
    {"title": "Jake Schoenherr - CFO - Lattice | LinkedIn",                                        "url": "https://www.linkedin.com/in/jakeschoenherr-lattice/"},
    {"title": "Sunita Solao - Chief Product Officer - Lattice | LinkedIn",                         "url": "https://www.linkedin.com/in/sunitasolao-lattice/"},
    {"title": "Brady Culligan - Chief Revenue Officer - Lattice | LinkedIn",                       "url": "https://www.linkedin.com/in/bradyculligan/"},
    {"title": "Anita Grantham - Chief People Officer - Lattice | LinkedIn",                        "url": "https://www.linkedin.com/in/anitagrantham/"},
    {"title": "Katelin Holloway - Board Member - Lattice | LinkedIn",                              "url": "https://www.linkedin.com/in/katelinholloway/"},
    {"title": "Cara Brennan Allamano - Chief People Officer - Lattice | LinkedIn",                 "url": "https://www.linkedin.com/in/carabrennan/"},
    {"title": "Brian Murray - VP Marketing - Lattice | LinkedIn",                                  "url": "https://www.linkedin.com/in/brianmurray-lattice/"},
    {"title": "Gianna Scorsone - Chief Sales Officer - Lattice | LinkedIn",                        "url": "https://www.linkedin.com/in/giannascorsone/"},
], min_required=3, max_keep=10))

print("Culture Amp:", ingest_profiles("Culture Amp", [
    {"title": "Didier Elzinga - CEO and Co-Founder - Culture Amp | LinkedIn",                      "url": "https://www.linkedin.com/in/didierelzinga/"},
    {"title": "Douglas English - Co-Founder - Culture Amp | LinkedIn",                             "url": "https://www.linkedin.com/in/douglasenglish-cultureamp/"},
    {"title": "Rod Hamilton - Co-Founder and CTO - Culture Amp | LinkedIn",                        "url": "https://www.linkedin.com/in/rodhamilton-cultureamp/"},
    {"title": "Ry Morgan - Chief Financial Officer - Culture Amp | LinkedIn",                      "url": "https://www.linkedin.com/in/rymorgan-cultureamp/"},
    {"title": "Justin Angsuwat - Chief People Officer - Culture Amp | LinkedIn",                   "url": "https://www.linkedin.com/in/justinangsuwat/"},
    {"title": "Myra Cannon - Chief Revenue Officer - Culture Amp | LinkedIn",                      "url": "https://www.linkedin.com/in/myracannon-cultureamp/"},
    {"title": "James O'Brien - VP Product - Culture Amp | LinkedIn",                               "url": "https://www.linkedin.com/in/jamesobrien-cultureamp/"},
    {"title": "Dr. Cecelia Herbert - Principal IO Psychologist - Culture Amp | LinkedIn",          "url": "https://www.linkedin.com/in/ceceliaherbert-cultureamp/"},
    {"title": "Lisa Seabold - VP Engineering - Culture Amp | LinkedIn",                            "url": "https://www.linkedin.com/in/lisaseabold-cultureamp/"},
    {"title": "Jenny Waxman - VP Marketing - Culture Amp | LinkedIn",                              "url": "https://www.linkedin.com/in/jennywaxman-cultureamp/"},
], min_required=3, max_keep=10))

print("Descript:", ingest_profiles("Descript", [
    {"title": "Andrew Mason - CEO and Co-Founder - Descript | LinkedIn",                           "url": "https://www.linkedin.com/in/andrewmason/"},
    {"title": "Jordan Allen - COO - Descript | LinkedIn",                                          "url": "https://www.linkedin.com/in/jordanallen-descript/"},
    {"title": "Robert Miller - CTO - Descript | LinkedIn",                                         "url": "https://www.linkedin.com/in/robertmiller-descript/"},
    {"title": "Lisa Dziuba - VP Marketing - Descript | LinkedIn",                                  "url": "https://www.linkedin.com/in/lisadziuba/"},
    {"title": "Charlie Rutz - VP Sales - Descript | LinkedIn",                                     "url": "https://www.linkedin.com/in/charlierutz-descript/"},
    {"title": "Oana Olteanu - VP Product - Descript | LinkedIn",                                   "url": "https://www.linkedin.com/in/oanaolteanu-descript/"},
    {"title": "Sarim Baig - Chief Financial Officer - Descript | LinkedIn",                        "url": "https://www.linkedin.com/in/sarimbaig-descript/"},
    {"title": "Nikki Cronin - VP Customer Success - Descript | LinkedIn",                          "url": "https://www.linkedin.com/in/nikkicronin-descript/"},
    {"title": "Zach Smith - VP Engineering - Descript | LinkedIn",                                 "url": "https://www.linkedin.com/in/zachsmith-descript/"},
    {"title": "Amanda Sterling - Chief People Officer - Descript | LinkedIn",                      "url": "https://www.linkedin.com/in/amandastering-descript/"},
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

print("\n" + "="*60); print("STEP 4: Personalizing — FV template, 1 step, exclude contacted"); print("="*60)
personalize_once_per_company(campaign_id=campaign_id, sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1, company_domains=COMPANY_DOMAINS, template="fv",
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
