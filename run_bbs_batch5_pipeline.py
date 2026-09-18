"""BBS Batch 5 — 20 new Fortune 500 companies, eleynxiong@berkeley.edu."""
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
    {"name": "Charles Schwab",       "domain": "schwab.com",              "industry": "Wealth Management / Brokerage / Banking",      "email_pattern": "first.last"},
    {"name": "Fiserv",               "domain": "fiserv.com",              "industry": "Fintech / Payment Processing / Banking Tech",   "email_pattern": "first.last"},
    {"name": "ADP",                  "domain": "adp.com",                 "industry": "HR Tech / Payroll / HCM",                      "email_pattern": "first.last"},
    {"name": "S&P Global",           "domain": "spglobal.com",            "industry": "Financial Data / Ratings / Analytics",         "email_pattern": "first.last"},
    {"name": "Moody's",              "domain": "moodys.com",              "industry": "Credit Ratings / Risk Analytics / Data",       "email_pattern": "first.last"},
    {"name": "Leidos",               "domain": "leidos.com",              "industry": "Defense IT / Health / Civil Cyber",            "email_pattern": "first.last"},
    {"name": "SAIC",                 "domain": "saic.com",                "industry": "Defense / Government IT / Analytics",          "email_pattern": "first.last"},
    {"name": "Becton Dickinson",     "domain": "bd.com",                  "industry": "Medical Devices / Diagnostics / Life Sciences","email_pattern": "first.last"},
    {"name": "Boston Scientific",    "domain": "bostonscientific.com",    "industry": "Medical Devices / Cardiovascular / Endo",      "email_pattern": "first.last"},
    {"name": "Danaher",              "domain": "danaher.com",             "industry": "Life Sciences / Diagnostics / Environmental",  "email_pattern": "first.last"},
    {"name": "HCA Healthcare",       "domain": "hcahealthcare.com",       "industry": "Hospital Systems / Healthcare Services",       "email_pattern": "first.last"},
    {"name": "Rockwell Automation",  "domain": "rockwellautomation.com",  "industry": "Industrial Automation / Digital Manufacturing","email_pattern": "first.last"},
    {"name": "NextEra Energy",       "domain": "nexteraenergy.com",       "industry": "Clean Energy / Utilities / Wind & Solar",      "email_pattern": "first.last"},
    {"name": "Duke Energy",          "domain": "duke-energy.com",         "industry": "Electric Utilities / Energy Transition",       "email_pattern": "first.last"},
    {"name": "Baker Hughes",         "domain": "bakerhughes.com",         "industry": "Energy Technology / Oilfield Services / LNG",  "email_pattern": "first.last"},
    {"name": "Halliburton",          "domain": "halliburton.com",         "industry": "Oilfield Services / Energy / Drilling",       "email_pattern": "first.last"},
    {"name": "TJX Companies",        "domain": "tjx.com",                 "industry": "Off-Price Retail / Consumer Goods",            "email_pattern": "first.last"},
    {"name": "Dollar General",       "domain": "dollargeneral.com",       "industry": "Discount Retail / Consumer Staples",           "email_pattern": "first.last"},
    {"name": "Cognizant",            "domain": "cognizant.com",           "industry": "IT Services / Digital Transformation / AI",   "email_pattern": "first.last"},
    {"name": "Gartner",              "domain": "gartner.com",             "industry": "Research / Advisory / IT / Data",              "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 5 - July 2026"
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

print("Charles Schwab:", ingest_profiles("Charles Schwab", [
    {"title": "Rick Wurster - President and CEO - Charles Schwab | LinkedIn",                "url": "https://www.linkedin.com/in/rickwurster/"},
    {"title": "Peter Crawford - EVP and CFO - Charles Schwab | LinkedIn",                    "url": "https://www.linkedin.com/in/petercrawford-schwab/"},
    {"title": "Jonathan Craig - EVP Investor Services - Charles Schwab | LinkedIn",          "url": "https://www.linkedin.com/in/jonathancraig-schwab/"},
    {"title": "Joe Martinetto - EVP COO - Charles Schwab | LinkedIn",                        "url": "https://www.linkedin.com/in/joemartinetto/"},
    {"title": "Jeff Edwards - EVP General Counsel - Charles Schwab | LinkedIn",              "url": "https://www.linkedin.com/in/jeffedwards-schwab/"},
    {"title": "Terri Kallsen - EVP Workplace Financial Services - Charles Schwab | LinkedIn","url": "https://www.linkedin.com/in/terrikallsen/"},
    {"title": "Neesha Hathi - EVP Chief Digital Officer - Charles Schwab | LinkedIn",        "url": "https://www.linkedin.com/in/neeshahathi/"},
    {"title": "Barry Metzger - EVP International - Charles Schwab | LinkedIn",               "url": "https://www.linkedin.com/in/barrymetzger-schwab/"},
    {"title": "Mike Verdeschi - EVP Treasurer - Charles Schwab | LinkedIn",                  "url": "https://www.linkedin.com/in/mikeverdeschi/"},
    {"title": "Mark Bettencourt - VP HR - Charles Schwab | LinkedIn",                        "url": "https://www.linkedin.com/in/markbettencourt-schwab/"},
], min_required=3, max_keep=10))

print("Fiserv:", ingest_profiles("Fiserv", [
    {"title": "Frank Bisignano - Chairman and CEO - Fiserv | LinkedIn",                      "url": "https://www.linkedin.com/in/frankbisignano/"},
    {"title": "Bob Hau - CFO - Fiserv | LinkedIn",                                           "url": "https://www.linkedin.com/in/bobhau-fiserv/"},
    {"title": "Guy Chiarello - President - Fiserv | LinkedIn",                               "url": "https://www.linkedin.com/in/guychiarello/"},
    {"title": "Jim Subers - President Banking Solutions - Fiserv | LinkedIn",                "url": "https://www.linkedin.com/in/jimsubers/"},
    {"title": "Kevin Schultz - President International - Fiserv | LinkedIn",                 "url": "https://www.linkedin.com/in/kevinschultz-fiserv/"},
    {"title": "Rahul Gupta - Chief Technology Officer - Fiserv | LinkedIn",                  "url": "https://www.linkedin.com/in/rahulgupta-fiserv/"},
    {"title": "Anne Pauk - Chief Legal Officer - Fiserv | LinkedIn",                         "url": "https://www.linkedin.com/in/annepauk/"},
    {"title": "Takis Georgakopoulos - President Enterprise - Fiserv | LinkedIn",             "url": "https://www.linkedin.com/in/takisgeorgakopoulos/"},
    {"title": "Byron Vielehr - President Global Business Solutions - Fiserv | LinkedIn",     "url": "https://www.linkedin.com/in/byronvielehr/"},
    {"title": "Andrea Doering - Chief People Officer - Fiserv | LinkedIn",                   "url": "https://www.linkedin.com/in/andreadoering-fiserv/"},
], min_required=3, max_keep=10))

print("ADP:", ingest_profiles("ADP", [
    {"title": "Maria Black - President and CEO - ADP | LinkedIn",                            "url": "https://www.linkedin.com/in/mariablack-adp/"},
    {"title": "Don McGuire - SVP and CFO - ADP | LinkedIn",                                  "url": "https://www.linkedin.com/in/donmcguire-adp/"},
    {"title": "Sreeni Kutam - Chief People Officer - ADP | LinkedIn",                        "url": "https://www.linkedin.com/in/sreenikutam/"},
    {"title": "Stuart Sackman - Group President Technology and Client Service - ADP | LinkedIn","url": "https://www.linkedin.com/in/stuartsackman/"},
    {"title": "John Ayala - Group President Americas - ADP | LinkedIn",                      "url": "https://www.linkedin.com/in/johnayala-adp/"},
    {"title": "Michael Bonarti - General Counsel - ADP | LinkedIn",                          "url": "https://www.linkedin.com/in/michaelbonarti/"},
    {"title": "Nela Richardson - Chief Economist - ADP | LinkedIn",                          "url": "https://www.linkedin.com/in/nelarichardson/"},
    {"title": "Tami Coyne - Group President Europe - ADP | LinkedIn",                        "url": "https://www.linkedin.com/in/tamicoyne/"},
    {"title": "Carlos Rodriguez - Executive Chairman - ADP | LinkedIn",                      "url": "https://www.linkedin.com/in/carlosrodriguez-adp/"},
    {"title": "Derik Sutton - VP Marketing - ADP | LinkedIn",                                "url": "https://www.linkedin.com/in/deriksutton/"},
], min_required=3, max_keep=10))

print("S&P Global:", ingest_profiles("S&P Global", [
    {"title": "Martina Cheung - President and CEO - S&P Global | LinkedIn",                  "url": "https://www.linkedin.com/in/martinacheung/"},
    {"title": "Ewout Steenbergen - EVP and CFO - S&P Global | LinkedIn",                     "url": "https://www.linkedin.com/in/ewoutsteenbergen/"},
    {"title": "Adam Kansler - President Market Intelligence - S&P Global | LinkedIn",        "url": "https://www.linkedin.com/in/adamkansler/"},
    {"title": "Saugata Saha - President S&P Dow Jones Indices - S&P Global | LinkedIn",      "url": "https://www.linkedin.com/in/saugatasaha/"},
    {"title": "Manav Garg - President Commodity Insights - S&P Global | LinkedIn",           "url": "https://www.linkedin.com/in/manavgarg/"},
    {"title": "Yann Le Pallec - President S&P Global Ratings - S&P Global | LinkedIn",       "url": "https://www.linkedin.com/in/yannlepallec/"},
    {"title": "Daniel Yergin - Vice Chairman - S&P Global | LinkedIn",                       "url": "https://www.linkedin.com/in/danielyergin/"},
    {"title": "Chris Craig - Chief People Officer - S&P Global | LinkedIn",                  "url": "https://www.linkedin.com/in/chriscraig-spglobal/"},
    {"title": "Lucy Fato - EVP General Counsel - S&P Global | LinkedIn",                     "url": "https://www.linkedin.com/in/lucyfato/"},
    {"title": "Chip Merritt - VP Investor Relations - S&P Global | LinkedIn",                "url": "https://www.linkedin.com/in/chipmerritt/"},
], min_required=3, max_keep=10))

print("Moody's:", ingest_profiles("Moody's", [
    {"title": "Robert Fauber - President and CEO - Moody's | LinkedIn",                      "url": "https://www.linkedin.com/in/robertfauber/"},
    {"title": "Noemie Heuland - CFO - Moody's | LinkedIn",                                   "url": "https://www.linkedin.com/in/noemieheuland/"},
    {"title": "Stephen Tulenko - President Moody's Analytics - Moody's | LinkedIn",          "url": "https://www.linkedin.com/in/stephentulenko/"},
    {"title": "Michael Rowan - President Moody's Ratings - Moody's | LinkedIn",              "url": "https://www.linkedin.com/in/michaelrowan-moodys/"},
    {"title": "Richard Cantor - Chief Credit Officer - Moody's | LinkedIn",                  "url": "https://www.linkedin.com/in/richardcantor/"},
    {"title": "Caroline Sullivan - Chief People Officer - Moody's | LinkedIn",               "url": "https://www.linkedin.com/in/carolinesullivan-moodys/"},
    {"title": "Shivani Kak - Chief Compliance Officer - Moody's | LinkedIn",                 "url": "https://www.linkedin.com/in/shivanikak/"},
    {"title": "Steven Balet - SVP General Counsel - Moody's | LinkedIn",                     "url": "https://www.linkedin.com/in/stevenbalet/"},
    {"title": "Atsi Sheth - MD Chief Credit Strategy Officer - Moody's | LinkedIn",          "url": "https://www.linkedin.com/in/atsisheth/"},
    {"title": "Mark Almeida - Former President Moody's Analytics - Moody's | LinkedIn",      "url": "https://www.linkedin.com/in/markalmeida-moodys/"},
], min_required=3, max_keep=10))

print("Leidos:", ingest_profiles("Leidos", [
    {"title": "Tom Bell - President and CEO - Leidos | LinkedIn",                            "url": "https://www.linkedin.com/in/tombell-leidos/"},
    {"title": "Chris Cage - EVP and CFO - Leidos | LinkedIn",                                "url": "https://www.linkedin.com/in/chriscage-leidos/"},
    {"title": "Roger Krone - Executive Chairman - Leidos | LinkedIn",                        "url": "https://www.linkedin.com/in/rogerkrone/"},
    {"title": "Jim Carlini - President Defense Systems - Leidos | LinkedIn",                 "url": "https://www.linkedin.com/in/jimcarlini/"},
    {"title": "Gerry Fasano - President Civilian Markets - Leidos | LinkedIn",               "url": "https://www.linkedin.com/in/gerryfasano/"},
    {"title": "Angela Heise - EVP Health Solutions - Leidos | LinkedIn",                     "url": "https://www.linkedin.com/in/angelaheise/"},
    {"title": "Vicki Schmanske - EVP Chief Administrative Officer - Leidos | LinkedIn",      "url": "https://www.linkedin.com/in/vickischmanske/"},
    {"title": "Jerald Howe Jr. - EVP General Counsel - Leidos | LinkedIn",                   "url": "https://www.linkedin.com/in/jerald-howe/"},
    {"title": "Liz Porter - EVP National Security - Leidos | LinkedIn",                      "url": "https://www.linkedin.com/in/lizporter-leidos/"},
    {"title": "Dan Lauer - SVP Strategy - Leidos | LinkedIn",                                "url": "https://www.linkedin.com/in/danlauer-leidos/"},
], min_required=3, max_keep=10))

print("SAIC:", ingest_profiles("SAIC", [
    {"title": "Toni Townes-Whitley - President and CEO - SAIC | LinkedIn",                   "url": "https://www.linkedin.com/in/tonitowneswhitley/"},
    {"title": "Prabu Natarajan - EVP and CFO - SAIC | LinkedIn",                             "url": "https://www.linkedin.com/in/prabunatarajan/"},
    {"title": "Bob Genter - EVP and COO - SAIC | LinkedIn",                                  "url": "https://www.linkedin.com/in/bobgenter/"},
    {"title": "DeEtte Gray - EVP Defense and Civilian Sector - SAIC | LinkedIn",             "url": "https://www.linkedin.com/in/deettegray/"},
    {"title": "Tommy Gardner - CTO - SAIC | LinkedIn",                                       "url": "https://www.linkedin.com/in/tommygardner-saic/"},
    {"title": "Laura McGee - Chief HR Officer - SAIC | LinkedIn",                            "url": "https://www.linkedin.com/in/lauramcgee-saic/"},
    {"title": "Steve Mahon - SVP General Counsel - SAIC | LinkedIn",                         "url": "https://www.linkedin.com/in/stevemahon-saic/"},
    {"title": "Claude Tucker - SVP Strategy and Business Development - SAIC | LinkedIn",     "url": "https://www.linkedin.com/in/claudetucker/"},
    {"title": "John Heller - EVP National Security Sector - SAIC | LinkedIn",               "url": "https://www.linkedin.com/in/johnheller-saic/"},
    {"title": "Mike LaRouche - SVP Chief Marketing Officer - SAIC | LinkedIn",               "url": "https://www.linkedin.com/in/mikelarouche/"},
], min_required=3, max_keep=10))

print("Becton Dickinson:", ingest_profiles("Becton Dickinson", [
    {"title": "Tom Polen - Chairman and CEO - Becton Dickinson | LinkedIn",                  "url": "https://www.linkedin.com/in/tompolen/"},
    {"title": "Christopher Reidy - EVP and CFO - Becton Dickinson | LinkedIn",               "url": "https://www.linkedin.com/in/christopherreidy-bd/"},
    {"title": "Simon Campion - EVP President BD Interventional - Becton Dickinson | LinkedIn","url": "https://www.linkedin.com/in/simoncampion/"},
    {"title": "Dave Hickey - President BD Life Sciences - Becton Dickinson | LinkedIn",      "url": "https://www.linkedin.com/in/davehickey-bd/"},
    {"title": "Alberto Mas - EVP Chief People Officer - Becton Dickinson | LinkedIn",        "url": "https://www.linkedin.com/in/albertomas-bd/"},
    {"title": "Gary DeFazio - SVP General Counsel - Becton Dickinson | LinkedIn",            "url": "https://www.linkedin.com/in/garydefazio/"},
    {"title": "Arlene Sawicki - EVP President Medical - Becton Dickinson | LinkedIn",        "url": "https://www.linkedin.com/in/arlenesawicki/"},
    {"title": "David Messinger - SVP Strategy - Becton Dickinson | LinkedIn",                "url": "https://www.linkedin.com/in/davidmessinger-bd/"},
    {"title": "Jim Borzi - President BD Interventional - Becton Dickinson | LinkedIn",       "url": "https://www.linkedin.com/in/jimborzi/"},
    {"title": "Thomas Polen - CEO - Becton Dickinson | LinkedIn",                            "url": "https://www.linkedin.com/in/thomaspolen/"},
], min_required=3, max_keep=10))

print("Boston Scientific:", ingest_profiles("Boston Scientific", [
    {"title": "Mike Mahoney - Chairman and CEO - Boston Scientific | LinkedIn",              "url": "https://www.linkedin.com/in/mikemahoney-bsc/"},
    {"title": "Dan Brennan - EVP and CFO - Boston Scientific | LinkedIn",                    "url": "https://www.linkedin.com/in/danbrennan-bsc/"},
    {"title": "Meghan Scanlon - EVP President Cardiology - Boston Scientific | LinkedIn",    "url": "https://www.linkedin.com/in/meghanscanlon-bsc/"},
    {"title": "Joe Fitzgerald - EVP President Rhythm Management - Boston Scientific | LinkedIn","url": "https://www.linkedin.com/in/joefitzgerald-bsc/"},
    {"title": "David Pierce - EVP President Endoscopy - Boston Scientific | LinkedIn",       "url": "https://www.linkedin.com/in/davidpierce-bsc/"},
    {"title": "Jeff Mirviss - EVP President Urology - Boston Scientific | LinkedIn",         "url": "https://www.linkedin.com/in/jeffmirviss/"},
    {"title": "Wendy Carruthers - EVP Chief People Officer - Boston Scientific | LinkedIn",  "url": "https://www.linkedin.com/in/wendycarruthers-bsc/"},
    {"title": "Jon Monson - SVP General Counsel - Boston Scientific | LinkedIn",             "url": "https://www.linkedin.com/in/jonmonson/"},
    {"title": "Vance Brown - President Neuromodulation - Boston Scientific | LinkedIn",      "url": "https://www.linkedin.com/in/vancebrown-bsc/"},
    {"title": "Art Butcher - EVP President MedSurg - Boston Scientific | LinkedIn",          "url": "https://www.linkedin.com/in/artbutcher-bsc/"},
], min_required=3, max_keep=10))

print("Danaher:", ingest_profiles("Danaher", [
    {"title": "Rainer Blair - President and CEO - Danaher | LinkedIn",                       "url": "https://www.linkedin.com/in/rainerblair/"},
    {"title": "Matthew McGrew - EVP and CFO - Danaher | LinkedIn",                           "url": "https://www.linkedin.com/in/matthewmcgrew/"},
    {"title": "Jennifer Honeycutt - EVP President Biotechnology - Danaher | LinkedIn",       "url": "https://www.linkedin.com/in/jenniferhoneycutt/"},
    {"title": "John Bedford - EVP President Life Sciences - Danaher | LinkedIn",             "url": "https://www.linkedin.com/in/johnbedford-danaher/"},
    {"title": "Angela Lalor - SVP HR - Danaher | LinkedIn",                                  "url": "https://www.linkedin.com/in/angelalalor/"},
    {"title": "Matt Gugino - SVP Strategy - Danaher | LinkedIn",                             "url": "https://www.linkedin.com/in/mattgugino/"},
    {"title": "James Lico - Former President - Danaher | LinkedIn",                          "url": "https://www.linkedin.com/in/jameslico/"},
    {"title": "William Daniel - SVP General Counsel - Danaher | LinkedIn",                   "url": "https://www.linkedin.com/in/williamdaniel-danaher/"},
    {"title": "Andrew Wilson - EVP - Danaher | LinkedIn",                                    "url": "https://www.linkedin.com/in/andrewwilson-danaher/"},
    {"title": "Joakim Weidemanis - EVP President Diagnostics - Danaher | LinkedIn",          "url": "https://www.linkedin.com/in/joakimweidemanis/"},
], min_required=3, max_keep=10))

print("HCA Healthcare:", ingest_profiles("HCA Healthcare", [
    {"title": "Sam Hazen - CEO - HCA Healthcare | LinkedIn",                                 "url": "https://www.linkedin.com/in/samhazen/"},
    {"title": "Bill Rutherford - EVP and CFO - HCA Healthcare | LinkedIn",                   "url": "https://www.linkedin.com/in/billrutherford-hca/"},
    {"title": "Jon Foster - EVP Operations - HCA Healthcare | LinkedIn",                     "url": "https://www.linkedin.com/in/jonfoster-hca/"},
    {"title": "Chuck Hall - SVP and CIO - HCA Healthcare | LinkedIn",                        "url": "https://www.linkedin.com/in/chuckhall-hca/"},
    {"title": "Jane Englebright - VP Chief Nursing Executive - HCA Healthcare | LinkedIn",   "url": "https://www.linkedin.com/in/janeenglebright/"},
    {"title": "Alan Yuspeh - SVP Ethics and Compliance - HCA Healthcare | LinkedIn",         "url": "https://www.linkedin.com/in/alanyuspeh/"},
    {"title": "Joseph Sowell - EVP Clinical Operations - HCA Healthcare | LinkedIn",         "url": "https://www.linkedin.com/in/josephsowell/"},
    {"title": "Phillip Billington - SVP HR - HCA Healthcare | LinkedIn",                     "url": "https://www.linkedin.com/in/phillipbillington/"},
    {"title": "Michael Cuffe - VP Quality and Education - HCA Healthcare | LinkedIn",        "url": "https://www.linkedin.com/in/michaelcuffe-hca/"},
    {"title": "Victor Campbell - SVP Strategy - HCA Healthcare | LinkedIn",                  "url": "https://www.linkedin.com/in/victorcampbell-hca/"},
], min_required=3, max_keep=10))

print("Rockwell Automation:", ingest_profiles("Rockwell Automation", [
    {"title": "Blake Moret - Chairman and CEO - Rockwell Automation | LinkedIn",             "url": "https://www.linkedin.com/in/blakemoret/"},
    {"title": "Nicholas Gangestad - SVP and CFO - Rockwell Automation | LinkedIn",           "url": "https://www.linkedin.com/in/nicholasgangestad/"},
    {"title": "Tessa Myers - SVP Intelligent Devices - Rockwell Automation | LinkedIn",      "url": "https://www.linkedin.com/in/tessamyers-rockwell/"},
    {"title": "Scott Kortier - SVP Software and Control - Rockwell Automation | LinkedIn",   "url": "https://www.linkedin.com/in/scottkortier/"},
    {"title": "John Miller - SVP Human Resources - Rockwell Automation | LinkedIn",          "url": "https://www.linkedin.com/in/johnmiller-rockwellautomation/"},
    {"title": "Rebecca House - SVP General Counsel - Rockwell Automation | LinkedIn",        "url": "https://www.linkedin.com/in/rebeccahouse-ra/"},
    {"title": "Cyril Perducat - SVP Digital Transformation - Rockwell Automation | LinkedIn","url": "https://www.linkedin.com/in/cyrilperducat/"},
    {"title": "Veena Lakkundi - SVP Strategy - Rockwell Automation | LinkedIn",              "url": "https://www.linkedin.com/in/veenalakkundi/"},
    {"title": "Susana Gonzalez - President APAC - Rockwell Automation | LinkedIn",           "url": "https://www.linkedin.com/in/susanagonzalez-ra/"},
    {"title": "Christian Dinesen - VP EMEA - Rockwell Automation | LinkedIn",                "url": "https://www.linkedin.com/in/christiandinesen/"},
], min_required=3, max_keep=10))

print("NextEra Energy:", ingest_profiles("NextEra Energy", [
    {"title": "John Ketchum - President and CEO - NextEra Energy | LinkedIn",                "url": "https://www.linkedin.com/in/johnketchum-nextera/"},
    {"title": "Kirk Crews - EVP and CFO - NextEra Energy | LinkedIn",                        "url": "https://www.linkedin.com/in/kirkcrews/"},
    {"title": "Rebecca Kujawa - President and CEO FPL Energy Resources - NextEra | LinkedIn","url": "https://www.linkedin.com/in/rebeccakujawa/"},
    {"title": "Armando Pimentel - President NextEra Energy Partners - NextEra | LinkedIn",   "url": "https://www.linkedin.com/in/armandopimentel/"},
    {"title": "Eric Silagy - Former President Florida Power and Light - NextEra | LinkedIn", "url": "https://www.linkedin.com/in/ericsilagy/"},
    {"title": "Amy Cortese - VP Human Resources - NextEra Energy | LinkedIn",                "url": "https://www.linkedin.com/in/amycortese-nextera/"},
    {"title": "Charles Sieving - EVP General Counsel - NextEra Energy | LinkedIn",           "url": "https://www.linkedin.com/in/charlessieving/"},
    {"title": "James Robo - Executive Chairman - NextEra Energy | LinkedIn",                 "url": "https://www.linkedin.com/in/jamesrobo/"},
    {"title": "Manoochehr Naraghi - VP Strategy - NextEra Energy | LinkedIn",                "url": "https://www.linkedin.com/in/manoochehrnaraghi/"},
    {"title": "Deborah Caplan - VP HR and Corporate Communications - NextEra | LinkedIn",    "url": "https://www.linkedin.com/in/deborahcaplan-nextera/"},
], min_required=3, max_keep=10))

print("Duke Energy:", ingest_profiles("Duke Energy", [
    {"title": "Lynn Good - Chairman President and CEO - Duke Energy | LinkedIn",             "url": "https://www.linkedin.com/in/lynngood/"},
    {"title": "Steve Young - EVP and CFO - Duke Energy | LinkedIn",                          "url": "https://www.linkedin.com/in/steveyoung-duke/"},
    {"title": "Kodwo Ghartey-Tagoe - EVP Chief Legal Officer - Duke Energy | LinkedIn",      "url": "https://www.linkedin.com/in/kodwogharteytagoe/"},
    {"title": "Harry Sideris - President Carolinas - Duke Energy | LinkedIn",                "url": "https://www.linkedin.com/in/harrysideris/"},
    {"title": "Stan Pinegar - President Indiana and Ohio - Duke Energy | LinkedIn",          "url": "https://www.linkedin.com/in/stanpinegar/"},
    {"title": "Chris Fallon - President Duke Energy Ohio and Kentucky - Duke Energy | LinkedIn","url": "https://www.linkedin.com/in/chrisfallon-duke/"},
    {"title": "Julie Janson - EVP Customer Experience - Duke Energy | LinkedIn",             "url": "https://www.linkedin.com/in/juliejanson-duke/"},
    {"title": "David Malcom - SVP Human Resources - Duke Energy | LinkedIn",                 "url": "https://www.linkedin.com/in/davidmalcom/"},
    {"title": "Tim Pettit - EVP Operations - Duke Energy | LinkedIn",                        "url": "https://www.linkedin.com/in/timpettit-duke/"},
    {"title": "Melissa Anderson - EVP Chief Administrative Officer - Duke Energy | LinkedIn","url": "https://www.linkedin.com/in/melissaanderson-duke/"},
], min_required=3, max_keep=10))

print("Baker Hughes:", ingest_profiles("Baker Hughes", [
    {"title": "Lorenzo Simonelli - Chairman President and CEO - Baker Hughes | LinkedIn",    "url": "https://www.linkedin.com/in/lorenzosimonelli/"},
    {"title": "Nancy Buese - EVP and CFO - Baker Hughes | LinkedIn",                         "url": "https://www.linkedin.com/in/nancybuese/"},
    {"title": "Maria Claudia Borras - EVP Oilfield Services - Baker Hughes | LinkedIn",      "url": "https://www.linkedin.com/in/mariaclaudiaborras/"},
    {"title": "Rod Christie - EVP Industrial and Energy Technology - Baker Hughes | LinkedIn","url": "https://www.linkedin.com/in/rodchristie-bh/"},
    {"title": "Derek Mathieson - Chief Technology Officer - Baker Hughes | LinkedIn",        "url": "https://www.linkedin.com/in/derekmathieson/"},
    {"title": "Robert Rajam - Chief HR Officer - Baker Hughes | LinkedIn",                   "url": "https://www.linkedin.com/in/robertrajam/"},
    {"title": "Ali Mese - VP Strategy and Corporate Development - Baker Hughes | LinkedIn",  "url": "https://www.linkedin.com/in/alimese/"},
    {"title": "Cathy Mann - VP Communications - Baker Hughes | LinkedIn",                    "url": "https://www.linkedin.com/in/cathymann-bh/"},
    {"title": "Tom Simons - EVP Digital Solutions - Baker Hughes | LinkedIn",                "url": "https://www.linkedin.com/in/tomsimons-bh/"},
    {"title": "Chris Drumgoole - Chief Digital Officer - Baker Hughes | LinkedIn",           "url": "https://www.linkedin.com/in/chrisdrumgoole/"},
], min_required=3, max_keep=10))

print("Halliburton:", ingest_profiles("Halliburton", [
    {"title": "Jeff Miller - Chairman President and CEO - Halliburton | LinkedIn",           "url": "https://www.linkedin.com/in/jeffmiller-halliburton/"},
    {"title": "Eric Carre - EVP and CFO - Halliburton | LinkedIn",                           "url": "https://www.linkedin.com/in/ericcarre/"},
    {"title": "Joe Rainey - President Eastern Hemisphere - Halliburton | LinkedIn",          "url": "https://www.linkedin.com/in/joerainey-halliburton/"},
    {"title": "Manu Nair - President Western Hemisphere - Halliburton | LinkedIn",           "url": "https://www.linkedin.com/in/manunair-halliburton/"},
    {"title": "Nagaraj Srinivasan - EVP Global Business Lines - Halliburton | LinkedIn",     "url": "https://www.linkedin.com/in/nagarajsrinivasan/"},
    {"title": "Van Beckwith - EVP General Counsel - Halliburton | LinkedIn",                 "url": "https://www.linkedin.com/in/vanbeckwith/"},
    {"title": "Lawrence Pope - EVP Administration and HR - Halliburton | LinkedIn",          "url": "https://www.linkedin.com/in/lawrencepope-halliburton/"},
    {"title": "Barry Goddard - VP Investor Relations - Halliburton | LinkedIn",              "url": "https://www.linkedin.com/in/barrygoddard-hal/"},
    {"title": "Anne Claire Coyne - VP Strategy - Halliburton | LinkedIn",                    "url": "https://www.linkedin.com/in/anneclairecoyne/"},
    {"title": "Robb Voyles - SVP Finance - Halliburton | LinkedIn",                          "url": "https://www.linkedin.com/in/robbvoyles/"},
], min_required=3, max_keep=10))

print("TJX Companies:", ingest_profiles("TJX Companies", [
    {"title": "Ernie Herrman - CEO and President - TJX Companies | LinkedIn",               "url": "https://www.linkedin.com/in/ernieherrman/"},
    {"title": "John Klinger - SVP and CFO - TJX Companies | LinkedIn",                      "url": "https://www.linkedin.com/in/johnklinger-tjx/"},
    {"title": "Carol Meyrowitz - Executive Chairman - TJX Companies | LinkedIn",             "url": "https://www.linkedin.com/in/carolmeyrowitz/"},
    {"title": "Ken Canestrari - Group President Marmaxx - TJX Companies | LinkedIn",        "url": "https://www.linkedin.com/in/kencanestrari/"},
    {"title": "Ann McCauley - President HomeGoods - TJX Companies | LinkedIn",              "url": "https://www.linkedin.com/in/annmccauley-tjx/"},
    {"title": "Richard Sherr - Group President TJX International - TJX Companies | LinkedIn","url": "https://www.linkedin.com/in/richardsherr-tjx/"},
    {"title": "Douglas Wilber - President Sierra - TJX Companies | LinkedIn",               "url": "https://www.linkedin.com/in/douglaswilber/"},
    {"title": "Michael MacMillan - VP Human Resources - TJX Companies | LinkedIn",          "url": "https://www.linkedin.com/in/michaelmacmillan-tjx/"},
    {"title": "Bridget Ryan - Chief Merchant - TJX Companies | LinkedIn",                   "url": "https://www.linkedin.com/in/bridgetryan-tjx/"},
    {"title": "Alicia Kelly - SVP Global Responsibility - TJX Companies | LinkedIn",        "url": "https://www.linkedin.com/in/aliciakelly-tjx/"},
], min_required=3, max_keep=10))

print("Dollar General:", ingest_profiles("Dollar General", [
    {"title": "Todd Vasos - CEO - Dollar General | LinkedIn",                                "url": "https://www.linkedin.com/in/toddvasos/"},
    {"title": "Kelly Dilts - EVP and CFO - Dollar General | LinkedIn",                       "url": "https://www.linkedin.com/in/kellydilts/"},
    {"title": "Tony Zuazo - EVP Store Operations - Dollar General | LinkedIn",               "url": "https://www.linkedin.com/in/tonyzuazo/"},
    {"title": "Emily Taylor - EVP and CMO - Dollar General | LinkedIn",                      "url": "https://www.linkedin.com/in/emilytaylor-dg/"},
    {"title": "Rhonda Taylor - EVP General Counsel - Dollar General | LinkedIn",             "url": "https://www.linkedin.com/in/rhondataylor-dg/"},
    {"title": "Jonah Ellin - EVP Digital and Emerging Business - Dollar General | LinkedIn", "url": "https://www.linkedin.com/in/jonahellin/"},
    {"title": "Kathy Reardon - SVP Human Resources - Dollar General | LinkedIn",             "url": "https://www.linkedin.com/in/kathyreardon-dg/"},
    {"title": "Steve Sunderland - EVP Store Operations - Dollar General | LinkedIn",         "url": "https://www.linkedin.com/in/stevesunderland-dg/"},
    {"title": "John Flanigan - EVP Global Supply Chain - Dollar General | LinkedIn",         "url": "https://www.linkedin.com/in/johnflanigan-dg/"},
    {"title": "Dan Owen - EVP Merchandise - Dollar General | LinkedIn",                      "url": "https://www.linkedin.com/in/danowen-dg/"},
], min_required=3, max_keep=10))

print("Cognizant:", ingest_profiles("Cognizant", [
    {"title": "Ravi Kumar S - CEO - Cognizant | LinkedIn",                                   "url": "https://www.linkedin.com/in/ravikumars/"},
    {"title": "Jatin Dalal - CFO - Cognizant | LinkedIn",                                    "url": "https://www.linkedin.com/in/jatindalal/"},
    {"title": "Becky Schmitt - Chief People Officer - Cognizant | LinkedIn",                 "url": "https://www.linkedin.com/in/beckyschmitt/"},
    {"title": "Surya Gummadi - President North America - Cognizant | LinkedIn",              "url": "https://www.linkedin.com/in/suryagummadi/"},
    {"title": "Rajesh Nambiar - President Digital Business and Technology - Cognizant | LinkedIn","url": "https://www.linkedin.com/in/rajeshnambiar/"},
    {"title": "Bhaskar Ghosh - Chief Strategy Officer - Cognizant | LinkedIn",               "url": "https://www.linkedin.com/in/bhaskarghosh-cognizant/"},
    {"title": "Eric Westphal - Chief Marketing Officer - Cognizant | LinkedIn",              "url": "https://www.linkedin.com/in/ericwestphal/"},
    {"title": "Ramakrishnan Chandrasekaran - EVP Technology and Operations - Cognizant | LinkedIn","url": "https://www.linkedin.com/in/ramakrishnanchandrasekaran/"},
    {"title": "Srinivasan Rengarajan - President Europe - Cognizant | LinkedIn",             "url": "https://www.linkedin.com/in/srinivasanrengarajan/"},
    {"title": "Greg Hyttenrauch - VP Consulting Services - Cognizant | LinkedIn",            "url": "https://www.linkedin.com/in/greghyttenrauch/"},
], min_required=3, max_keep=10))

print("Gartner:", ingest_profiles("Gartner", [
    {"title": "Gene Hall - CEO - Gartner | LinkedIn",                                        "url": "https://www.linkedin.com/in/genehall/"},
    {"title": "Craig Safian - EVP and CFO - Gartner | LinkedIn",                             "url": "https://www.linkedin.com/in/craigsafian/"},
    {"title": "Robin Kranich - Chief People Officer - Gartner | LinkedIn",                   "url": "https://www.linkedin.com/in/robinkranich/"},
    {"title": "Michael Harris - EVP Research and Advisory - Gartner | LinkedIn",             "url": "https://www.linkedin.com/in/michaelharris-gartner/"},
    {"title": "Alwyn Dawkins - President Asia Pacific - Gartner | LinkedIn",                 "url": "https://www.linkedin.com/in/alwyndawkins/"},
    {"title": "Chris Howard - VP Distinguished Analyst - Gartner | LinkedIn",                "url": "https://www.linkedin.com/in/chrishoward-gartner/"},
    {"title": "Vikram Sehgal - EVP Product Management - Gartner | LinkedIn",                 "url": "https://www.linkedin.com/in/vikramsehgal-gartner/"},
    {"title": "Jules Kaufman - SVP General Counsel - Gartner | LinkedIn",                    "url": "https://www.linkedin.com/in/juleskaufman/"},
    {"title": "Paul Furtado - VP Analyst - Gartner | LinkedIn",                              "url": "https://www.linkedin.com/in/paulfurtado-gartner/"},
    {"title": "Sandy Shen - VP Distinguished Analyst - Gartner | LinkedIn",                  "url": "https://www.linkedin.com/in/sandyshen-gartner/"},
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
