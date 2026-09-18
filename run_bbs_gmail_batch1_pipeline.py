"""
BBS Gmail Batch 1 — sent from eleynxiong@gmail.com.
15 new companies not previously contacted via BBS.
exclude_contacted=True ensures no person receives more than one email across all orgs.
"""
import sys, time, random, sqlite3
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import config
# Override sender to gmail address for this batch
config.SENDER_EMAIL = "eleynxiong@gmail.com"
config.SENDER_NAME  = "Eleyn Xiong"

from db import get_db, new_id, init_db
from linkedin_ingest import ingest_profiles
from personalize_once import personalize_once_per_company
from gmail_client import GmailClient
from datetime import datetime

init_db()

COMPANIES = [
    {"name": "Slack",                    "domain": "slack.com",           "industry": "Enterprise SaaS / Collaboration",       "email_pattern": "first.last"},
    {"name": "Atlassian",                "domain": "atlassian.com",       "industry": "Developer Tools / Enterprise SaaS",     "email_pattern": "first.last"},
    {"name": "Replit",                   "domain": "replit.com",          "industry": "AI Dev Tools / Cloud IDE",              "email_pattern": "first.last"},
    {"name": "L'Oreal",                  "domain": "loreal.com",          "industry": "Beauty / Consumer Goods",               "email_pattern": "first.last"},
    {"name": "Mondelez",                 "domain": "mondelez.com",        "industry": "Consumer Goods / Food & Snacks",        "email_pattern": "first.last"},
    {"name": "Thermo Fisher Scientific", "domain": "thermofisher.com",    "industry": "Life Sciences / Lab Equipment",         "email_pattern": "first.last"},
    {"name": "NBA",                      "domain": "nba.com",             "industry": "Sports / Media / Entertainment",        "email_pattern": "first.last"},
    {"name": "Duolingo",                 "domain": "duolingo.com",        "industry": "EdTech / Consumer App",                 "email_pattern": "first.last"},
    {"name": "eBay",                     "domain": "ebay.com",            "industry": "E-Commerce / Marketplace",              "email_pattern": "first.last"},
    {"name": "Lyft",                     "domain": "lyft.com",            "industry": "Rideshare / Mobility Tech",             "email_pattern": "first.last"},
    {"name": "Pinterest",                "domain": "pinterest.com",       "industry": "Social Media / Visual Discovery",       "email_pattern": "first.last"},
    {"name": "Shopify",                  "domain": "shopify.com",         "industry": "E-Commerce Platform / SaaS",            "email_pattern": "first.last"},
    {"name": "HubSpot",                  "domain": "hubspot.com",         "industry": "CRM / Marketing SaaS",                  "email_pattern": "first.last"},
    {"name": "Cloudflare",               "domain": "cloudflare.com",      "industry": "Network Security / CDN / Infrastructure","email_pattern": "first.last"},
    {"name": "Palo Alto Networks",       "domain": "paloaltonetworks.com","industry": "Cybersecurity / Enterprise Security",   "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Gmail Batch 1 - June 2026"
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
            conn.execute(
                "INSERT INTO companies (id,name,domain,industry,email_pattern,email_pattern_confidence) VALUES (?,?,?,?,?,?)",
                (new_id(), c["name"], c["domain"], c["industry"], c["email_pattern"], 70.0)
            )
            print(f"  [+] {c['name']}")
        except Exception as e:
            print(f"  [=] {c['name']} already exists" if "UNIQUE" in str(e).upper() else f"  [!] {e}")

print("\n" + "="*60); print("STEP 2: Ingesting fresh profiles"); print("="*60)

# Slack
print("Slack:", ingest_profiles("Slack", [
    {"title": "Denise Dresser - CEO - Slack | LinkedIn",                          "url": "https://www.linkedin.com/in/denisedresser/"},
    {"title": "Brian Elliott - SVP and GM - Slack | LinkedIn",                    "url": "https://www.linkedin.com/in/briandelliott/"},
    {"title": "Jonathan Prince - VP Communications and Policy - Slack | LinkedIn","url": "https://www.linkedin.com/in/jonathan-prince/"},
    {"title": "Ali Rayl - VP Customer Experience - Slack | LinkedIn",             "url": "https://www.linkedin.com/in/alirayl/"},
    {"title": "Noah Weiss - Chief Product Officer - Slack | LinkedIn",            "url": "https://www.linkedin.com/in/noahweiss/"},
    {"title": "Brad Armstrong - VP Legal - Slack | LinkedIn",                     "url": "https://www.linkedin.com/in/brad-armstrong-slack/"},
    {"title": "Tamar Yehoshua - Chief Product Officer - Slack | LinkedIn",        "url": "https://www.linkedin.com/in/tamaryehoshua/"},
    {"title": "Sarah Friar - Former CFO - Slack | LinkedIn",                      "url": "https://www.linkedin.com/in/sarahfriar/"},
    {"title": "April Underwood - VP Product - Slack | LinkedIn",                  "url": "https://www.linkedin.com/in/aprilunderwood/"},
    {"title": "Robert Frati - Chief Sales and Marketing Officer - Slack | LinkedIn","url": "https://www.linkedin.com/in/robert-frati/"},
], min_required=3, max_keep=10))

# Atlassian
print("Atlassian:", ingest_profiles("Atlassian", [
    {"title": "Mike Cannon-Brookes - CEO - Atlassian | LinkedIn",                 "url": "https://www.linkedin.com/in/mike-cannon-brookes/"},
    {"title": "Scott Farquhar - Co-CEO - Atlassian | LinkedIn",                   "url": "https://www.linkedin.com/in/scottfarquhar/"},
    {"title": "Cameron Deatsch - Chief Revenue Officer - Atlassian | LinkedIn",   "url": "https://www.linkedin.com/in/camerondeatsch/"},
    {"title": "Anu Bharadwaj - President - Atlassian | LinkedIn",                 "url": "https://www.linkedin.com/in/anubharadwaj/"},
    {"title": "Andrew Donalds - CFO - Atlassian | LinkedIn",                      "url": "https://www.linkedin.com/in/andrewdonalds/"},
    {"title": "Joff Redfern - Chief Product Officer - Atlassian | LinkedIn",      "url": "https://www.linkedin.com/in/joffredfern/"},
    {"title": "Erika Trautman - VP Product - Atlassian | LinkedIn",               "url": "https://www.linkedin.com/in/erikatrautman/"},
    {"title": "Saket Saurabh - VP Engineering - Atlassian | LinkedIn",            "url": "https://www.linkedin.com/in/saketsaurabh/"},
    {"title": "Avani Prabhakar - Chief People Officer - Atlassian | LinkedIn",    "url": "https://www.linkedin.com/in/avaniprabhakar/"},
    {"title": "Mark Cruth - Principal Work Futurist - Atlassian | LinkedIn",      "url": "https://www.linkedin.com/in/markcruth/"},
], min_required=3, max_keep=10))

# Replit
print("Replit:", ingest_profiles("Replit", [
    {"title": "Amjad Masad - CEO - Replit | LinkedIn",                            "url": "https://www.linkedin.com/in/amasad/"},
    {"title": "Haya Odeh - Co-founder and COO - Replit | LinkedIn",               "url": "https://www.linkedin.com/in/hayaodeh/"},
    {"title": "Michele Catasta - VP AI - Replit | LinkedIn",                      "url": "https://www.linkedin.com/in/pirroh/"},
    {"title": "Faris Masad - Head of Growth - Replit | LinkedIn",                 "url": "https://www.linkedin.com/in/faris-masad/"},
    {"title": "David Hershey - VP Engineering - Replit | LinkedIn",               "url": "https://www.linkedin.com/in/david-hershey/"},
    {"title": "Barron Webster - Head of Design - Replit | LinkedIn",              "url": "https://www.linkedin.com/in/barron-webster/"},
    {"title": "Connor Brewster - Head of Infrastructure - Replit | LinkedIn",     "url": "https://www.linkedin.com/in/connor-brewster/"},
    {"title": "Talor Browne - Head of Marketing - Replit | LinkedIn",             "url": "https://www.linkedin.com/in/talor-browne/"},
    {"title": "Matt Iselin - Head of Partnerships - Replit | LinkedIn",           "url": "https://www.linkedin.com/in/mattiselin/"},
    {"title": "Lena Ye - Head of Product - Replit | LinkedIn",                    "url": "https://www.linkedin.com/in/lenaye/"},
], min_required=3, max_keep=10))

# L'Oreal
print("L'Oreal:", ingest_profiles("L'Oreal", [
    {"title": "Nicolas Hieronimus - CEO - L'Oreal | LinkedIn",                    "url": "https://www.linkedin.com/in/nicolas-hieronimus/"},
    {"title": "Barbara Lavernos - Deputy CEO - L'Oreal | LinkedIn",               "url": "https://www.linkedin.com/in/barbara-lavernos/"},
    {"title": "Alexis Perakis-Valat - President Consumer Products - L'Oreal | LinkedIn","url": "https://www.linkedin.com/in/alexis-perakis-valat/"},
    {"title": "Stephane Rinderknech - President L'Oreal USA | LinkedIn",          "url": "https://www.linkedin.com/in/stephanerinderknech/"},
    {"title": "Nathalie Roos - President Professional Products - L'Oreal | LinkedIn","url": "https://www.linkedin.com/in/nathalie-roos/"},
    {"title": "Delphine Viguier-Hovasse - President L'Oreal Paris | LinkedIn",    "url": "https://www.linkedin.com/in/delphineviguierhovasse/"},
    {"title": "Vianney Derville - President Europe Zone - L'Oreal | LinkedIn",    "url": "https://www.linkedin.com/in/vianneyderville/"},
    {"title": "Asmita Dubey - Chief Digital and Marketing Officer - L'Oreal | LinkedIn","url": "https://www.linkedin.com/in/asmita-dubey/"},
    {"title": "Carol Hamilton - Group President L'Oreal USA | LinkedIn",          "url": "https://www.linkedin.com/in/carol-hamilton-loreal/"},
    {"title": "David Greenberg - President L'Oreal USA Consumer Products | LinkedIn","url": "https://www.linkedin.com/in/david-greenberg-loreal/"},
], min_required=3, max_keep=10))

# Mondelez
print("Mondelez:", ingest_profiles("Mondelez", [
    {"title": "Dirk Van de Put - Chairman and CEO - Mondelez | LinkedIn",          "url": "https://www.linkedin.com/in/dirk-van-de-put/"},
    {"title": "Luca Zaramella - CFO - Mondelez | LinkedIn",                        "url": "https://www.linkedin.com/in/lucazaramella/"},
    {"title": "Maurizio Brusadelli - EVP APAC MEA - Mondelez | LinkedIn",          "url": "https://www.linkedin.com/in/maurizio-brusadelli/"},
    {"title": "Glen Walter - EVP North America - Mondelez | LinkedIn",             "url": "https://www.linkedin.com/in/glen-walter-mondelez/"},
    {"title": "Gustavo Valle - EVP Latin America - Mondelez | LinkedIn",           "url": "https://www.linkedin.com/in/gustavo-valle-mondelez/"},
    {"title": "Vinzenz Gruber - EVP Europe - Mondelez | LinkedIn",                 "url": "https://www.linkedin.com/in/vinzenz-gruber/"},
    {"title": "Laura Helper-Ferris - VP Strategy - Mondelez | LinkedIn",           "url": "https://www.linkedin.com/in/laura-helper-ferris/"},
    {"title": "Martin Renaud - Chief Marketing Officer - Mondelez | LinkedIn",     "url": "https://www.linkedin.com/in/martinrenaud/"},
    {"title": "Sandra MacQuillan - Chief Supply Chain Officer - Mondelez | LinkedIn","url": "https://www.linkedin.com/in/sandramacquillan/"},
    {"title": "Jonathan Adashek - Chief Communications Officer - Mondelez | LinkedIn","url": "https://www.linkedin.com/in/jonathanadashek/"},
], min_required=3, max_keep=10))

# Thermo Fisher Scientific
print("Thermo Fisher Scientific:", ingest_profiles("Thermo Fisher Scientific", [
    {"title": "Marc Casper - Chairman President and CEO - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/marc-casper/"},
    {"title": "Stephen Williamson - SVP and CFO - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/stephen-williamson-tmo/"},
    {"title": "Michel Lagarde - EVP and Chief Operating Officer - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/michel-lagarde-tmo/"},
    {"title": "Fred Lowenbraun - EVP Chief Commercial Officer - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/fred-lowenbraun/"},
    {"title": "Gianluca Pettiti - SVP Life Sciences - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/gianluca-pettiti/"},
    {"title": "Lisa Bicker - VP Human Resources Americas - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/lisa-bicker/"},
    {"title": "Peter Hornstra - VP Global Marketing - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/peter-hornstra/"},
    {"title": "Sanjiv Bhatt - VP Strategy - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/sanjiv-bhatt-tmo/"},
    {"title": "Rebecca Scheuneman - VP Investor Relations - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/rebeccascheuneman/"},
    {"title": "Brenda Furlow - VP Associate General Counsel - Thermo Fisher Scientific | LinkedIn","url": "https://www.linkedin.com/in/brendafurlow/"},
], min_required=3, max_keep=10))

# NBA
print("NBA:", ingest_profiles("NBA", [
    {"title": "Adam Silver - Commissioner - NBA | LinkedIn",                       "url": "https://www.linkedin.com/in/adam-silver-nba/"},
    {"title": "Mark Tatum - Deputy Commissioner - NBA | LinkedIn",                 "url": "https://www.linkedin.com/in/mark-tatum/"},
    {"title": "Chris Paul - VP Operations - NBA | LinkedIn",                       "url": "https://www.linkedin.com/in/chris-paul-nba/"},
    {"title": "Kathy Behrens - President Social Responsibility - NBA | LinkedIn",  "url": "https://www.linkedin.com/in/kathy-behrens/"},
    {"title": "Kerry Tatlock - EVP Chief Marketing Officer - NBA | LinkedIn",      "url": "https://www.linkedin.com/in/kerry-tatlock/"},
    {"title": "Dan Rossomondo - VP Media Strategy - NBA | LinkedIn",               "url": "https://www.linkedin.com/in/danrossomondo/"},
    {"title": "Pamela El - Chief Marketing Officer - NBA | LinkedIn",              "url": "https://www.linkedin.com/in/pamelaelnba/"},
    {"title": "David Denenberg - VP Strategy and Innovation - NBA | LinkedIn",     "url": "https://www.linkedin.com/in/daviddenenberg/"},
    {"title": "Jeff Thomas - VP Partnerships - NBA | LinkedIn",                    "url": "https://www.linkedin.com/in/jeff-thomas-nba/"},
    {"title": "Naz Long - VP Player Engagement - NBA | LinkedIn",                  "url": "https://www.linkedin.com/in/naz-long/"},
], min_required=3, max_keep=10))

# Duolingo
print("Duolingo:", ingest_profiles("Duolingo", [
    {"title": "Luis von Ahn - CEO - Duolingo | LinkedIn",                          "url": "https://www.linkedin.com/in/luisvonahn/"},
    {"title": "Matthew Rubinstein - CTO - Duolingo | LinkedIn",                    "url": "https://www.linkedin.com/in/matthewrubinstein/"},
    {"title": "Cem Kansu - Chief Product Officer - Duolingo | LinkedIn",           "url": "https://www.linkedin.com/in/cemkansu/"},
    {"title": "Severin Hacker - Co-founder and CTO Emeritus - Duolingo | LinkedIn","url": "https://www.linkedin.com/in/severinhacker/"},
    {"title": "Kara McWilliams - VP People - Duolingo | LinkedIn",                 "url": "https://www.linkedin.com/in/kara-mcwilliams/"},
    {"title": "Zaria Parveen - VP Marketing - Duolingo | LinkedIn",                "url": "https://www.linkedin.com/in/zaria-parveen/"},
    {"title": "Michael Uhl - VP Revenue - Duolingo | LinkedIn",                    "url": "https://www.linkedin.com/in/michaeluhl/"},
    {"title": "Bob Meese - Chief Business Officer - Duolingo | LinkedIn",          "url": "https://www.linkedin.com/in/bobmeese/"},
    {"title": "Nate Uy - Director of Product - Duolingo | LinkedIn",               "url": "https://www.linkedin.com/in/nateuy/"},
    {"title": "Jackson Shuttleworth - Director Growth - Duolingo | LinkedIn",      "url": "https://www.linkedin.com/in/jackson-shuttleworth/"},
], min_required=3, max_keep=10))

# eBay
print("eBay:", ingest_profiles("eBay", [
    {"title": "Jamie Iannone - President and CEO - eBay | LinkedIn",               "url": "https://www.linkedin.com/in/jamieiannone/"},
    {"title": "Steve Priest - CFO - eBay | LinkedIn",                              "url": "https://www.linkedin.com/in/steve-priest-ebay/"},
    {"title": "Jordan Sweetnam - SVP General Manager Americas - eBay | LinkedIn",  "url": "https://www.linkedin.com/in/jordansweetnam/"},
    {"title": "Cornelius Boone - Chief People Officer - eBay | LinkedIn",          "url": "https://www.linkedin.com/in/corneliusboone/"},
    {"title": "Dawn Britt - SVP General Manager Europe - eBay | LinkedIn",         "url": "https://www.linkedin.com/in/dawn-britt/"},
    {"title": "Victor Iannello - Chief Technical Officer - eBay | LinkedIn",       "url": "https://www.linkedin.com/in/victoriannello/"},
    {"title": "Alyssa Simpson Rochwerger - VP AI and Data - eBay | LinkedIn",      "url": "https://www.linkedin.com/in/alyssasimpsonrochwerger/"},
    {"title": "Joele Frank - VP Communications - eBay | LinkedIn",                 "url": "https://www.linkedin.com/in/joele-frank/"},
    {"title": "Peter Thompson - VP Product Management - eBay | LinkedIn",          "url": "https://www.linkedin.com/in/peter-thompson-ebay/"},
    {"title": "Andrea Stairs - VP and Managing Director Canada - eBay | LinkedIn", "url": "https://www.linkedin.com/in/andreastairs/"},
], min_required=3, max_keep=10))

# Lyft
print("Lyft:", ingest_profiles("Lyft", [
    {"title": "David Risher - CEO - Lyft | LinkedIn",                              "url": "https://www.linkedin.com/in/davidrisher/"},
    {"title": "Erin Brewer - CFO - Lyft | LinkedIn",                               "url": "https://www.linkedin.com/in/erin-brewer-lyft/"},
    {"title": "Kristin Sverchek - President - Lyft | LinkedIn",                    "url": "https://www.linkedin.com/in/kristinsverchek/"},
    {"title": "Melissa Waters - Chief Marketing Officer - Lyft | LinkedIn",        "url": "https://www.linkedin.com/in/melissawaters/"},
    {"title": "Ashwin Raj - VP Engineering - Lyft | LinkedIn",                     "url": "https://www.linkedin.com/in/ashwin-raj-lyft/"},
    {"title": "Matt Kallman - VP Communications - Lyft | LinkedIn",                "url": "https://www.linkedin.com/in/mattkallman/"},
    {"title": "Rohan Bhobe - VP Product - Lyft | LinkedIn",                        "url": "https://www.linkedin.com/in/rohanbhobe/"},
    {"title": "Faye Thieman - Chief People Officer - Lyft | LinkedIn",             "url": "https://www.linkedin.com/in/fayethieman/"},
    {"title": "Ishaan Bhola - VP Strategy - Lyft | LinkedIn",                      "url": "https://www.linkedin.com/in/ishaanbhola/"},
    {"title": "Joao Machado - VP Driver Experience - Lyft | LinkedIn",             "url": "https://www.linkedin.com/in/joao-machado-lyft/"},
], min_required=3, max_keep=10))

# Pinterest
print("Pinterest:", ingest_profiles("Pinterest", [
    {"title": "Bill Ready - CEO - Pinterest | LinkedIn",                           "url": "https://www.linkedin.com/in/billready/"},
    {"title": "Julia Donnelly - CFO - Pinterest | LinkedIn",                       "url": "https://www.linkedin.com/in/juliadonnelly/"},
    {"title": "Andrei Hagiu - Chief Strategy Officer - Pinterest | LinkedIn",      "url": "https://www.linkedin.com/in/andreihagiu/"},
    {"title": "Sabrina Ellis - Chief Product Officer - Pinterest | LinkedIn",      "url": "https://www.linkedin.com/in/sabrinaellis/"},
    {"title": "Malik Ducard - Chief Content Officer - Pinterest | LinkedIn",       "url": "https://www.linkedin.com/in/malikducard/"},
    {"title": "Naveen Gavini - Chief Revenue Officer - Pinterest | LinkedIn",      "url": "https://www.linkedin.com/in/naveengavini/"},
    {"title": "Jon Kaplan - Chief Revenue Officer - Pinterest | LinkedIn",         "url": "https://www.linkedin.com/in/jonkaplan/"},
    {"title": "Katie Clow - VP Marketing - Pinterest | LinkedIn",                  "url": "https://www.linkedin.com/in/katieclow/"},
    {"title": "Pam Kaufman - Chief Marketing Officer - Pinterest | LinkedIn",      "url": "https://www.linkedin.com/in/pamkaufman/"},
    {"title": "Cristina Schreib - VP People - Pinterest | LinkedIn",               "url": "https://www.linkedin.com/in/cristinaschreib/"},
], min_required=3, max_keep=10))

# Shopify
print("Shopify:", ingest_profiles("Shopify", [
    {"title": "Tobi Lutke - CEO - Shopify | LinkedIn",                             "url": "https://www.linkedin.com/in/tobiaslutke/"},
    {"title": "Harley Finkelstein - President - Shopify | LinkedIn",               "url": "https://www.linkedin.com/in/harleyf/"},
    {"title": "Jeff Hoffmeister - CFO - Shopify | LinkedIn",                       "url": "https://www.linkedin.com/in/jeffhoffmeister/"},
    {"title": "Bobby Morrison - Chief Revenue Officer - Shopify | LinkedIn",       "url": "https://www.linkedin.com/in/bobby-morrison/"},
    {"title": "Kaz Nejatian - VP Product and COO - Shopify | LinkedIn",            "url": "https://www.linkedin.com/in/kaznejatian/"},
    {"title": "Glen Coates - VP Product - Shopify | LinkedIn",                     "url": "https://www.linkedin.com/in/glencoates/"},
    {"title": "Carl Rivera - VP Merchant Experience - Shopify | LinkedIn",         "url": "https://www.linkedin.com/in/carlrivera/"},
    {"title": "Loren Padelford - VP Enterprise - Shopify | LinkedIn",              "url": "https://www.linkedin.com/in/lorenpadelford/"},
    {"title": "Christopher Nolan - Chief Legal Officer - Shopify | LinkedIn",      "url": "https://www.linkedin.com/in/christopher-nolan-shopify/"},
    {"title": "Vanessa Lee - VP Talent - Shopify | LinkedIn",                      "url": "https://www.linkedin.com/in/vanessalee-shopify/"},
], min_required=3, max_keep=10))

# HubSpot
print("HubSpot:", ingest_profiles("HubSpot", [
    {"title": "Yamini Rangan - CEO - HubSpot | LinkedIn",                          "url": "https://www.linkedin.com/in/yamini-rangan/"},
    {"title": "Dharmesh Shah - Co-Founder and CTO - HubSpot | LinkedIn",           "url": "https://www.linkedin.com/in/dharmesh/"},
    {"title": "Kate Bueker - CFO - HubSpot | LinkedIn",                            "url": "https://www.linkedin.com/in/kate-bueker/"},
    {"title": "Andy Pitre - EVP Product - HubSpot | LinkedIn",                     "url": "https://www.linkedin.com/in/andypitre/"},
    {"title": "Kieran Flanagan - SVP Marketing - HubSpot | LinkedIn",              "url": "https://www.linkedin.com/in/kieranflanagan/"},
    {"title": "Alison Elworthy - EVP Customer Success - HubSpot | LinkedIn",       "url": "https://www.linkedin.com/in/alisonelworthy/"},
    {"title": "Nancy H - Chief People Officer - HubSpot | LinkedIn",               "url": "https://www.linkedin.com/in/nancy-hubspot/"},
    {"title": "Hunter Madeley - Chief Sales Officer - HubSpot | LinkedIn",         "url": "https://www.linkedin.com/in/huntermadeley/"},
    {"title": "Mark Roberge - Chief Revenue Officer Emeritus - HubSpot | LinkedIn","url": "https://www.linkedin.com/in/markroberge/"},
    {"title": "Michael Redbord - SVP Customer Platform - HubSpot | LinkedIn",      "url": "https://www.linkedin.com/in/mredbord/"},
], min_required=3, max_keep=10))

# Cloudflare
print("Cloudflare:", ingest_profiles("Cloudflare", [
    {"title": "Matthew Prince - Co-Founder and CEO - Cloudflare | LinkedIn",       "url": "https://www.linkedin.com/in/matthewprince/"},
    {"title": "Michelle Zatlyn - Co-Founder and President - Cloudflare | LinkedIn","url": "https://www.linkedin.com/in/michellezatlyn/"},
    {"title": "Thomas Seifert - CFO - Cloudflare | LinkedIn",                      "url": "https://www.linkedin.com/in/thomasseifert/"},
    {"title": "Marc Boroditsky - Chief Revenue Officer - Cloudflare | LinkedIn",   "url": "https://www.linkedin.com/in/marcboroditsky/"},
    {"title": "Jen Taylor - Chief Product Officer - Cloudflare | LinkedIn",        "url": "https://www.linkedin.com/in/jentaylor/"},
    {"title": "Dane Knecht - SVP Product - Cloudflare | LinkedIn",                 "url": "https://www.linkedin.com/in/daneknecht/"},
    {"title": "Grant Bourzikas - Chief Security Officer - Cloudflare | LinkedIn",  "url": "https://www.linkedin.com/in/grantbourzikas/"},
    {"title": "Steve Huffman - VP Engineering - Cloudflare | LinkedIn",            "url": "https://www.linkedin.com/in/steve-huffman-cloudflare/"},
    {"title": "Vanessa Larco - Board Director - Cloudflare | LinkedIn",            "url": "https://www.linkedin.com/in/vanessalarco/"},
    {"title": "Robert Blumofe - EVP Technology and CTO - Cloudflare | LinkedIn",   "url": "https://www.linkedin.com/in/rblumofe/"},
], min_required=3, max_keep=10))

# Palo Alto Networks
print("Palo Alto Networks:", ingest_profiles("Palo Alto Networks", [
    {"title": "Nikesh Arora - Chairman and CEO - Palo Alto Networks | LinkedIn",   "url": "https://www.linkedin.com/in/nikesharora/"},
    {"title": "Dipak Golechha - CFO - Palo Alto Networks | LinkedIn",              "url": "https://www.linkedin.com/in/dipak-golechha/"},
    {"title": "BJ Jenkins - President - Palo Alto Networks | LinkedIn",            "url": "https://www.linkedin.com/in/bjjenkins/"},
    {"title": "Lee Klarich - Chief Product Officer - Palo Alto Networks | LinkedIn","url": "https://www.linkedin.com/in/leeklarich/"},
    {"title": "Helmut Reisinger - CEO EMEA and LATAM - Palo Alto Networks | LinkedIn","url": "https://www.linkedin.com/in/helmutreisinger/"},
    {"title": "Simon Green - President JAPAC - Palo Alto Networks | LinkedIn",     "url": "https://www.linkedin.com/in/simon-green-panw/"},
    {"title": "Wendy Bahr - Chief Partner Officer - Palo Alto Networks | LinkedIn","url": "https://www.linkedin.com/in/wendybahr/"},
    {"title": "Liane Hornsey - Chief People Officer - Palo Alto Networks | LinkedIn","url": "https://www.linkedin.com/in/lianehornsey/"},
    {"title": "Rene Bonvanie - Former CMO - Palo Alto Networks | LinkedIn",        "url": "https://www.linkedin.com/in/renebonvanie/"},
    {"title": "Anand Oswal - SVP and GM Network Security - Palo Alto Networks | LinkedIn","url": "https://www.linkedin.com/in/anandoswal/"},
], min_required=3, max_keep=10))

# ── Available-contact summary ─────────────────────────────────────────────────
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
        print(f"  [=] Campaign exists: {campaign_id}")
    else:
        campaign_id = new_id()
        conn.execute(
            "INSERT INTO campaigns (id, name, status) VALUES (?, ?, 'active')",
            (campaign_id, CAMPAIGN_NAME)
        )
        print(f"  [+] Campaign created: {campaign_id}")

with open("CAMPAIGN_ID.txt", "w") as f:
    f.write(campaign_id)
print(f"  Campaign ID saved to CAMPAIGN_ID.txt")

# ── STEP 4: Personalize ───────────────────────────────────────────────────────
print("\n" + "="*60); print("STEP 4: Personalizing emails (1 per company, BBS template)"); print("="*60)
personalize_once_per_company(
    campaign_id=campaign_id,
    sender_value_prop=SENDER_VALUE_PROP,
    num_steps=1,
    company_domains=COMPANY_DOMAINS,
    template="bbs",
    max_contacts_per_company=10,
    exclude_contacted=True,
)

# ── STEP 5: Send via eleynxiong@gmail.com ────────────────────────────────────
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
    SELECT sr.id as sr_id, sr.step_number,
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
        delay = random.uniform(60, 90)
        time.sleep(delay)
    except Exception as e:
        total_failed += 1
        print(f"  [!] FAILED {row['primary_email']}: {e}")
        safe_exec(
            "UPDATE send_records SET status='failed',last_error=? WHERE id=?",
            (str(e), row["sr_id"])
        )

conn_s.close()

print(f"\n{'='*60}")
print(f"DONE — {total_sent} sent, {total_failed} failed")
print(f"Sender: eleynxiong@gmail.com | Campaign: {CAMPAIGN_NAME}")
print(f"{'='*60}")
