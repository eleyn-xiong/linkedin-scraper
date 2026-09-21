"""BBS Batch 9 — 25 new Fortune 500 companies, 10 emails each, eleynxiong@berkeley.edu."""
import sys, time, random, sqlite3
from schedule_utils import next_business_send_time, _PACIFIC
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
    {"name": "Devon Energy",                "domain": "devonenergy.com",        "industry": "E&P Oil and Gas / Permian Basin / Natural Gas",              "email_pattern": "first.last"},
    {"name": "Coterra Energy",              "domain": "coterra.com",            "industry": "E&P Oil and Gas / Natural Gas / Permian and Marcellus",       "email_pattern": "first.last"},
    {"name": "Diamondback Energy",          "domain": "diamondbackenergy.com",  "industry": "Permian Basin E&P / Oil and Gas / Upstream",                  "email_pattern": "first.last"},
    {"name": "TransDigm Group",             "domain": "transdigm.com",          "industry": "Aerospace Components / Defense / Proprietary Hardware",        "email_pattern": "first.last"},
    {"name": "Huntington Ingalls",          "domain": "huntingtoningalls.com",  "industry": "Naval Shipbuilding / Defense / Government Contracts",          "email_pattern": "first.last"},
    {"name": "Cincinnati Financial",        "domain": "cinfin.com",             "industry": "Property Casualty Insurance / Life Insurance / Investments",   "email_pattern": "first.last"},
    {"name": "W.R. Berkley",               "domain": "berkley.com",            "industry": "Commercial Lines Insurance / Specialty Insurance / Reinsurance","email_pattern": "first.last"},
    {"name": "Regions Financial",           "domain": "regions.com",            "industry": "Regional Banking / Consumer and Commercial Finance / Wealth",  "email_pattern": "first.last"},
    {"name": "Huntington Bancshares",       "domain": "huntington.com",         "industry": "Regional Banking / Consumer Finance / Commercial Banking",      "email_pattern": "first.last"},
    {"name": "KeyCorp",                     "domain": "key.com",                "industry": "Banking / Investment Banking / Wealth Management / Fintech",   "email_pattern": "first.last"},
    {"name": "Church and Dwight",           "domain": "churchdwight.com",       "industry": "Consumer Goods / Personal Care / Household Products",          "email_pattern": "first.last"},
    {"name": "JM Smucker",                  "domain": "jmsmucker.com",          "industry": "Food and Beverage / Coffee / Pet Food / Snacks / Brands",      "email_pattern": "first.last"},
    {"name": "Hanesbrands",                 "domain": "hanesbrands.com",        "industry": "Apparel / Innerwear / Activewear / Hosiery / Global Brands",   "email_pattern": "first.last"},
    {"name": "Five Below",                  "domain": "fivebelow.com",          "industry": "Specialty Retail / Discount / Teen and Tween / Value",         "email_pattern": "first.last"},
    {"name": "BJ's Wholesale Club",         "domain": "bjs.com",               "industry": "Wholesale Club / Membership Retail / Grocery / Gas",           "email_pattern": "first.last"},
    {"name": "Universal Health Services",   "domain": "uhs.com",               "industry": "Acute Care Hospitals / Behavioral Health / Healthcare Services","email_pattern": "first.last"},
    {"name": "Encompass Health",            "domain": "encompasshealth.com",    "industry": "Inpatient Rehabilitation / Home Health / Hospice / Post-Acute","email_pattern": "first.last"},
    {"name": "Charles River Laboratories",  "domain": "crl.com",               "industry": "Preclinical Research / Drug Discovery / Lab Testing / CRO",    "email_pattern": "first.last"},
    {"name": "Cushman and Wakefield",       "domain": "cushmanwakefield.com",   "industry": "Commercial Real Estate / Advisory / Leasing / Valuation",      "email_pattern": "first.last"},
    {"name": "XPO",                         "domain": "xpo.com",               "industry": "LTL Freight / Logistics / Transportation / Supply Chain",       "email_pattern": "first.last"},
    {"name": "Old Dominion Freight Line",   "domain": "odfl.com",              "industry": "LTL Freight Transportation / Logistics / Distribution",         "email_pattern": "first.last"},
    {"name": "FTI Consulting",              "domain": "fticonsulting.com",      "industry": "Management Consulting / Forensic / Litigation / Economics",    "email_pattern": "first.last"},
    {"name": "ManpowerGroup",               "domain": "manpowergroup.com",      "industry": "Workforce Solutions / Staffing / Talent Management / HR",      "email_pattern": "first.last"},
    {"name": "Vistra",                      "domain": "vistra.com",            "industry": "Electric Power / Energy / Retail Electricity / Nuclear",        "email_pattern": "first.last"},
    {"name": "AES Corporation",             "domain": "aes.com",               "industry": "Clean Energy / Power Generation / Utilities / Renewables",      "email_pattern": "first.last"},
]

COMPANY_DOMAINS = [c["domain"] for c in COMPANIES]
CAMPAIGN_NAME = "BBS Batch 9 - July 2026"
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

print("Devon Energy:", ingest_profiles("Devon Energy", [
    {"title": "Rick Muncrief - President and CEO - Devon Energy | LinkedIn",                        "url": "https://www.linkedin.com/in/rickmuncrief/"},
    {"title": "Jeff Ritenour - EVP and CFO - Devon Energy | LinkedIn",                             "url": "https://www.linkedin.com/in/jeffritenour-devon/"},
    {"title": "Clay Gaspar - EVP and COO - Devon Energy | LinkedIn",                               "url": "https://www.linkedin.com/in/claygaspar-devon/"},
    {"title": "Tana Cashion - SVP Human Resources - Devon Energy | LinkedIn",                      "url": "https://www.linkedin.com/in/tanacashion-devon/"},
    {"title": "Karl Pfeil - SVP Exploration - Devon Energy | LinkedIn",                            "url": "https://www.linkedin.com/in/karlpfeil-devon/"},
    {"title": "Dennis Cameron - SVP and General Counsel - Devon Energy | LinkedIn",                "url": "https://www.linkedin.com/in/denniscameron-devon/"},
    {"title": "Scott Coody - VP Investor Relations - Devon Energy | LinkedIn",                     "url": "https://www.linkedin.com/in/scottcoody-devon/"},
    {"title": "David Harris - SVP Corporate Strategy - Devon Energy | LinkedIn",                   "url": "https://www.linkedin.com/in/davidharris-devon/"},
    {"title": "Amber Wilson - SVP Marketing - Devon Energy | LinkedIn",                            "url": "https://www.linkedin.com/in/amberwilson-devon/"},
    {"title": "Lyndon Taylor - SVP Operations - Devon Energy | LinkedIn",                          "url": "https://www.linkedin.com/in/lyndontaylor-devon/"},
], min_required=3, max_keep=10))

