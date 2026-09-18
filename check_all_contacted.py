import sqlite3
conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row
companies = conn.execute("""
    SELECT DISTINCT co.name, co.domain
    FROM send_records sr
    JOIN contacts ct ON sr.contact_id=ct.id
    JOIN companies co ON ct.company_id=co.id
    ORDER BY co.name
""").fetchall()
print(f"{len(companies)} companies ever contacted:")
for c in companies:
    print(f"  {c['name']} ({c['domain']})")
conn.close()
