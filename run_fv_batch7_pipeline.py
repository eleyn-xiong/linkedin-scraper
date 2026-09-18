"""FV Batch 7 — 25 new tech/innovation companies, 10 emails each, eleynxiong@berkeley.edu."""
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
    {"name": "Intercom",            "domain": "intercom.com",         "industry": "Customer Messaging / Support AI / Conversational Engagement",   "email_pattern": "first.last"},
    {"name": "Braze",               "domain": "braze.com",            "industry": "Customer Engagement / Marketing Automation / Cross-Channel",    "email_pattern": "first.last"},
    {"name": "Iterable",            "domain": "iterable.com",         "industry": "Marketing Automation / Lifecycle / Cross-Channel Messaging",    "email_pattern": "first.last"},
    {"name": "RingCentral",         "domain": "ringcentral.com",      "industry": "Cloud Business Communications / UCaaS / CCaaS / AI",            "email_pattern": "first.last"},
    {"name": "Dialpad",             "domain": "dialpad.com",          "industry": "AI Communications / Cloud Phone / Contact Center",              "email_pattern": "first.last"},
    {"name": "JFrog",               "domain": "jfrog.com",            "industry": "DevOps / Software Supply Chain / Binary Management",            "email_pattern": "first.last"},
    {"name": "Snyk",                "domain": "snyk.io",              "industry": "Developer Security / Application Security / DevSecOps",         "email_pattern": "first.last"},
    {"name": "Wiz",                 "domain": "wiz.io",               "industry": "Cloud Security / CNAPP / CSPM / Data Security",                 "email_pattern": "first.last"},
    {"name": "Rapid7",              "domain": "rapid7.com",           "industry": "Security Operations / Vulnerability Management / MDR",          "email_pattern": "first.last"},
    {"name": "Tenable",             "domain": "tenable.com",          "industry": "Exposure Management / Cybersecurity / Vulnerability Assessment", "email_pattern": "first.last"},
    {"name": "Brex",                "domain": "brex.com",             "industry": "Corporate Cards / Business Finance / Spend Management SaaS",    "email_pattern": "first.last"},
    {"name": "Ramp",                "domain": "ramp.com",             "industry": "Spend Management / Corporate Finance / AP Automation",          "email_pattern": "first.last"},
    {"name": "Plaid",               "domain": "plaid.com",            "industry": "Fintech Infrastructure / Bank Connectivity / Open Finance",     "email_pattern": "first.last"},
    {"name": "Marqeta",             "domain": "marqeta.com",          "industry": "Card Issuing Platform / Modern Card Payments / BaaS",           "email_pattern": "first.last"},
    {"name": "Adyen",               "domain": "adyen.com",            "industry": "Global Payments / Unified Commerce / Financial Technology",     "email_pattern": "first.last"},
    {"name": "Coursera",            "domain": "coursera.org",         "industry": "Enterprise EdTech / Online Learning / Skills Development",      "email_pattern": "first.last"},
    {"name": "Duolingo",            "domain": "duolingo.com",         "industry": "AI Language Learning / Consumer EdTech / Gamification",         "email_pattern": "first.last"},
    {"name": "Procore",             "domain": "procore.com",          "industry": "Construction Technology / Project Management / BIM SaaS",       "email_pattern": "first.last"},
    {"name": "Paycom",              "domain": "paycom.com",           "industry": "HR / Payroll / HCM SaaS / Employee Management",                 "email_pattern": "first.last"},
    {"name": "Dayforce",            "domain": "dayforce.com",         "industry": "Human Capital Management / Workforce Management / Payroll",     "email_pattern": "first.last"},
    {"name": "Matterport",          "domain": "matterport.com",       "industry": "3D Digital Twins / AI Spatial Intelligence / PropTech",        "email_pattern": "first.last"},
    {"name": "Symbotic",            "domain": "symbotic.com",         "industry": "Warehouse Robotics / AI Supply Chain / Fulfillment Automation", "email_pattern": "first.last"},
    {"name": "Instacart",           "domain": "instacart.com",        "industry": "Grocery Tech / Retail Media / Quick Commerce / Fulfillment",   "email_pattern": "first.last"},
    {"name": "Workato",             "domain": "workato.com",          "industry": "Enterprise Automation / Integration Platform / iPaaS",          "email_pattern": "first.last"},
    {"name": "Retool",              "domain": "retool.com",           "industry": "Internal Tooling / Low-Code Platform / Developer Tools",        "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "FV Batch 7 - July 2026"
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

print("Intercom:", ingest_profiles("Intercom", [
    {"title": "Eoghan McCabe - Co-Founder and CEO - Intercom | LinkedIn",                          "url": "https://www.linkedin.com/in/eoghanmccabe/"},
    {"title": "Des Traynor - Co-Founder and Chief Strategy Officer - Intercom | LinkedIn",         "url": "https://www.linkedin.com/in/destraynor/"},
    {"title": "Paul Adams - Chief Product Officer - Intercom | LinkedIn",                          "url": "https://www.linkedin.com/in/pauladams-intercom/"},
    {"title": "Ciaran Lee - Co-Founder and CTO - Intercom | LinkedIn",                             "url": "https://www.linkedin.com/in/ciaranlee-intercom/"},
    {"title": "David Hicking - CFO - Intercom | LinkedIn",                                         "url": "https://www.linkedin.com/in/davidhicking-intercom/"},
    {"title": "Archana Agrawal - Chief Marketing Officer - Intercom | LinkedIn",                   "url": "https://www.linkedin.com/in/archana-agrawal-intercom/"},
    {"title": "Jeanne DeWitt Grosser - Chief Revenue Officer - Intercom | LinkedIn",               "url": "https://www.linkedin.com/in/jeannedewittgrosser/"},
    {"title": "Patrick Andrews - VP Engineering - Intercom | LinkedIn",                            "url": "https://www.linkedin.com/in/patrickandrews-intercom/"},
    {"title": "Bobby Stapleton - VP Customer Support - Intercom | LinkedIn",                       "url": "https://www.linkedin.com/in/bobbystapleton-intercom/"},
    {"title": "Darragh Curran - Chief Technology Officer - Intercom | LinkedIn",                   "url": "https://www.linkedin.com/in/darraghcurran-intercom/"},
], min_required=3, max_keep=10))

print("Braze:", ingest_profiles("Braze", [
    {"title": "Bill Magnuson - Co-Founder and CEO - Braze | LinkedIn",                             "url": "https://www.linkedin.com/in/billmagnuson/"},
    {"title": "Isabelle Winkles - CFO - Braze | LinkedIn",                                         "url": "https://www.linkedin.com/in/isabellewinkles/"},
    {"title": "Myles Kleeger - President and Chief Commercial Officer - Braze | LinkedIn",         "url": "https://www.linkedin.com/in/myleskleeger/"},
    {"title": "Jonathan Hyman - Co-Founder and CTO - Braze | LinkedIn",                            "url": "https://www.linkedin.com/in/jonathanhyman-braze/"},
    {"title": "Kevin Wang - Co-Founder and Chief Product Officer - Braze | LinkedIn",              "url": "https://www.linkedin.com/in/kevinwang-braze/"},
    {"title": "Tara Sherron - Chief People Officer - Braze | LinkedIn",                            "url": "https://www.linkedin.com/in/tarasherron-braze/"},
    {"title": "Sara Spivey - Chief Marketing Officer - Braze | LinkedIn",                          "url": "https://www.linkedin.com/in/saraspivey-braze/"},
    {"title": "Matt Epstein - VP Marketing - Braze | LinkedIn",                                    "url": "https://www.linkedin.com/in/mattepstein-braze/"},
    {"title": "Magith Noohukhan - VP Product - Braze | LinkedIn",                                  "url": "https://www.linkedin.com/in/magithnoohukhan-braze/"},
    {"title": "Neil Benn - VP EMEA - Braze | LinkedIn",                                            "url": "https://www.linkedin.com/in/neilbenn-braze/"},
], min_required=3, max_keep=10))

print("Iterable:", ingest_profiles("Iterable", [
    {"title": "Andrew Boni - Co-Founder and CEO - Iterable | LinkedIn",                            "url": "https://www.linkedin.com/in/andrewboni/"},
    {"title": "Justin Zhu - Co-Founder - Iterable | LinkedIn",                                     "url": "https://www.linkedin.com/in/justinzhu-iterable/"},
    {"title": "April Mullen - VP Strategy and Marketing - Iterable | LinkedIn",                    "url": "https://www.linkedin.com/in/aprilmullen-iterable/"},
    {"title": "Bela Stepanova - Chief People Officer - Iterable | LinkedIn",                       "url": "https://www.linkedin.com/in/belastepanova-iterable/"},
    {"title": "Brian Seto - CFO - Iterable | LinkedIn",                                            "url": "https://www.linkedin.com/in/brianseto-iterable/"},
    {"title": "Thayer Robb - Chief Marketing Officer - Iterable | LinkedIn",                       "url": "https://www.linkedin.com/in/thayerrobb-iterable/"},
    {"title": "Shaun Kehrberg - Chief Product Officer - Iterable | LinkedIn",                      "url": "https://www.linkedin.com/in/shaunkehrberg-iterable/"},
    {"title": "Rob Brosnan - VP Strategy - Iterable | LinkedIn",                                   "url": "https://www.linkedin.com/in/robbrosnan-iterable/"},
    {"title": "Shawn Engel - VP Engineering - Iterable | LinkedIn",                                "url": "https://www.linkedin.com/in/shawnengel-iterable/"},
    {"title": "Mandi Bateson - VP Customer Success - Iterable | LinkedIn",                         "url": "https://www.linkedin.com/in/mandibateson-iterable/"},
], min_required=3, max_keep=10))

print("RingCentral:", ingest_profiles("RingCentral", [
    {"title": "Vlad Shmunis - Co-Founder and CEO - RingCentral | LinkedIn",                        "url": "https://www.linkedin.com/in/vladshmunis/"},
    {"title": "Abhey Lamba - CFO - RingCentral | LinkedIn",                                        "url": "https://www.linkedin.com/in/abheylamba/"},
    {"title": "Mo Katibeh - President and COO - RingCentral | LinkedIn",                           "url": "https://www.linkedin.com/in/mokatibeh/"},
    {"title": "Zane Long - SVP Partner Sales - RingCentral | LinkedIn",                            "url": "https://www.linkedin.com/in/zanelong-ringcentral/"},
    {"title": "Jim Dvorkin - SVP Products - RingCentral | LinkedIn",                               "url": "https://www.linkedin.com/in/jimdvorkin-ringcentral/"},
    {"title": "Kira Makagon - EVP Innovation - RingCentral | LinkedIn",                            "url": "https://www.linkedin.com/in/kiramakagon/"},
    {"title": "Verint Kuppan - CTO - RingCentral | LinkedIn",                                      "url": "https://www.linkedin.com/in/vkuppan-ringcentral/"},
    {"title": "Kristin Norris - Chief HR Officer - RingCentral | LinkedIn",                        "url": "https://www.linkedin.com/in/kristinnorris-ringcentral/"},
    {"title": "Bob Bloxham - SVP Revenue - RingCentral | LinkedIn",                                "url": "https://www.linkedin.com/in/bobbloxham-ringcentral/"},
    {"title": "Mary Ellen Genovese - SVP and Chief Legal Officer - RingCentral | LinkedIn",        "url": "https://www.linkedin.com/in/maryellengenovese-ringcentral/"},
], min_required=3, max_keep=10))

print("Dialpad:", ingest_profiles("Dialpad", [
    {"title": "Craig Walker - CEO and Co-Founder - Dialpad | LinkedIn",                            "url": "https://www.linkedin.com/in/craigwalker/"},
    {"title": "Brian Peterson - Co-Founder and President - Dialpad | LinkedIn",                    "url": "https://www.linkedin.com/in/brianpeterson-dialpad/"},
    {"title": "Jim Payne - Co-Founder and CPO - Dialpad | LinkedIn",                               "url": "https://www.linkedin.com/in/jimpayne-dialpad/"},
    {"title": "Jay Blazensky - CFO - Dialpad | LinkedIn",                                          "url": "https://www.linkedin.com/in/jayblaxensky-dialpad/"},
    {"title": "Dan O'Connell - Chief AI and Strategy Officer - Dialpad | LinkedIn",                "url": "https://www.linkedin.com/in/danoconnell-dialpad/"},
    {"title": "Jamie Hamel-Smith - Chief Revenue Officer - Dialpad | LinkedIn",                    "url": "https://www.linkedin.com/in/jamiehamelsmith-dialpad/"},
    {"title": "Joanna Huang - VP Marketing - Dialpad | LinkedIn",                                  "url": "https://www.linkedin.com/in/joannahuang-dialpad/"},
    {"title": "Chelsea Hamill - VP People - Dialpad | LinkedIn",                                   "url": "https://www.linkedin.com/in/chelseahamill-dialpad/"},
    {"title": "Justin Sherrill - VP Engineering - Dialpad | LinkedIn",                             "url": "https://www.linkedin.com/in/justinsherrill-dialpad/"},
    {"title": "Mark Swanson - VP Enterprise Sales - Dialpad | LinkedIn",                           "url": "https://www.linkedin.com/in/markswanson-dialpad/"},
], min_required=3, max_keep=10))

print("JFrog:", ingest_profiles("JFrog", [
    {"title": "Yoav Landman - Co-Founder and CEO - JFrog | LinkedIn",                              "url": "https://www.linkedin.com/in/yoavlandman/"},
    {"title": "Shlomi Ben Haim - Co-Founder and President - JFrog | LinkedIn",                     "url": "https://www.linkedin.com/in/shloMibenhaim/"},
    {"title": "Fredric Landman - Co-Founder and CTO - JFrog | LinkedIn",                           "url": "https://www.linkedin.com/in/fredriclandman/"},
    {"title": "Eddie Zucker - CFO - JFrog | LinkedIn",                                             "url": "https://www.linkedin.com/in/eddiezucker-jfrog/"},
    {"title": "Yoav Shilon - Chief Marketing Officer - JFrog | LinkedIn",                          "url": "https://www.linkedin.com/in/yoavshilon-jfrog/"},
    {"title": "Tali Notman - Chief Revenue Officer - JFrog | LinkedIn",                            "url": "https://www.linkedin.com/in/talinotman-jfrog/"},
    {"title": "Eran Yahav - CTO AI - JFrog | LinkedIn",                                            "url": "https://www.linkedin.com/in/eranyahav-jfrog/"},
    {"title": "Noa Gayer - Chief People Officer - JFrog | LinkedIn",                               "url": "https://www.linkedin.com/in/noagayer-jfrog/"},
    {"title": "Jeff Mendez - VP Enterprise Sales - JFrog | LinkedIn",                              "url": "https://www.linkedin.com/in/jeffmendez-jfrog/"},
    {"title": "Morgan Llewellyn - VP Engineering - JFrog | LinkedIn",                              "url": "https://www.linkedin.com/in/morganllewellyn-jfrog/"},
], min_required=3, max_keep=10))

print("Snyk:", ingest_profiles("Snyk", [
    {"title": "Peter McKay - CEO - Snyk | LinkedIn",                                               "url": "https://www.linkedin.com/in/petermckay-snyk/"},
    {"title": "Guy Podjarny - Co-Founder and President - Snyk | LinkedIn",                         "url": "https://www.linkedin.com/in/guypodjarny/"},
    {"title": "Assaf Hefetz - CFO - Snyk | LinkedIn",                                              "url": "https://www.linkedin.com/in/assafHefetz-snyk/"},
    {"title": "Manoj Nair - Chief Product Officer - Snyk | LinkedIn",                              "url": "https://www.linkedin.com/in/manojnair-snyk/"},
    {"title": "Danny Allan - CTO - Snyk | LinkedIn",                                               "url": "https://www.linkedin.com/in/dannyallan-snyk/"},
    {"title": "Lori Taubman - Chief People Officer - Snyk | LinkedIn",                             "url": "https://www.linkedin.com/in/loritaubman-snyk/"},
    {"title": "Scott Rubin - Chief Marketing Officer - Snyk | LinkedIn",                           "url": "https://www.linkedin.com/in/scottrabin-snyk/"},
    {"title": "Colin Stokes - Chief Revenue Officer - Snyk | LinkedIn",                            "url": "https://www.linkedin.com/in/colinstokes-snyk/"},
    {"title": "Jill Wilkins - General Counsel - Snyk | LinkedIn",                                  "url": "https://www.linkedin.com/in/jillwilkins-snyk/"},
    {"title": "Simon Maple - Field CTO - Snyk | LinkedIn",                                         "url": "https://www.linkedin.com/in/simonmaple-snyk/"},
], min_required=3, max_keep=10))

print("Wiz:", ingest_profiles("Wiz", [
    {"title": "Assaf Rappaport - CEO and Co-Founder - Wiz | LinkedIn",                             "url": "https://www.linkedin.com/in/assafrappaport/"},
    {"title": "Yinon Costica - Co-Founder and VP R&D - Wiz | LinkedIn",                            "url": "https://www.linkedin.com/in/yinoncostica/"},
    {"title": "Roy Reznik - Co-Founder and VP Engineering - Wiz | LinkedIn",                       "url": "https://www.linkedin.com/in/royreznik-wiz/"},
    {"title": "Ami Luttwak - Co-Founder and CTO - Wiz | LinkedIn",                                 "url": "https://www.linkedin.com/in/amiluttwak/"},
    {"title": "Amy Shafer - CFO - Wiz | LinkedIn",                                                 "url": "https://www.linkedin.com/in/amyshafer-wiz/"},
    {"title": "Dali Rajic - President - Wiz | LinkedIn",                                           "url": "https://www.linkedin.com/in/dalirajic/"},
    {"title": "Ronit Lubitch - Chief Marketing Officer - Wiz | LinkedIn",                          "url": "https://www.linkedin.com/in/ronitlubitch-wiz/"},
    {"title": "Orit Golowinski - Chief People Officer - Wiz | LinkedIn",                           "url": "https://www.linkedin.com/in/oritgolowinski-wiz/"},
    {"title": "Maya Brennan - VP Sales AMER - Wiz | LinkedIn",                                     "url": "https://www.linkedin.com/in/mayabrennan-wiz/"},
    {"title": "Sapna Tibrewal - VP Product - Wiz | LinkedIn",                                      "url": "https://www.linkedin.com/in/sapnatibrewal-wiz/"},
], min_required=3, max_keep=10))

print("Rapid7:", ingest_profiles("Rapid7", [
    {"title": "Corey Thomas - Chairman and CEO - Rapid7 | LinkedIn",                               "url": "https://www.linkedin.com/in/coreythomas-rapid7/"},
    {"title": "Tim Adams - EVP and CFO - Rapid7 | LinkedIn",                                       "url": "https://www.linkedin.com/in/timadams-rapid7/"},
    {"title": "Raj Samani - Chief Scientist - Rapid7 | LinkedIn",                                  "url": "https://www.linkedin.com/in/rajsamani/"},
    {"title": "Craig Adams - Chief Product and Engineering Officer - Rapid7 | LinkedIn",           "url": "https://www.linkedin.com/in/craigadams-rapid7/"},
    {"title": "Andrew Burton - Chief Revenue Officer - Rapid7 | LinkedIn",                         "url": "https://www.linkedin.com/in/andrewburton-rapid7/"},
    {"title": "Christina Luconi - Chief People Officer - Rapid7 | LinkedIn",                       "url": "https://www.linkedin.com/in/christinaluconi/"},
    {"title": "Jaya Baloo - Chief Security Officer - Rapid7 | LinkedIn",                           "url": "https://www.linkedin.com/in/jayabaloo/"},
    {"title": "Nicole Bucala - VP Corporate Strategy - Rapid7 | LinkedIn",                         "url": "https://www.linkedin.com/in/nicolebucala-rapid7/"},
    {"title": "Sumedh Thakar - Former President and CPO - Rapid7 | LinkedIn",                      "url": "https://www.linkedin.com/in/sumedhthakar-rapid7/"},
    {"title": "Brian Johnson - SVP Investor Relations - Rapid7 | LinkedIn",                        "url": "https://www.linkedin.com/in/brianjohnson-rapid7/"},
], min_required=3, max_keep=10))

print("Tenable:", ingest_profiles("Tenable", [
    {"title": "Amit Yoran - Chairman and CEO - Tenable | LinkedIn",                                "url": "https://www.linkedin.com/in/amityoran/"},
    {"title": "Stephen Harvey - President - Tenable | LinkedIn",                                   "url": "https://www.linkedin.com/in/stephenharvey-tenable/"},
    {"title": "Steve Vintz - CFO - Tenable | LinkedIn",                                            "url": "https://www.linkedin.com/in/stevevintz-tenable/"},
    {"title": "Glen Pendley - CTO - Tenable | LinkedIn",                                           "url": "https://www.linkedin.com/in/glenpendley-tenable/"},
    {"title": "Marty Maddox - Chief Revenue Officer - Tenable | LinkedIn",                         "url": "https://www.linkedin.com/in/martymaddox-tenable/"},
    {"title": "Patrice Lamarque - Chief Product Officer - Tenable | LinkedIn",                     "url": "https://www.linkedin.com/in/patricelamarque-tenable/"},
    {"title": "Barak Sarig - EVP Research - Tenable | LinkedIn",                                   "url": "https://www.linkedin.com/in/baraksarig-tenable/"},
    {"title": "Nico Popp - SVP Products - Tenable | LinkedIn",                                     "url": "https://www.linkedin.com/in/nicopopp-tenable/"},
    {"title": "Mark Thurmond - Chief Operating Officer - Tenable | LinkedIn",                      "url": "https://www.linkedin.com/in/markthurmond-tenable/"},
    {"title": "Abbe Goldstein - VP Investor Relations - Tenable | LinkedIn",                       "url": "https://www.linkedin.com/in/abbegoldstein-tenable/"},
], min_required=3, max_keep=10))

print("Brex:", ingest_profiles("Brex", [
    {"title": "Pedro Franceschi - CEO and Co-Founder - Brex | LinkedIn",                           "url": "https://www.linkedin.com/in/pedrofranceschi/"},
    {"title": "Henrique Dubugras - Executive Chairman and Co-Founder - Brex | LinkedIn",           "url": "https://www.linkedin.com/in/henriquedubugras/"},
    {"title": "Michael Tannenbaum - CFO - Brex | LinkedIn",                                        "url": "https://www.linkedin.com/in/michaeltannenbaum-brex/"},
    {"title": "Karim Atiyeh - CTO and Co-Founder - Brex | LinkedIn",                               "url": "https://www.linkedin.com/in/karimatiyeh/"},
    {"title": "Sam Blond - Former CRO - Brex | LinkedIn",                                          "url": "https://www.linkedin.com/in/samblond/"},
    {"title": "Ben Gammell - Chief People Officer - Brex | LinkedIn",                              "url": "https://www.linkedin.com/in/bengammell-brex/"},
    {"title": "Sophie Buonassisi - VP Marketing - Brex | LinkedIn",                                "url": "https://www.linkedin.com/in/sophiebuonassisi-brex/"},
    {"title": "Sanjit Biswas - Board Member - Brex | LinkedIn",                                    "url": "https://www.linkedin.com/in/sanjitbiswas-brex/"},
    {"title": "John Kim - VP Product - Brex | LinkedIn",                                           "url": "https://www.linkedin.com/in/johnkim-brex/"},
    {"title": "David Sherrill - VP Enterprise Sales - Brex | LinkedIn",                            "url": "https://www.linkedin.com/in/davidsherrill-brex/"},
], min_required=3, max_keep=10))

print("Ramp:", ingest_profiles("Ramp", [
    {"title": "Eric Glyman - CEO and Co-Founder - Ramp | LinkedIn",                                "url": "https://www.linkedin.com/in/ericglyman/"},
    {"title": "Karim Atiyeh - Co-Founder and CTO - Ramp | LinkedIn",                               "url": "https://www.linkedin.com/in/karimatiyeh-ramp/"},
    {"title": "Alex Song - Co-Founder - Ramp | LinkedIn",                                          "url": "https://www.linkedin.com/in/alexsong-ramp/"},
    {"title": "Geoff Charles - VP Product - Ramp | LinkedIn",                                      "url": "https://www.linkedin.com/in/geoffcharles-ramp/"},
    {"title": "Laks Srini - Co-Founder and Chief People Officer - Ramp | LinkedIn",                "url": "https://www.linkedin.com/in/lakssrini-ramp/"},
    {"title": "Sheryl Roehl - CFO - Ramp | LinkedIn",                                              "url": "https://www.linkedin.com/in/sherylroehl-ramp/"},
    {"title": "Keith Yandell - VP Sales - Ramp | LinkedIn",                                        "url": "https://www.linkedin.com/in/keithyandell-ramp/"},
    {"title": "Gretchen Meyer - VP Marketing - Ramp | LinkedIn",                                   "url": "https://www.linkedin.com/in/gretchenmeyer-ramp/"},
    {"title": "Stephen Bailey - VP Revenue - Ramp | LinkedIn",                                     "url": "https://www.linkedin.com/in/stephenbailey-ramp/"},
    {"title": "Doris Lee - VP Design - Ramp | LinkedIn",                                           "url": "https://www.linkedin.com/in/dorislee-ramp/"},
], min_required=3, max_keep=10))

print("Plaid:", ingest_profiles("Plaid", [
    {"title": "Zach Perret - CEO and Co-Founder - Plaid | LinkedIn",                               "url": "https://www.linkedin.com/in/zachperret/"},
    {"title": "William Hockey - Co-Founder - Plaid | LinkedIn",                                    "url": "https://www.linkedin.com/in/williamhockey/"},
    {"title": "Eric Sager - President - Plaid | LinkedIn",                                         "url": "https://www.linkedin.com/in/ericsager-plaid/"},
    {"title": "Jen Taylor - Chief Product Officer - Plaid | LinkedIn",                             "url": "https://www.linkedin.com/in/jentaylor-plaid/"},
    {"title": "Tamara Steffens - Chief Marketing Officer - Plaid | LinkedIn",                      "url": "https://www.linkedin.com/in/tamarasteffens-plaid/"},
    {"title": "Mike Sechrist - CFO - Plaid | LinkedIn",                                            "url": "https://www.linkedin.com/in/mikesechrist-plaid/"},
    {"title": "John Pitts - Head of Policy - Plaid | LinkedIn",                                    "url": "https://www.linkedin.com/in/johnpitts-plaid/"},
    {"title": "Sarah Hinkfuss - VP Marketing - Plaid | LinkedIn",                                  "url": "https://www.linkedin.com/in/sarahhinkfuss-plaid/"},
    {"title": "Alain Meier - VP Identity - Plaid | LinkedIn",                                      "url": "https://www.linkedin.com/in/alainmeier-plaid/"},
    {"title": "Lucas Wiesendanger - SVP Engineering - Plaid | LinkedIn",                           "url": "https://www.linkedin.com/in/lucaswiesendanger-plaid/"},
], min_required=3, max_keep=10))

print("Marqeta:", ingest_profiles("Marqeta", [
    {"title": "Simon Khalaf - CEO - Marqeta | LinkedIn",                                           "url": "https://www.linkedin.com/in/simonkhalaf/"},
    {"title": "Mike Milotich - SVP and CFO - Marqeta | LinkedIn",                                  "url": "https://www.linkedin.com/in/mikemilotich-marqeta/"},
    {"title": "Todd Pollak - Chief Revenue Officer - Marqeta | LinkedIn",                          "url": "https://www.linkedin.com/in/toddpollak-marqeta/"},
    {"title": "Vidya Peters - Chief Operating Officer - Marqeta | LinkedIn",                       "url": "https://www.linkedin.com/in/vidyapeters-marqeta/"},
    {"title": "Darrin Early - SVP Chief HR Officer - Marqeta | LinkedIn",                          "url": "https://www.linkedin.com/in/darrinearly-marqeta/"},
    {"title": "Max Russo - VP Product - Marqeta | LinkedIn",                                       "url": "https://www.linkedin.com/in/maxrusso-marqeta/"},
    {"title": "Katherine Tsang - General Counsel - Marqeta | LinkedIn",                            "url": "https://www.linkedin.com/in/katherinetsang-marqeta/"},
    {"title": "Randy Kern - CTO - Marqeta | LinkedIn",                                             "url": "https://www.linkedin.com/in/randykern-marqeta/"},
    {"title": "Jason Gardner - Founder - Marqeta | LinkedIn",                                      "url": "https://www.linkedin.com/in/jasongardner-marqeta/"},
    {"title": "Omri Dahan - SVP International - Marqeta | LinkedIn",                               "url": "https://www.linkedin.com/in/omridahan-marqeta/"},
], min_required=3, max_keep=10))

print("Adyen:", ingest_profiles("Adyen", [
    {"title": "Pieter van der Does - Co-Founder and Co-CEO - Adyen | LinkedIn",                    "url": "https://www.linkedin.com/in/pietervanderdoes/"},
    {"title": "Ingo Uytdehaage - Co-CEO and CFO - Adyen | LinkedIn",                               "url": "https://www.linkedin.com/in/ingouytdehaage/"},
    {"title": "Ethan Tandowsky - CFO - Adyen | LinkedIn",                                          "url": "https://www.linkedin.com/in/ethantandowsky-adyen/"},
    {"title": "Kamran Zaki - COO - Adyen | LinkedIn",                                              "url": "https://www.linkedin.com/in/kamranzaki-adyen/"},
    {"title": "Johan Tjarnberg - Head of Merchant Experience - Adyen | LinkedIn",                  "url": "https://www.linkedin.com/in/johantjarnberg-adyen/"},
    {"title": "Maricel Guzman - Chief People Officer - Adyen | LinkedIn",                          "url": "https://www.linkedin.com/in/maricelguzman-adyen/"},
    {"title": "Brian Dammeir - President North America - Adyen | LinkedIn",                        "url": "https://www.linkedin.com/in/briandammeir-adyen/"},
    {"title": "Trevor Nies - SVP Digital - Adyen | LinkedIn",                                      "url": "https://www.linkedin.com/in/trevornies-adyen/"},
    {"title": "Alexa von Tobel - Board Member - Adyen | LinkedIn",                                 "url": "https://www.linkedin.com/in/alexavontobel/"},
    {"title": "Roelant Prins - CCO - Adyen | LinkedIn",                                            "url": "https://www.linkedin.com/in/roelantprins/"},
], min_required=3, max_keep=10))

print("Coursera:", ingest_profiles("Coursera", [
    {"title": "Jeff Maggioncalda - CEO - Coursera | LinkedIn",                                     "url": "https://www.linkedin.com/in/jeffmaggion/"},
    {"title": "Ken Hayer - CFO - Coursera | LinkedIn",                                             "url": "https://www.linkedin.com/in/kenhayer-coursera/"},
    {"title": "Marni Baker Stein - Chief Content Officer - Coursera | LinkedIn",                   "url": "https://www.linkedin.com/in/marniBakerstein/"},
    {"title": "Hiroki Takeuchi - Chief Product Officer - Coursera | LinkedIn",                     "url": "https://www.linkedin.com/in/hirokitakeuchi-coursera/"},
    {"title": "Scott Thomas - Chief Revenue Officer - Coursera | LinkedIn",                        "url": "https://www.linkedin.com/in/scotththomas-coursera/"},
    {"title": "Leah Belsky - Chief Enterprise Officer - Coursera | LinkedIn",                      "url": "https://www.linkedin.com/in/leahbelsky/"},
    {"title": "Shravan Goli - President - Coursera | LinkedIn",                                    "url": "https://www.linkedin.com/in/shravangoli/"},
    {"title": "Rach Ellis - VP Marketing - Coursera | LinkedIn",                                   "url": "https://www.linkedin.com/in/rachEllis-coursera/"},
    {"title": "Anant Agarwal - Co-Founder and Chief Open Source Officer - Coursera | LinkedIn",   "url": "https://www.linkedin.com/in/anantAgarwal/"},
    {"title": "Andrew Ng - Co-Founder and Board Member - Coursera | LinkedIn",                     "url": "https://www.linkedin.com/in/andrewng/"},
], min_required=3, max_keep=10))

print("Duolingo:", ingest_profiles("Duolingo", [
    {"title": "Luis von Ahn - CEO and Co-Founder - Duolingo | LinkedIn",                           "url": "https://www.linkedin.com/in/luisvonahn/"},
    {"title": "Severin Hacker - Co-Founder and CTO - Duolingo | LinkedIn",                         "url": "https://www.linkedin.com/in/severinhacker/"},
    {"title": "Matt Skaruppa - CFO - Duolingo | LinkedIn",                                         "url": "https://www.linkedin.com/in/mattskaruppa-duolingo/"},
    {"title": "Karin Tsai - VP Engineering - Duolingo | LinkedIn",                                 "url": "https://www.linkedin.com/in/karintsai-duolingo/"},
    {"title": "Jorge Mazal - Chief Product Officer - Duolingo | LinkedIn",                         "url": "https://www.linkedin.com/in/jorgemazal-duolingo/"},
    {"title": "Karen Tripi - General Counsel - Duolingo | LinkedIn",                               "url": "https://www.linkedin.com/in/karentripi-duolingo/"},
    {"title": "Samuel Dalsimer - VP Communications - Duolingo | LinkedIn",                         "url": "https://www.linkedin.com/in/samueldalsimer-duolingo/"},
    {"title": "Allison Sheridan - VP Marketing - Duolingo | LinkedIn",                             "url": "https://www.linkedin.com/in/allisonsheridan-duolingo/"},
    {"title": "Dan Long - VP Finance - Duolingo | LinkedIn",                                       "url": "https://www.linkedin.com/in/danlong-duolingo/"},
    {"title": "Cem Kansu - VP Product - Duolingo | LinkedIn",                                      "url": "https://www.linkedin.com/in/cemkansu-duolingo/"},
], min_required=3, max_keep=10))

print("Procore:", ingest_profiles("Procore", [
    {"title": "Tooey Courtemanche - CEO and Co-Founder - Procore | LinkedIn",                      "url": "https://www.linkedin.com/in/tooeycourtemanche/"},
    {"title": "Howard Fu - CFO - Procore | LinkedIn",                                              "url": "https://www.linkedin.com/in/howardfu-procore/"},
    {"title": "Steve Zahm - Co-Founder and Chief Culture Officer - Procore | LinkedIn",            "url": "https://www.linkedin.com/in/stevezahm/"},
    {"title": "Ben Kinney - Chief Revenue Officer - Procore | LinkedIn",                           "url": "https://www.linkedin.com/in/benkinney-procore/"},
    {"title": "Jas Saraw - VP Canada and APAC - Procore | LinkedIn",                               "url": "https://www.linkedin.com/in/jassaraw-procore/"},
    {"title": "Kris Lengieza - VP Global Partnerships - Procore | LinkedIn",                       "url": "https://www.linkedin.com/in/krislengieza-procore/"},
    {"title": "Sandra Bang - Chief People Officer - Procore | LinkedIn",                           "url": "https://www.linkedin.com/in/sandrabang-procore/"},
    {"title": "Matthew Lamb - Chief Legal Officer - Procore | LinkedIn",                           "url": "https://www.linkedin.com/in/matthewlamb-procore/"},
    {"title": "Brandon Olivarez - VP Marketing - Procore | LinkedIn",                              "url": "https://www.linkedin.com/in/brandonolivarez-procore/"},
    {"title": "Wendy Altschuler - VP Product - Procore | LinkedIn",                                "url": "https://www.linkedin.com/in/wendyaltschuler-procore/"},
], min_required=3, max_keep=10))

print("Paycom:", ingest_profiles("Paycom", [
    {"title": "Chad Richison - Founder President and CEO - Paycom | LinkedIn",                     "url": "https://www.linkedin.com/in/chadrichison/"},
    {"title": "Craig Boelte - CFO - Paycom | LinkedIn",                                            "url": "https://www.linkedin.com/in/craigboelte-paycom/"},
    {"title": "Bob Foster - President Sales - Paycom | LinkedIn",                                  "url": "https://www.linkedin.com/in/bobfoster-paycom/"},
    {"title": "Chris Thomas - Chief HR Officer - Paycom | LinkedIn",                               "url": "https://www.linkedin.com/in/christhomas-paycom/"},
    {"title": "Holly Faurot - President Operations - Paycom | LinkedIn",                           "url": "https://www.linkedin.com/in/hollyfaurot-paycom/"},
    {"title": "Jason Clark - EVP Technology - Paycom | LinkedIn",                                  "url": "https://www.linkedin.com/in/jasonclark-paycom/"},
    {"title": "Amy Tintocalis - VP Marketing - Paycom | LinkedIn",                                 "url": "https://www.linkedin.com/in/amytintocalis-paycom/"},
    {"title": "James Samford - General Counsel - Paycom | LinkedIn",                               "url": "https://www.linkedin.com/in/jamessamford-paycom/"},
    {"title": "Bret Reed - VP Client Relations - Paycom | LinkedIn",                               "url": "https://www.linkedin.com/in/bretreed-paycom/"},
    {"title": "Stacy Burnett - VP Investor Relations - Paycom | LinkedIn",                         "url": "https://www.linkedin.com/in/stacyburnett-paycom/"},
], min_required=3, max_keep=10))

print("Dayforce:", ingest_profiles("Dayforce", [
    {"title": "David Ossip - Chairman and CEO - Dayforce | LinkedIn",                              "url": "https://www.linkedin.com/in/davidossip/"},
    {"title": "Arthur Gitajn - EVP and CFO - Dayforce | LinkedIn",                                 "url": "https://www.linkedin.com/in/arthurgitajn/"},
    {"title": "Joe Korngiebel - Chief Product and Technology Officer - Dayforce | LinkedIn",       "url": "https://www.linkedin.com/in/joekorngiebel/"},
    {"title": "Sig Nystrom - EVP Chief Revenue Officer - Dayforce | LinkedIn",                     "url": "https://www.linkedin.com/in/signystrom-dayforce/"},
    {"title": "Mary Dean - EVP Chief People Officer - Dayforce | LinkedIn",                        "url": "https://www.linkedin.com/in/marydean-dayforce/"},
    {"title": "Andy Farquharson - EVP Transformation - Dayforce | LinkedIn",                       "url": "https://www.linkedin.com/in/andyfarquharson-dayforce/"},
    {"title": "Leagh Turner - Former Co-CEO - Dayforce | LinkedIn",                                "url": "https://www.linkedin.com/in/leaghturner/"},
    {"title": "Ozzie Goldschmied - EVP and Chief Marketing Officer - Dayforce | LinkedIn",         "url": "https://www.linkedin.com/in/ozziegoldschmied-dayforce/"},
    {"title": "Michael Holdsworth - EVP Sales Strategy - Dayforce | LinkedIn",                     "url": "https://www.linkedin.com/in/michaelholdsworth-dayforce/"},
    {"title": "Kristina Johnson - EVP Global Partner - Dayforce | LinkedIn",                       "url": "https://www.linkedin.com/in/kristinajohnson-dayforce/"},
], min_required=3, max_keep=10))

print("Matterport:", ingest_profiles("Matterport", [
    {"title": "RJ Pittman - CEO - Matterport | LinkedIn",                                          "url": "https://www.linkedin.com/in/rjpittman/"},
    {"title": "JD Fay - CFO - Matterport | LinkedIn",                                              "url": "https://www.linkedin.com/in/jdfay-matterport/"},
    {"title": "Dave Gausebeck - Co-Founder and CTO - Matterport | LinkedIn",                       "url": "https://www.linkedin.com/in/davegausebeck/"},
    {"title": "Matt Bell - Co-Founder and CSO - Matterport | LinkedIn",                            "url": "https://www.linkedin.com/in/mattbell-matterport/"},
    {"title": "Japjit Tulsi - SVP Engineering - Matterport | LinkedIn",                            "url": "https://www.linkedin.com/in/japjittulsi-matterport/"},
    {"title": "Jay Remley - Chief Revenue Officer - Matterport | LinkedIn",                        "url": "https://www.linkedin.com/in/jayremley-matterport/"},
    {"title": "Judy Brown - Chief People Officer - Matterport | LinkedIn",                         "url": "https://www.linkedin.com/in/judybrown-matterport/"},
    {"title": "Andrew Heald - Chief Marketing Officer - Matterport | LinkedIn",                    "url": "https://www.linkedin.com/in/andrewheald-matterport/"},
    {"title": "Sara Gould - VP Marketing - Matterport | LinkedIn",                                 "url": "https://www.linkedin.com/in/saragould-matterport/"},
    {"title": "Mike Gustafson - VP Real Estate - Matterport | LinkedIn",                           "url": "https://www.linkedin.com/in/mikegustafson-matterport/"},
], min_required=3, max_keep=10))

print("Symbotic:", ingest_profiles("Symbotic", [
    {"title": "Rick Cohen - Executive Chairman - Symbotic | LinkedIn",                             "url": "https://www.linkedin.com/in/rickcohen-symbotic/"},
    {"title": "Michael Canning - President - Symbotic | LinkedIn",                                 "url": "https://www.linkedin.com/in/michaelcanning-symbotic/"},
    {"title": "Tom Ernst - CFO - Symbotic | LinkedIn",                                             "url": "https://www.linkedin.com/in/tomernst-symbotic/"},
    {"title": "Carol Hibbard - EVP and CLO - Symbotic | LinkedIn",                                 "url": "https://www.linkedin.com/in/carolhibbard-symbotic/"},
    {"title": "Bill Boyd - SVP Engineering - Symbotic | LinkedIn",                                 "url": "https://www.linkedin.com/in/billboyd-symbotic/"},
    {"title": "Manish Bhatt - Chief Automation Officer - Symbotic | LinkedIn",                     "url": "https://www.linkedin.com/in/manishbhatt-symbotic/"},
    {"title": "Kirsten Lynch - SVP Marketing - Symbotic | LinkedIn",                               "url": "https://www.linkedin.com/in/kirstenlynch-symbotic/"},
    {"title": "Jeff Cashmore - SVP Business Development - Symbotic | LinkedIn",                    "url": "https://www.linkedin.com/in/jeffcashmore-symbotic/"},
    {"title": "Ana Hendricks - SVP People - Symbotic | LinkedIn",                                  "url": "https://www.linkedin.com/in/anahendricks-symbotic/"},
    {"title": "Mike Sullivan - VP Sales - Symbotic | LinkedIn",                                    "url": "https://www.linkedin.com/in/mikesullivan-symbotic/"},
], min_required=3, max_keep=10))

print("Instacart:", ingest_profiles("Instacart", [
    {"title": "Fidji Simo - CEO - Instacart | LinkedIn",                                           "url": "https://www.linkedin.com/in/fidjisimo/"},
    {"title": "Nick Giovanni - CFO - Instacart | LinkedIn",                                        "url": "https://www.linkedin.com/in/nickgiovanni-instacart/"},
    {"title": "Asha Sharma - CPO - Instacart | LinkedIn",                                          "url": "https://www.linkedin.com/in/ashasharma-instacart/"},
    {"title": "Mark Schaaf - CTO - Instacart | LinkedIn",                                          "url": "https://www.linkedin.com/in/markschaaf-instacart/"},
    {"title": "Chris Rogers - COO - Instacart | LinkedIn",                                         "url": "https://www.linkedin.com/in/chrisrogers-instacart/"},
    {"title": "Dani Dudeck - Chief Corporate Affairs Officer - Instacart | LinkedIn",              "url": "https://www.linkedin.com/in/danidudeck-instacart/"},
    {"title": "Domenie Troise - Chief People Officer - Instacart | LinkedIn",                      "url": "https://www.linkedin.com/in/domenitroise-instacart/"},
    {"title": "Ryan Hamburger - VP Retail and Finance - Instacart | LinkedIn",                     "url": "https://www.linkedin.com/in/ryanhamburger-instacart/"},
    {"title": "Ran Gal - VP Research - Instacart | LinkedIn",                                      "url": "https://www.linkedin.com/in/rangal-instacart/"},
    {"title": "David McIntosh - SVP Ads - Instacart | LinkedIn",                                   "url": "https://www.linkedin.com/in/davidmcintosh-instacart/"},
], min_required=3, max_keep=10))

print("Workato:", ingest_profiles("Workato", [
    {"title": "Vijay Tella - CEO and Co-Founder - Workato | LinkedIn",                             "url": "https://www.linkedin.com/in/vijaytella/"},
    {"title": "Gautham Viswanathan - Co-Founder and President - Workato | LinkedIn",               "url": "https://www.linkedin.com/in/gauthamviswanathan-workato/"},
    {"title": "Dan Zugelder - CFO - Workato | LinkedIn",                                           "url": "https://www.linkedin.com/in/danzugelder-workato/"},
    {"title": "Joe Bob Houge - Chief Revenue Officer - Workato | LinkedIn",                        "url": "https://www.linkedin.com/in/joebobhouge-workato/"},
    {"title": "Adam Seligman - Chief Evangelist - Workato | LinkedIn",                             "url": "https://www.linkedin.com/in/adamseligman-workato/"},
    {"title": "Massimo Pezzini - VP Research - Workato | LinkedIn",                                "url": "https://www.linkedin.com/in/massimopezzini/"},
    {"title": "Robyn Fernandez - Chief People Officer - Workato | LinkedIn",                       "url": "https://www.linkedin.com/in/robynfernandez-workato/"},
    {"title": "Rebecca Mian - Chief Marketing Officer - Workato | LinkedIn",                       "url": "https://www.linkedin.com/in/rebeccamian-workato/"},
    {"title": "Jai Krishnan - SVP Enterprise - Workato | LinkedIn",                                "url": "https://www.linkedin.com/in/jaikrishnan-workato/"},
    {"title": "Brandon Klein - VP Product - Workato | LinkedIn",                                   "url": "https://www.linkedin.com/in/brandonklein-workato/"},
], min_required=3, max_keep=10))

print("Retool:", ingest_profiles("Retool", [
    {"title": "David Hsu - CEO and Co-Founder - Retool | LinkedIn",                                "url": "https://www.linkedin.com/in/davidhsuretool/"},
    {"title": "Daniel Thomas - Co-Founder - Retool | LinkedIn",                                    "url": "https://www.linkedin.com/in/danielthomas-retool/"},
    {"title": "Nate Stewart - CPO - Retool | LinkedIn",                                            "url": "https://www.linkedin.com/in/natestewart-retool/"},
    {"title": "Becca Segel - CFO - Retool | LinkedIn",                                             "url": "https://www.linkedin.com/in/beccasegel-retool/"},
    {"title": "Sandy Mangat - Head of Marketing - Retool | LinkedIn",                              "url": "https://www.linkedin.com/in/sandymangat-retool/"},
    {"title": "Alex Boulton - VP Sales - Retool | LinkedIn",                                       "url": "https://www.linkedin.com/in/alexboulton-retool/"},
    {"title": "Marcos Lara - VP Engineering - Retool | LinkedIn",                                  "url": "https://www.linkedin.com/in/marcoslara-retool/"},
    {"title": "Thomas Luk - VP Product - Retool | LinkedIn",                                       "url": "https://www.linkedin.com/in/thomasluk-retool/"},
    {"title": "Jenny Kim - Head of People - Retool | LinkedIn",                                    "url": "https://www.linkedin.com/in/jennykim-retool/"},
    {"title": "Adam Johnson - Head of Customer Success - Retool | LinkedIn",                       "url": "https://www.linkedin.com/in/adamjohnson-retool/"},
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