print("Coterra Energy:", ingest_profiles("Coterra Energy", [
    {"title": "Tom Jorden - Chairman President and CEO - Coterra Energy | LinkedIn",               "url": "https://www.linkedin.com/in/tomjorden-coterra/"},
    {"title": "Shane Young - EVP and CFO - Coterra Energy | LinkedIn",                             "url": "https://www.linkedin.com/in/shaneyoung-coterra/"},
    {"title": "Blake Sirgo - SVP Operations - Coterra Energy | LinkedIn",                          "url": "https://www.linkedin.com/in/blakesirgo-coterra/"},
    {"title": "Stephen Bell - SVP General Counsel - Coterra Energy | LinkedIn",                    "url": "https://www.linkedin.com/in/stephenbell-coterra/"},
    {"title": "Dan Guffey - SVP and Chief Sustainability Officer - Coterra Energy | LinkedIn",     "url": "https://www.linkedin.com/in/danguffey-coterra/"},
    {"title": "Kevin Cannell - VP Investor Relations - Coterra Energy | LinkedIn",                 "url": "https://www.linkedin.com/in/kevincannell-coterra/"},
    {"title": "Scott Strazik - Board Member - Coterra Energy | LinkedIn",                          "url": "https://www.linkedin.com/in/scottstrazik-coterra/"},
    {"title": "Todd Rosenthal - SVP Permian Operations - Coterra Energy | LinkedIn",               "url": "https://www.linkedin.com/in/toddrosenthal-coterra/"},
    {"title": "Kim Kurtz - SVP Human Resources - Coterra Energy | LinkedIn",                       "url": "https://www.linkedin.com/in/kimkurtz-coterra/"},
    {"title": "Chris Abundis - SVP Drilling - Coterra Energy | LinkedIn",                          "url": "https://www.linkedin.com/in/chrisabundis-coterra/"},
], min_required=3, max_keep=10))

print("Diamondback Energy:", ingest_profiles("Diamondback Energy", [
    {"title": "Travis Stice - Chairman and CEO - Diamondback Energy | LinkedIn",                   "url": "https://www.linkedin.com/in/travisstice/"},
    {"title": "Kaes Van't Hof - President and CFO - Diamondback Energy | LinkedIn",               "url": "https://www.linkedin.com/in/kaesvanthof/"},
    {"title": "Danny Wesson - VP Operations - Diamondback Energy | LinkedIn",                      "url": "https://www.linkedin.com/in/dannywesson-diamondback/"},
    {"title": "Kim Sherwood - SVP and General Counsel - Diamondback Energy | LinkedIn",            "url": "https://www.linkedin.com/in/kimsherwood-diamondback/"},
    {"title": "Mike Hollis - COO - Diamondback Energy | LinkedIn",                                 "url": "https://www.linkedin.com/in/mikehollis-diamondback/"},
    {"title": "Adam Lawlis - VP Investor Relations - Diamondback Energy | LinkedIn",               "url": "https://www.linkedin.com/in/adamlawlis-diamondback/"},
    {"title": "Teresa Dick - VP and Chief Accounting Officer - Diamondback Energy | LinkedIn",     "url": "https://www.linkedin.com/in/teresadick-diamondback/"},
    {"title": "Brent White - VP Business Development - Diamondback Energy | LinkedIn",             "url": "https://www.linkedin.com/in/brentwhite-diamondback/"},
    {"title": "Cynthia Walker - VP Supply Chain - Diamondback Energy | LinkedIn",                  "url": "https://www.linkedin.com/in/cynthiawalker-diamondback/"},
    {"title": "Scott Reasoner - VP Exploration - Diamondback Energy | LinkedIn",                   "url": "https://www.linkedin.com/in/scottreasoner-diamondback/"},
], min_required=3, max_keep=10))

print("TransDigm Group:", ingest_profiles("TransDigm Group", [
    {"title": "Kevin Stein - President and CEO - TransDigm Group | LinkedIn",                      "url": "https://www.linkedin.com/in/kevinstein-transdigm/"},
    {"title": "Sarah Wynne - CFO - TransDigm Group | LinkedIn",                                    "url": "https://www.linkedin.com/in/sarahwynne-transdigm/"},
    {"title": "Mike Lisman - EVP Operations - TransDigm Group | LinkedIn",                         "url": "https://www.linkedin.com/in/mikelisman-transdigm/"},
    {"title": "Liza Sabol - VP Investor Relations - TransDigm Group | LinkedIn",                   "url": "https://www.linkedin.com/in/lizasabol-transdigm/"},
    {"title": "Joel Turner - EVP Strategic Sourcing - TransDigm Group | LinkedIn",                 "url": "https://www.linkedin.com/in/joelturner-transdigm/"},
    {"title": "Robert Henderson - VP and General Counsel - TransDigm Group | LinkedIn",            "url": "https://www.linkedin.com/in/roberthenderson-transdigm/"},
    {"title": "Christine Harris - VP Human Resources - TransDigm Group | LinkedIn",                "url": "https://www.linkedin.com/in/christineharris-transdigm/"},
    {"title": "Jorge Valladares - VP Business Development - TransDigm Group | LinkedIn",           "url": "https://www.linkedin.com/in/jorgevalladares-transdigm/"},
    {"title": "Nick Howley - Executive Chairman - TransDigm Group | LinkedIn",                     "url": "https://www.linkedin.com/in/nickhowley-transdigm/"},
    {"title": "Scott Krasting - VP Finance - TransDigm Group | LinkedIn",                          "url": "https://www.linkedin.com/in/scottkrasting-transdigm/"},
], min_required=3, max_keep=10))

