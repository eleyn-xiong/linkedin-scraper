import sqlite3
conn = sqlite3.connect('outreach.db')
conn.row_factory = sqlite3.Row
campaigns = conn.execute("""
    SELECT c.name,
           SUM(CASE WHEN sr.status='sent' THEN 1 ELSE 0 END) as sent,
           SUM(CASE WHEN sr.status='queued' THEN 1 ELSE 0 END) as queued,
           SUM(CASE WHEN sr.status='failed' THEN 1 ELSE 0 END) as failed
    FROM campaigns c JOIN send_records sr ON c.id=sr.campaign_id
    WHERE c.name LIKE '%Gmail%'
    GROUP BY c.name ORDER BY c.created_at
""").fetchall()
print("Gmail campaign status:")
total_sent = total_queued = total_failed = 0
for c in campaigns:
    print(f"  {c['name']}")
    print(f"    sent={c['sent']}  queued={c['queued']}  failed={c['failed']}")
    total_sent += c['sent'] or 0
    total_queued += c['queued'] or 0
    total_failed += c['failed'] or 0
print(f"\nTOTAL: sent={total_sent}  queued={total_queued}  failed={total_failed}")
conn.close()
