import sqlite3
conn = sqlite3.connect('outreach.db')
print('All tables:')
for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    print(' ', row[0])

# Check personalized_messages or similar
for table in ['personalized_messages', 'outreach_messages', 'email_queue', 'queued_emails']:
    try:
        cols = conn.execute(f"PRAGMA table_info({table})").fetchall()
        if cols:
            print(f'\n{table} columns:')
            for c in cols:
                print(' ', c)
    except:
        pass
conn.close()