print("Huntington Ingalls:", ingest_profiles("Huntington Ingalls", [
    {"title": "Christopher Kastner - President and CEO - Huntington Ingalls Industries | LinkedIn","url": "https://www.linkedin.com/in/christopherkastner-hii/"},
    {"title": "Tom Stiehle - EVP and CFO - Huntington Ingalls Industries | LinkedIn",              "url": "https://www.linkedin.com/in/tomstiehle-hii/"},
    {"title": "Kari Wilkinson - EVP and President Newport News - Huntington Ingalls | LinkedIn",   "url": "https://www.linkedin.com/in/kariwilkinson-hii/"},
    {"title": "Charles Southall - EVP and President Ingalls Shipbuilding - HII | LinkedIn",        "url": "https://www.linkedin.com/in/charlessouthall-hii/"},
    {"title": "Andy Green - EVP and President Mission Technologies - HII | LinkedIn",              "url": "https://www.linkedin.com/in/andygreen-hii/"},
    {"title": "Brian Blanton - SVP and General Counsel - Huntington Ingalls | LinkedIn",           "url": "https://www.linkedin.com/in/brianblanton-hii/"},
    {"title": "Joanne Pinderhughes - SVP Communications - Huntington Ingalls | LinkedIn",         "url": "https://www.linkedin.com/in/joannepinderhughes-hii/"},
    {"title": "Jennifer Boykin - SVP Ship Repair - Huntington Ingalls | LinkedIn",                 "url": "https://www.linkedin.com/in/jenniferboykin-hii/"},
    {"title": "Cynthia Trevino - VP Government Relations - Huntington Ingalls | LinkedIn",         "url": "https://www.linkedin.com/in/cynthiatrevino-hii/"},
    {"title": "Deon Johnson - SVP Human Resources - Huntington Ingalls | LinkedIn",                "url": "https://www.linkedin.com/in/deonjohnson-hii/"},
], min_required=3, max_keep=10))

print("Cincinnati Financial:", ingest_profiles("Cincinnati Financial", [
    {"title": "Steve Johnston - Chairman President and CEO - Cincinnati Financial | LinkedIn",      "url": "https://www.linkedin.com/in/stevejohnston-cinf/"},
    {"title": "Mike Sewell - SVP and CFO - Cincinnati Financial | LinkedIn",                       "url": "https://www.linkedin.com/in/mikesewell-cinf/"},
    {"title": "Mark Bardwell - SVP Personal Lines - Cincinnati Financial | LinkedIn",              "url": "https://www.linkedin.com/in/markbardwell-cinf/"},
    {"title": "Marc Schambow - SVP Commercial Lines - Cincinnati Financial | LinkedIn",            "url": "https://www.linkedin.com/in/marcschambow-cinf/"},
    {"title": "Lisa Love - SVP Life Insurance - Cincinnati Financial | LinkedIn",                  "url": "https://www.linkedin.com/in/lisalove-cinf/"},
    {"title": "J.F. Scherer - EVP Sales and Marketing - Cincinnati Financial | LinkedIn",          "url": "https://www.linkedin.com/in/jfscherer-cinf/"},
    {"title": "Todd Bault - VP Investor Relations - Cincinnati Financial | LinkedIn",              "url": "https://www.linkedin.com/in/toddbault-cinf/"},
    {"title": "Theresa Hoffer - SVP Chief HR Officer - Cincinnati Financial | LinkedIn",            "url": "https://www.linkedin.com/in/theresahoffer-cinf/"},
    {"title": "Skip Sander - SVP Corporate Claims - Cincinnati Financial | LinkedIn",              "url": "https://www.linkedin.com/in/skipsander-cinf/"},
    {"title": "Martin Hollenbeck - VP Investment Management - Cincinnati Financial | LinkedIn",    "url": "https://www.linkedin.com/in/martinhollenbeck-cinf/"},
], min_required=3, max_keep=10))

print("W.R. Berkley:", ingest_profiles("W.R. Berkley", [
    {"title": "William Berkley - Executive Chairman - W.R. Berkley Corporation | LinkedIn",        "url": "https://www.linkedin.com/in/williamberkley/"},
    {"title": "Rob Berkley - President and CEO - W.R. Berkley Corporation | LinkedIn",             "url": "https://www.linkedin.com/in/robb-berkley/"},
    {"title": "Rich Baio - EVP and CFO - W.R. Berkley Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/richbaio-wrberkley/"},
    {"title": "Thomas O'Brien - EVP - W.R. Berkley Corporation | LinkedIn",                       "url": "https://www.linkedin.com/in/thomasobrien-wrberkley/"},
    {"title": "Ira Lederman - SVP General Counsel - W.R. Berkley Corporation | LinkedIn",         "url": "https://www.linkedin.com/in/iralederman-wrberkley/"},
    {"title": "James Shiel - EVP International - W.R. Berkley Corporation | LinkedIn",            "url": "https://www.linkedin.com/in/jamesshiel-wrberkley/"},
    {"title": "Karen Horvath - VP Investor Relations - W.R. Berkley Corporation | LinkedIn",      "url": "https://www.linkedin.com/in/karenhorvath-wrberkley/"},
    {"title": "Eugene Ballard - SVP Finance - W.R. Berkley Corporation | LinkedIn",               "url": "https://www.linkedin.com/in/eugeneballard-wrberkley/"},
    {"title": "David Hwang - SVP Specialty Insurance - W.R. Berkley | LinkedIn",                   "url": "https://www.linkedin.com/in/davidhwang-wrberkley/"},
    {"title": "Adrian Colosimo - SVP Reinsurance - W.R. Berkley | LinkedIn",                       "url": "https://www.linkedin.com/in/adriancolosimo-wrberkley/"},
], min_required=3, max_keep=10))

print("Regions Financial:", ingest_profiles("Regions Financial", [
    {"title": "John Turner - Chairman President and CEO - Regions Financial | LinkedIn",           "url": "https://www.linkedin.com/in/johnturner-regions/"},
    {"title": "David Turner - EVP and CFO - Regions Financial | LinkedIn",                         "url": "https://www.linkedin.com/in/davidturner-regions/"},
    {"title": "Kate Danella - EVP Consumer Banking - Regions Financial | LinkedIn",                "url": "https://www.linkedin.com/in/katedanella-regions/"},
    {"title": "Clay Nix - EVP Head of Private Wealth - Regions Financial | LinkedIn",              "url": "https://www.linkedin.com/in/claynix-regions/"},
    {"title": "Chris Grimes - EVP and Chief Risk Officer - Regions Financial | LinkedIn",          "url": "https://www.linkedin.com/in/chrisgrimes-regions/"},
    {"title": "Bill Cimino - EVP and General Counsel - Regions Financial | LinkedIn",              "url": "https://www.linkedin.com/in/billcimino-regions/"},
    {"title": "Kathy Mazzarella - EVP Chief HR Officer - Regions Financial | LinkedIn",            "url": "https://www.linkedin.com/in/kathymazzarella-regions/"},
    {"title": "Dana Nolan - EVP Technology and Operations - Regions Financial | LinkedIn",         "url": "https://www.linkedin.com/in/dananolan-regions/"},
    {"title": "Dana Elmore - EVP and Chief Marketing Officer - Regions Financial | LinkedIn",      "url": "https://www.linkedin.com/in/danaelmore-regions/"},
    {"title": "Dana Chestang - EVP Corporate Banking - Regions Financial | LinkedIn",              "url": "https://www.linkedin.com/in/danachestang-regions/"},
], min_required=3, max_keep=10))

