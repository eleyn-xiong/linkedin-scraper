import sys, sqlite3
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row

rows = conn.execute("""
    SELECT c.name, sr.status, COUNT(*) as cnt
    FROM send_records sr
    JOIN campaigns c ON sr.campaign_id = c.id
    WHERE c.name LIKE '%BBS%' OR c.name LIKE '%bbs%'
    GROUP BY c.name, sr.status
    ORDER BY c.created_at, sr.status
""").fetchall()

for r in rows:
    print(f"{r['name'][:45]:<47} {r['status']:<12} {r['cnt']}")

print("\n--- State Farm status sample ---")
sf = conn.execute("""
    SELECT sr.status, sr.reply_detected_at, sr.bounced_at
    FROM send_records sr
    JOIN contacts ct ON sr.contact_id=ct.id
    JOIN companies co ON ct.company_id=co.id
    JOIN campaigns c ON sr.campaign_id=c.id
    WHERE co.name='State Farm' AND (c.name LIKE '%BBS%' OR c.name LIKE '%bbs%')
    LIMIT 10
""").fetchall()
for r in sf:
    print(f"  status={r['status']}, reply_detected_at={r['reply_detected_at']}, bounced_at={r['bounced_at']}")
