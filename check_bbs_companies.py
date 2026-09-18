import sqlite3
conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row

all_campaigns = conn.execute("SELECT id, name FROM campaigns ORDER BY created_at").fetchall()
bbs_campaigns = [
    c for c in all_campaigns
    if not any(kw in c["name"] for kw in ["FV", "Free Ventures", "Venture Out", " VO "])
    and not c["name"].startswith("VO ")
    and not c["name"].startswith("Venture Out")
]
bbs_ids = [c["id"] for c in bbs_campaigns]
print(f"BBS campaigns ({len(bbs_campaigns)}):")
for c in bbs_campaigns:
    print(f"  {c['name']}")

if bbs_ids:
    placeholders = ",".join("?" * len(bbs_ids))
    companies = conn.execute(f"""
        SELECT DISTINCT co.name, COUNT(sr.id) as sent
        FROM send_records sr
        JOIN contacts ct ON sr.contact_id = ct.id
        JOIN companies co ON ct.company_id = co.id
        WHERE sr.campaign_id IN ({placeholders})
        GROUP BY co.id, co.name
        ORDER BY co.name
    """, bbs_ids).fetchall()
    print(f"\nCompanies already in BBS ({len(companies)}):")
    for c in companies:
        print(f"  {c['name']}")
conn.close()