print("Huntington Bancshares:", ingest_profiles("Huntington Bancshares", [
    {"title": "Steve Steinour - Chairman President and CEO - Huntington Bancshares | LinkedIn",    "url": "https://www.linkedin.com/in/stevesteinour/"},
    {"title": "Zach Wasserman - EVP and CFO - Huntington Bancshares | LinkedIn",                   "url": "https://www.linkedin.com/in/zachwasserman-huntington/"},
    {"title": "Andy Harmening - Former President - Huntington Bancshares | LinkedIn",              "url": "https://www.linkedin.com/in/andyharmening/"},
    {"title": "Jana Litsey - EVP Chief Risk Officer - Huntington Bancshares | LinkedIn",           "url": "https://www.linkedin.com/in/janalitsey-huntington/"},
    {"title": "Helga Houston - EVP Chief Technology Officer - Huntington Bancshares | LinkedIn",   "url": "https://www.linkedin.com/in/helgahouston-huntington/"},
    {"title": "David Medina - EVP and General Counsel - Huntington Bancshares | LinkedIn",         "url": "https://www.linkedin.com/in/davidmedina-huntington/"},
    {"title": "Brant Standridge - EVP Consumer and Regional Banking - Huntington | LinkedIn",      "url": "https://www.linkedin.com/in/brantstandridge-huntington/"},
    {"title": "Scott Kleinman - EVP Commercial Banking - Huntington Bancshares | LinkedIn",        "url": "https://www.linkedin.com/in/scottkleinman-huntington/"},
    {"title": "Sandra Bell - EVP Chief HR Officer - Huntington Bancshares | LinkedIn",             "url": "https://www.linkedin.com/in/sandrabell-huntington/"},
    {"title": "Tim Sedabres - SVP Investor Relations - Huntington Bancshares | LinkedIn",          "url": "https://www.linkedin.com/in/timsedabres-huntington/"},
], min_required=3, max_keep=10))

print("KeyCorp:", ingest_profiles("KeyCorp", [
    {"title": "Chris Gorman - Chairman and CEO - KeyCorp | LinkedIn",                              "url": "https://www.linkedin.com/in/chrisgorman-keycorp/"},
    {"title": "Clark Khayat - EVP and CFO - KeyCorp | LinkedIn",                                   "url": "https://www.linkedin.com/in/clarkkhayat-keycorp/"},
    {"title": "Ken Gavrity - EVP Head of Enterprise Payments - KeyCorp | LinkedIn",                "url": "https://www.linkedin.com/in/kengavrity-keycorp/"},
    {"title": "Andy Briggs - EVP Consumer Bank - KeyCorp | LinkedIn",                              "url": "https://www.linkedin.com/in/andybriggs-keycorp/"},
    {"title": "David Harnisch - EVP Commercial Bank - KeyCorp | LinkedIn",                         "url": "https://www.linkedin.com/in/davidharnisch-keycorp/"},
    {"title": "Amy Brady - Chief Information Officer - KeyCorp | LinkedIn",                        "url": "https://www.linkedin.com/in/amybrady-keycorp/"},
    {"title": "Trina Evans - EVP Chief HR Officer - KeyCorp | LinkedIn",                           "url": "https://www.linkedin.com/in/trinaevans-keycorp/"},
    {"title": "Jamie Warder - EVP Head of Digital Banking - KeyCorp | LinkedIn",                   "url": "https://www.linkedin.com/in/jamiewarder-keycorp/"},
    {"title": "Brian Mooney - EVP Corporate Responsibility - KeyCorp | LinkedIn",                  "url": "https://www.linkedin.com/in/brianmooney-keycorp/"},
    {"title": "Vern Patterson - VP Investor Relations - KeyCorp | LinkedIn",                       "url": "https://www.linkedin.com/in/vernpatterson-keycorp/"},
], min_required=3, max_keep=10))

print("Church and Dwight:", ingest_profiles("Church and Dwight", [
    {"title": "Matt Farrell - CEO - Church and Dwight | LinkedIn",                                 "url": "https://www.linkedin.com/in/matthewfarrell-cd/"},
    {"title": "Rick Dierker - EVP and CFO - Church and Dwight | LinkedIn",                         "url": "https://www.linkedin.com/in/rickdierker-cd/"},
    {"title": "Britta Bomhard - EVP and Chief Marketing Officer - Church and Dwight | LinkedIn",   "url": "https://www.linkedin.com/in/brittabomhard-cd/"},
    {"title": "Patrick de Maynadier - EVP and General Counsel - Church and Dwight | LinkedIn",    "url": "https://www.linkedin.com/in/patrickdemaynadier-cd/"},
    {"title": "Louis Tursi - EVP Sales - Church and Dwight | LinkedIn",                            "url": "https://www.linkedin.com/in/louistursi-cd/"},
    {"title": "Barry Bruno - EVP Chief HR Officer - Church and Dwight | LinkedIn",                 "url": "https://www.linkedin.com/in/barrybruno-cd/"},
    {"title": "Aaron Berlin - EVP Chief Information Officer - Church and Dwight | LinkedIn",       "url": "https://www.linkedin.com/in/aaronberlin-cd/"},
    {"title": "Steven Linares - EVP Research and Development - Church and Dwight | LinkedIn",     "url": "https://www.linkedin.com/in/stevenlinares-cd/"},
    {"title": "Brett Seifried - EVP Operations - Church and Dwight | LinkedIn",                   "url": "https://www.linkedin.com/in/brettseifried-cd/"},
    {"title": "Mark Conish - VP Investor Relations - Church and Dwight | LinkedIn",               "url": "https://www.linkedin.com/in/markconish-cd/"},
], min_required=3, max_keep=10))

