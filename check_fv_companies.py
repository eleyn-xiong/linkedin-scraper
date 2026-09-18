import sqlite3
conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row
all_campaigns = conn.execute("SELECT id, name FROM campaigns ORDER BY created_at").fetchall()
fv_campaigns = [
    c for c in all_campaigns
    if any(kw in c["name"] for kw in ["FV", "Free Ventures", "Free V"])
]
print(f"FV campaigns ({len(fv_campaigns)}):")
for c in fv_campaigns:
    print(f"  {c['name']}")
fv_ids = [c["id"] for c in fv_campaigns]
if fv_ids:
    placeholders = ",".join("?" * len(fv_ids))
    companies = conn.execute(f"""
        SELECT DISTINCT co.name, COUNT(sr.id) as sent
        FROM send_records sr
        JOIN contacts ct ON sr.contact_id = ct.id
        JOIN companies co ON ct.company_id = co.id
        WHERE sr.campaign_id IN ({placeholders})
        GROUP BY co.id, co.name
        ORDER BY co.name
    """, fv_ids).fetchall()
    print(f"\nCompanies already in FV ({len(companies)}):")
    for c in companies:
        print(f"  {c['name']}")
conn.close()