print("JM Smucker:", ingest_profiles("JM Smucker", [
    {"title": "Mark Smucker - President and CEO - JM Smucker Company | LinkedIn",                 "url": "https://www.linkedin.com/in/marksmucker/"},
    {"title": "Tucker Marshall - SVP and CFO - JM Smucker Company | LinkedIn",                    "url": "https://www.linkedin.com/in/tuckermarshall-smucker/"},
    {"title": "Gina Carey - Chief Revenue Officer - JM Smucker Company | LinkedIn",               "url": "https://www.linkedin.com/in/ginacarey-smucker/"},
    {"title": "Jeannette Marcos - Chief Marketing Officer - JM Smucker Company | LinkedIn",       "url": "https://www.linkedin.com/in/jeannetteMarcos-smucker/"},
    {"title": "Tina Floyd - Chief People Officer - JM Smucker Company | LinkedIn",                "url": "https://www.linkedin.com/in/tinafloyd-smucker/"},
    {"title": "Geoff Tanner - Chief Commercial Officer - JM Smucker Company | LinkedIn",          "url": "https://www.linkedin.com/in/geofftanner-smucker/"},
    {"title": "John Donahue - General Counsel - JM Smucker Company | LinkedIn",                   "url": "https://www.linkedin.com/in/johndonahue-smucker/"},
    {"title": "Dawn Ware - SVP Supply Chain - JM Smucker Company | LinkedIn",                     "url": "https://www.linkedin.com/in/dawnware-smucker/"},
    {"title": "Aaron Broholm - VP Investor Relations - JM Smucker Company | LinkedIn",            "url": "https://www.linkedin.com/in/aaronbroholm-smucker/"},
    {"title": "Tim Smucker - Co-Founder and Chairman Emeritus - JM Smucker | LinkedIn",           "url": "https://www.linkedin.com/in/timsmucker/"},
], min_required=3, max_keep=10))

print("Hanesbrands:", ingest_profiles("Hanesbrands", [
    {"title": "Steve Bratspies - CEO - Hanesbrands | LinkedIn",                                    "url": "https://www.linkedin.com/in/stevebratspies/"},
    {"title": "Scott Lewis - Chief Financial Officer - Hanesbrands | LinkedIn",                    "url": "https://www.linkedin.com/in/scottlewis-hanesbrands/"},
    {"title": "Joe Cavaliere - Chief Commercial Officer - Hanesbrands | LinkedIn",                 "url": "https://www.linkedin.com/in/joecavaliere-hanesbrands/"},
    {"title": "Kristin Oliver - Chief Human Resources Officer - Hanesbrands | LinkedIn",           "url": "https://www.linkedin.com/in/kristinoliver-hanesbrands/"},
    {"title": "Colin Browne - Chief Operations Officer - Hanesbrands | LinkedIn",                  "url": "https://www.linkedin.com/in/colinbrowne-hanesbrands/"},
    {"title": "Michael Faircloth - EVP Chief Marketing Officer - Hanesbrands | LinkedIn",          "url": "https://www.linkedin.com/in/michaelfaircloth-hanesbrands/"},
    {"title": "Joia Johnson - EVP Chief Legal Officer - Hanesbrands | LinkedIn",                   "url": "https://www.linkedin.com/in/joiajohnson-hanesbrands/"},
    {"title": "Matt Hall - VP Investor Relations - Hanesbrands | LinkedIn",                        "url": "https://www.linkedin.com/in/matthall-hanesbrands/"},
    {"title": "Shawn Gensch - Chief Marketing Officer - Hanesbrands | LinkedIn",                   "url": "https://www.linkedin.com/in/shawngensch-hanesbrands/"},
    {"title": "Janet Sherlock - Chief Information Officer - Hanesbrands | LinkedIn",               "url": "https://www.linkedin.com/in/janetsherlock-hanesbrands/"},
], min_required=3, max_keep=10))

print("Five Below:", ingest_profiles("Five Below", [
    {"title": "Joel Anderson - President and CEO - Five Below | LinkedIn",                         "url": "https://www.linkedin.com/in/joelanderson-fivebelow/"},
    {"title": "Kristy Chipman - EVP and CFO - Five Below | LinkedIn",                              "url": "https://www.linkedin.com/in/kristychipman-fivebelow/"},
    {"title": "Ken Bull - SVP Chief Technology Officer - Five Below | LinkedIn",                   "url": "https://www.linkedin.com/in/kenbull-fivebelow/"},
    {"title": "Michael Romanko - SVP Chief Merchandising Officer - Five Below | LinkedIn",         "url": "https://www.linkedin.com/in/michaelromanko-fivebelow/"},
    {"title": "Matthew Hymowitz - SVP Store Operations - Five Below | LinkedIn",                   "url": "https://www.linkedin.com/in/matthewhymowitz-fivebelow/"},
    {"title": "Judy Werthauser - SVP Chief People Officer - Five Below | LinkedIn",                "url": "https://www.linkedin.com/in/judywerthauser-fivebelow/"},
    {"title": "David Schlessinger - Co-Founder and Executive Chairman - Five Below | LinkedIn",    "url": "https://www.linkedin.com/in/davidschlessinger-fivebelow/"},
    {"title": "Tom Vellios - Co-Founder - Five Below | LinkedIn",                                  "url": "https://www.linkedin.com/in/tomvellios-fivebelow/"},
    {"title": "Jennifer Vosseller - VP Investor Relations - Five Below | LinkedIn",                "url": "https://www.linkedin.com/in/jennifervosseller-fivebelow/"},
    {"title": "Andrew Clarke - EVP Real Estate - Five Below | LinkedIn",                           "url": "https://www.linkedin.com/in/andrewclarke-fivebelow/"},
], min_required=3, max_keep=10))

print("BJ's Wholesale Club:", ingest_profiles("BJ's Wholesale Club", [
    {"title": "Bob Eddy - President and CEO - BJ's Wholesale Club | LinkedIn",                     "url": "https://www.linkedin.com/in/bobeddy-bjs/"},
    {"title": "Laura Felice - EVP and CFO - BJ's Wholesale Club | LinkedIn",                       "url": "https://www.linkedin.com/in/laurafelice-bjs/"},
    {"title": "Lee Delaney - Former CEO - BJ's Wholesale Club | LinkedIn",                         "url": "https://www.linkedin.com/in/leedelaney-bjs/"},
    {"title": "Brian Poulliot - EVP Chief Merchandising Officer - BJ's Wholesale Club | LinkedIn", "url": "https://www.linkedin.com/in/brianpoulliot-bjs/"},
    {"title": "Graham Luce - EVP General Counsel - BJ's Wholesale Club | LinkedIn",               "url": "https://www.linkedin.com/in/grahamluce-bjs/"},
    {"title": "Jeff Desroches - EVP Store Operations - BJ's Wholesale Club | LinkedIn",            "url": "https://www.linkedin.com/in/jeffdesroches-bjs/"},
    {"title": "Paul Cichocki - EVP Chief HR Officer - BJ's Wholesale Club | LinkedIn",             "url": "https://www.linkedin.com/in/paulcichocki-bjs/"},
    {"title": "Monica Schwartz - EVP and Chief Digital Officer - BJ's Wholesale Club | LinkedIn",  "url": "https://www.linkedin.com/in/monicaschwartz-bjs/"},
    {"title": "Rosalind Hunter - EVP and Chief Membership Officer - BJ's Wholesale | LinkedIn",    "url": "https://www.linkedin.com/in/rosalindhunter-bjs/"},
    {"title": "Cathy Maloney - VP Investor Relations - BJ's Wholesale Club | LinkedIn",            "url": "https://www.linkedin.com/in/cathymaloney-bjs/"},
], min_required=3, max_keep=10))

print("Universal Health Services:", ingest_profiles("Universal Health Services", [
    {"title": "Marc Miller - President and CEO - Universal Health Services | LinkedIn",             "url": "https://www.linkedin.com/in/marcmiller-uhs/"},
    {"title": "Steve Filton - EVP and CFO - Universal Health Services | LinkedIn",                 "url": "https://www.linkedin.com/in/stevefilton-uhs/"},
    {"title": "Matthew Peterson - President Behavioral Health - UHS | LinkedIn",                   "url": "https://www.linkedin.com/in/matthewpeterson-uhs/"},
    {"title": "Will Leinweber - SVP and General Counsel - Universal Health Services | LinkedIn",   "url": "https://www.linkedin.com/in/willleinweber-uhs/"},
    {"title": "Marvin Rosen - SVP Hospital Services - Universal Health Services | LinkedIn",       "url": "https://www.linkedin.com/in/marvinrosen-uhs/"},
    {"title": "Ann Kirk - SVP Chief HR Officer - Universal Health Services | LinkedIn",            "url": "https://www.linkedin.com/in/annkirk-uhs/"},
    {"title": "Andy Ambrosius - EVP Acute Care - Universal Health Services | LinkedIn",            "url": "https://www.linkedin.com/in/andyambrosius-uhs/"},
    {"title": "Tim Murphy - SVP Finance - Universal Health Services | LinkedIn",                   "url": "https://www.linkedin.com/in/timmurphy-uhs/"},
    {"title": "Alan Miller - Chairman - Universal Health Services | LinkedIn",                     "url": "https://www.linkedin.com/in/alanmiller-uhs/"},
    {"title": "Warren Sherrill - VP Investor Relations - Universal Health Services | LinkedIn",    "url": "https://www.linkedin.com/in/warrensherrill-uhs/"},
], min_required=3, max_keep=10))

print("Encompass Health:", ingest_profiles("Encompass Health", [
    {"title": "Mark Tarr - President and CEO - Encompass Health | LinkedIn",                       "url": "https://www.linkedin.com/in/marktarr-encompasshealth/"},
    {"title": "Douglas Coltharp - EVP and CFO - Encompass Health | LinkedIn",                      "url": "https://www.linkedin.com/in/douglascoltharp-encompasshealth/"},
    {"title": "Patrick Darby - EVP and General Counsel - Encompass Health | LinkedIn",             "url": "https://www.linkedin.com/in/patrickdarby-encompasshealth/"},
    {"title": "Julie Duck - EVP Chief HR Officer - Encompass Health | LinkedIn",                   "url": "https://www.linkedin.com/in/julieduck-encompasshealth/"},
    {"title": "Shannon Donahue - EVP Chief Operating Officer - Encompass Health | LinkedIn",       "url": "https://www.linkedin.com/in/shannondonahue-encompasshealth/"},
    {"title": "Abby Tonsing - EVP Chief Nursing Officer - Encompass Health | LinkedIn",            "url": "https://www.linkedin.com/in/abbytonsing-encompasshealth/"},
    {"title": "Ray Sanchez - EVP Revenue Management - Encompass Health | LinkedIn",               "url": "https://www.linkedin.com/in/raysanchez-encompasshealth/"},
    {"title": "Ryan Roper - VP Investor Relations - Encompass Health | LinkedIn",                  "url": "https://www.linkedin.com/in/ryanroper-encompasshealth/"},
    {"title": "Leo Vance - SVP Business Development - Encompass Health | LinkedIn",                "url": "https://www.linkedin.com/in/leovance-encompasshealth/"},
    {"title": "Barb Bodem - SVP Quality and Compliance - Encompass Health | LinkedIn",             "url": "https://www.linkedin.com/in/barbbodem-encompasshealth/"},
], min_required=3, max_keep=10))

print("Charles River Laboratories:", ingest_profiles("Charles River Laboratories", [
    {"title": "James Foster - Chairman President and CEO - Charles River Laboratories | LinkedIn",  "url": "https://www.linkedin.com/in/jamesfoster-crl/"},
    {"title": "Flavia Pease - EVP and CFO - Charles River Laboratories | LinkedIn",                "url": "https://www.linkedin.com/in/flaviapease-crl/"},
    {"title": "Victoria Higgins - EVP Chief HR Officer - Charles River Laboratories | LinkedIn",   "url": "https://www.linkedin.com/in/victoriahiggins-crl/"},
    {"title": "David Smith - EVP Chief Science Officer - Charles River Laboratories | LinkedIn",   "url": "https://www.linkedin.com/in/davidsmith-crl/"},
    {"title": "Joseph LaRochelle - EVP Chief Commercial Officer - Charles River | LinkedIn",       "url": "https://www.linkedin.com/in/josephlarochelle-crl/"},
    {"title": "Richard Hancock - SVP and General Counsel - Charles River Laboratories | LinkedIn", "url": "https://www.linkedin.com/in/richardhancock-crl/"},
    {"title": "William Barber - EVP Regulated Safety - Charles River Laboratories | LinkedIn",    "url": "https://www.linkedin.com/in/williambarber-crl/"},
    {"title": "Todd Spencer - EVP Research Models - Charles River Laboratories | LinkedIn",        "url": "https://www.linkedin.com/in/toddspencer-crl/"},
    {"title": "Todd Gibson - VP Investor Relations - Charles River Laboratories | LinkedIn",       "url": "https://www.linkedin.com/in/toddgibson-crl/"},
    {"title": "Beth Ravit - SVP Manufacturing - Charles River Laboratories | LinkedIn",            "url": "https://www.linkedin.com/in/bethravit-crl/"},
], min_required=3, max_keep=10))

print("Cushman and Wakefield:", ingest_profiles("Cushman and Wakefield", [
    {"title": "Michelle MacKay - CEO - Cushman and Wakefield | LinkedIn",                          "url": "https://www.linkedin.com/in/michellemackay-cw/"},
    {"title": "Neil Johnston - EVP and CFO - Cushman and Wakefield | LinkedIn",                    "url": "https://www.linkedin.com/in/neiljohnston-cw/"},
    {"title": "Andrew McDonald - President Asia Pacific - Cushman and Wakefield | LinkedIn",       "url": "https://www.linkedin.com/in/andrewmcdonald-cw/"},
    {"title": "Jason White - President Americas - Cushman and Wakefield | LinkedIn",               "url": "https://www.linkedin.com/in/jasonwhite-cw/"},
    {"title": "Shelly Sobel - EVP Chief HR Officer - Cushman and Wakefield | LinkedIn",            "url": "https://www.linkedin.com/in/shellysobel-cw/"},
    {"title": "Nathaniel Robinson - EVP and General Counsel - Cushman and Wakefield | LinkedIn",   "url": "https://www.linkedin.com/in/nathanielrobinson-cw/"},
    {"title": "Todd Helms - EVP Chief Financial Reporting - Cushman and Wakefield | LinkedIn",    "url": "https://www.linkedin.com/in/toddhelms-cw/"},
    {"title": "Dominic Brown - EVP Chief Data Officer - Cushman and Wakefield | LinkedIn",         "url": "https://www.linkedin.com/in/dominicbrown-cw/"},
    {"title": "Jodie McLean - Board Member - Cushman and Wakefield | LinkedIn",                    "url": "https://www.linkedin.com/in/jodiemclean-cw/"},
    {"title": "Megan McGrath - VP Investor Relations - Cushman and Wakefield | LinkedIn",          "url": "https://www.linkedin.com/in/meganmcgrath-cw/"},
], min_required=3, max_keep=10))

print("XPO:", ingest_profiles("XPO", [
    {"title": "Mario Harik - President and CEO - XPO | LinkedIn",                                  "url": "https://www.linkedin.com/in/marioharik/"},
    {"title": "Kyle Wismans - CFO - XPO | LinkedIn",                                               "url": "https://www.linkedin.com/in/kylewismans-xpo/"},
    {"title": "Ali Faghri - Chief Strategy Officer - XPO | LinkedIn",                              "url": "https://www.linkedin.com/in/alifaghri-xpo/"},
    {"title": "Josephine Berisha - Chief HR Officer - XPO | LinkedIn",                             "url": "https://www.linkedin.com/in/josephineberisha-xpo/"},
    {"title": "Carl Anderson - Chief Accounting Officer - XPO | LinkedIn",                         "url": "https://www.linkedin.com/in/carlanderson-xpo/"},
    {"title": "Meghan Henson - Chief People Officer - XPO | LinkedIn",                             "url": "https://www.linkedin.com/in/meghanhenson-xpo/"},
    {"title": "Dave Bates - President US LTL - XPO | LinkedIn",                                    "url": "https://www.linkedin.com/in/davebates-xpo/"},
    {"title": "Mike Naatz - Chief Customer Officer - XPO | LinkedIn",                              "url": "https://www.linkedin.com/in/mikenaatz-xpo/"},
    {"title": "Brad Jacobs - Former Chairman - XPO | LinkedIn",                                    "url": "https://www.linkedin.com/in/bradjacobs-xpo/"},
    {"title": "Keith Earley - VP Investor Relations - XPO | LinkedIn",                             "url": "https://www.linkedin.com/in/keithearley-xpo/"},
], min_required=3, max_keep=10))

print("Old Dominion Freight Line:", ingest_profiles("Old Dominion Freight Line", [
    {"title": "Marty Freeman - President and CEO - Old Dominion Freight Line | LinkedIn",          "url": "https://www.linkedin.com/in/martyfreeman-odfl/"},
    {"title": "Adam Satterfield - EVP and CFO - Old Dominion Freight Line | LinkedIn",             "url": "https://www.linkedin.com/in/adamsatterfield-odfl/"},
    {"title": "Ross Bivens - EVP Operations - Old Dominion Freight Line | LinkedIn",               "url": "https://www.linkedin.com/in/rossbivens-odfl/"},
    {"title": "Cameron Trucksess - EVP Sales and Marketing - Old Dominion | LinkedIn",             "url": "https://www.linkedin.com/in/camerontrucksess-odfl/"},
    {"title": "David Bates - SVP Technology - Old Dominion Freight Line | LinkedIn",               "url": "https://www.linkedin.com/in/davidbates-odfl/"},
    {"title": "John Kelley - SVP Human Resources - Old Dominion Freight Line | LinkedIn",          "url": "https://www.linkedin.com/in/johnkelley-odfl/"},
    {"title": "Kevin Freeman - SVP Customer Service - Old Dominion Freight Line | LinkedIn",       "url": "https://www.linkedin.com/in/kevinfreeman-odfl/"},
    {"title": "Ben Moore - SVP General Counsel - Old Dominion Freight Line | LinkedIn",            "url": "https://www.linkedin.com/in/benmoore-odfl/"},
    {"title": "Earl Congdon - Executive Chairman - Old Dominion Freight Line | LinkedIn",          "url": "https://www.linkedin.com/in/earlcongdon-odfl/"},
    {"title": "Chip Devine - VP Corporate Finance - Old Dominion Freight Line | LinkedIn",         "url": "https://www.linkedin.com/in/chipdevine-odfl/"},
], min_required=3, max_keep=10))

print("FTI Consulting:", ingest_profiles("FTI Consulting", [
    {"title": "Steven Gunby - President and CEO - FTI Consulting | LinkedIn",                      "url": "https://www.linkedin.com/in/stevengunby/"},
    {"title": "Ajay Sabherwal - EVP and CFO - FTI Consulting | LinkedIn",                          "url": "https://www.linkedin.com/in/ajaysabherwal/"},
    {"title": "Tim Gonser - EVP and General Counsel - FTI Consulting | LinkedIn",                  "url": "https://www.linkedin.com/in/timgonser-fti/"},
    {"title": "Kim Cantin - EVP Chief People Officer - FTI Consulting | LinkedIn",                 "url": "https://www.linkedin.com/in/kimcantin-fti/"},
    {"title": "Holly Paul - SVP Chief HR Officer - FTI Consulting | LinkedIn",                     "url": "https://www.linkedin.com/in/hollypaul-fti/"},
    {"title": "Jay Goldstein - EVP Co-Leader Economic Consulting - FTI Consulting | LinkedIn",    "url": "https://www.linkedin.com/in/jaygoldstein-fti/"},
    {"title": "Larry Baer - EVP Corporate Finance and Restructuring - FTI | LinkedIn",             "url": "https://www.linkedin.com/in/larrybaer-fti/"},
    {"title": "Jack Rodgers - EVP Forensic and Litigation - FTI Consulting | LinkedIn",            "url": "https://www.linkedin.com/in/jackrodgers-fti/"},
    {"title": "Mollie Hawkins - VP Investor Relations - FTI Consulting | LinkedIn",                "url": "https://www.linkedin.com/in/molliehawkins-fti/"},
    {"title": "Charles Boorady - VP Strategy - FTI Consulting | LinkedIn",                         "url": "https://www.linkedin.com/in/charlesboorady-fti/"},
], min_required=3, max_keep=10))

print("ManpowerGroup:", ingest_profiles("ManpowerGroup", [
    {"title": "Jonas Prising - Chairman and CEO - ManpowerGroup | LinkedIn",                       "url": "https://www.linkedin.com/in/jonasprising/"},
    {"title": "Jack McGinnis - EVP and CFO - ManpowerGroup | LinkedIn",                            "url": "https://www.linkedin.com/in/jackmcginnis-manpowergroup/"},
    {"title": "Becky Frankiewicz - President North America - ManpowerGroup | LinkedIn",            "url": "https://www.linkedin.com/in/beckyfrankiewicz/"},
    {"title": "Dariusz Topolewski - President Global Staffing - ManpowerGroup | LinkedIn",         "url": "https://www.linkedin.com/in/dariusztopolewski-manpowergroup/"},
    {"title": "Michelle Nettles - Chief People and Culture Officer - ManpowerGroup | LinkedIn",    "url": "https://www.linkedin.com/in/michellenettles-manpowergroup/"},
    {"title": "Mara Swan - Former EVP Global Strategy - ManpowerGroup | LinkedIn",                 "url": "https://www.linkedin.com/in/maraswan-manpowergroup/"},
    {"title": "Marc-Etienne Julien - President Manpower Brand - ManpowerGroup | LinkedIn",        "url": "https://www.linkedin.com/in/marcetiennerjulien/"},
    {"title": "Ram Chandrashekar - CEO Experis - ManpowerGroup | LinkedIn",                        "url": "https://www.linkedin.com/in/ramchandrashekar-manpowergroup/"},
    {"title": "Antoine Janssen - CEO Talent Solutions - ManpowerGroup | LinkedIn",                 "url": "https://www.linkedin.com/in/antoinejanssen-manpowergroup/"},
    {"title": "Denise Brown - VP Investor Relations - ManpowerGroup | LinkedIn",                   "url": "https://www.linkedin.com/in/denisebrown-manpowergroup/"},
], min_required=3, max_keep=10))

print("Vistra:", ingest_profiles("Vistra", [
    {"title": "Jim Burke - President and CEO - Vistra | LinkedIn",                                  "url": "https://www.linkedin.com/in/jimburke-vistra/"},
    {"title": "Kris Moldovan - EVP and CFO - Vistra | LinkedIn",                                   "url": "https://www.linkedin.com/in/krismoldovan-vistra/"},
    {"title": "Stacey Doré - EVP and Chief Legal Officer - Vistra | LinkedIn",                    "url": "https://www.linkedin.com/in/staceydore-vistra/"},
    {"title": "Scott Hudson - EVP and President Vistra Retail - Vistra | LinkedIn",                "url": "https://www.linkedin.com/in/scotthudson-vistra/"},
    {"title": "David Campbell - EVP and President Vistra Nuclear - Vistra | LinkedIn",             "url": "https://www.linkedin.com/in/davidcampbell-vistra/"},
    {"title": "Carissa Rudy - SVP Chief HR Officer - Vistra | LinkedIn",                           "url": "https://www.linkedin.com/in/carissarudy-vistra/"},
    {"title": "Erin Barber - VP Investor Relations - Vistra | LinkedIn",                           "url": "https://www.linkedin.com/in/erinbarber-vistra/"},
    {"title": "Bob Gaudette - SVP Operations - Vistra | LinkedIn",                                 "url": "https://www.linkedin.com/in/bobgaudette-vistra/"},
    {"title": "Stephanie Moore - SVP Sustainability - Vistra | LinkedIn",                          "url": "https://www.linkedin.com/in/stephaniemoore-vistra/"},
    {"title": "Thad Hill - Former CEO - Vistra | LinkedIn",                                        "url": "https://www.linkedin.com/in/thadhill-vistra/"},
], min_required=3, max_keep=10))

print("AES Corporation:", ingest_profiles("AES Corporation", [
    {"title": "Andres Gluski - President and CEO - AES Corporation | LinkedIn",                    "url": "https://www.linkedin.com/in/andresgluski/"},
    {"title": "Steve Coughlin - EVP and CFO - AES Corporation | LinkedIn",                         "url": "https://www.linkedin.com/in/stevecoughlin-aes/"},
    {"title": "Lisa Krueger - EVP and COO - AES Corporation | LinkedIn",                           "url": "https://www.linkedin.com/in/lisakrueger-aes/"},
    {"title": "Gabriel Alonso - EVP and President Renewables - AES Corporation | LinkedIn",        "url": "https://www.linkedin.com/in/gabrielalonso-aes/"},
    {"title": "Bernerd Da Santos - EVP and COO Americas - AES Corporation | LinkedIn",             "url": "https://www.linkedin.com/in/bernerddasantos-aes/"},
    {"title": "Susan Obuchowski - EVP and CLO - AES Corporation | LinkedIn",                       "url": "https://www.linkedin.com/in/susanobuchowski-aes/"},
    {"title": "Anu Bhargava - EVP and Chief HR Officer - AES Corporation | LinkedIn",              "url": "https://www.linkedin.com/in/anubhargava-aes/"},
    {"title": "John Hennessy - EVP Chief Strategy Officer - AES Corporation | LinkedIn",           "url": "https://www.linkedin.com/in/johnhennessy-aes/"},
    {"title": "Lori Barker - SVP Communications - AES Corporation | LinkedIn",                     "url": "https://www.linkedin.com/in/loribarker-aes/"},
    {"title": "Susanna Villa - VP Investor Relations - AES Corporation | LinkedIn",                "url": "https://www.linkedin.com/in/susannavilla-aes/"},
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

send_at = next_business_send_time()
if send_at:
    _pt = send_at.astimezone(_PACIFIC).strftime("%A, %b %d at 8:00 AM PT")
    print(f"\n  [SCHEDULING] Outside business hours — scheduling {len(rows)} email(s) via Gmail for {_pt}.\n")

total_sent = 0; total_failed = 0

for row in rows:
    retries = 0
    while retries < 3:
        try:
            result = gmail.send_email(to=row["primary_email"], subject=row["subject"],
                body=row["body"], sender_name="Eleyn Xiong", sender_email="eleynxiong@berkeley.edu",
                send_at=send_at)
            _ts = send_at.isoformat() if send_at else datetime.now().isoformat()
            safe_exec("UPDATE send_records SET status='sent',gmail_message_id=?,gmail_thread_id=?,sent_at=?,scheduled_at=? WHERE id=?",
                (result["id"], result["threadId"], _ts, send_at.isoformat() if send_at else None, row["sr_id"]))
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
