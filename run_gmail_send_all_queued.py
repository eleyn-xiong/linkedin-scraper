"""
Send all queued emails across all Gmail campaigns from eleynxiong@berkeley.edu.
Reads queued records from DB and sends in order. Safe to re-run.
"""
import sys, sqlite3, time, random
from datetime import datetime
from schedule_utils import next_business_send_time, _PACIFIC

DB_PATH = "outreach.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=60)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=60000")
    return conn

def safe_exec(sql, params=()):
    for attempt in range(5):
        try:
            conn = get_conn()
            conn.execute(sql, params)
            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError as e:
            if "locked" in str(e) and attempt < 4:
                time.sleep(2 ** attempt)
            else:
                raise

# Fetch all queued records across all Gmail campaigns
conn = get_conn()
rows = conn.execute("""
    SELECT sr.id as sr_id, sr.campaign_id, c.name as campaign_name,
           ct.primary_email, pm.subject, pm.body
    FROM send_records sr
    JOIN campaigns c ON sr.campaign_id = c.id
    JOIN contacts ct ON sr.contact_id = ct.id
    JOIN personalized_messages pm
      ON pm.contact_id = sr.contact_id
     AND pm.campaign_id = sr.campaign_id
     AND pm.step_number = sr.step_number
    WHERE sr.status = 'queued'
      AND c.name LIKE '%Gmail%'
    ORDER BY c.created_at, sr.id
""").fetchall()
conn.close()

print(f"Total queued across all Gmail campaigns: {len(rows)}")

send_at = next_business_send_time()
if send_at:
    _pt = send_at.astimezone(_PACIFIC).strftime("%A, %b %d at 8:00 AM PT")
    print(f"\n[SCHEDULING] Outside business hours — scheduling {len(rows)} email(s) via Gmail for {_pt}.\n")

from gmail_client import GmailClient
gmail = GmailClient(account="default")

total_sent = 0
total_failed = 0
last_campaign = None

for i, row in enumerate(rows, 1):
    if row["campaign_name"] != last_campaign:
        print(f"\n--- {row['campaign_name']} ---")
        last_campaign = row["campaign_name"]

    print(f"  [{i}/{len(rows)}] {row['primary_email']}", end="", flush=True)

    retries = 0
    while retries < 3:
        try:
            result = gmail.send_email(
                to=row["primary_email"],
                subject=row["subject"],
                body=row["body"],
                sender_name="Eleyn Xiong",
                sender_email="eleynxiong@berkeley.edu",
                send_at=send_at,
            )
            _ts = send_at.isoformat() if send_at else datetime.now().isoformat()
            safe_exec(
                "UPDATE send_records SET status='sent', gmail_message_id=?, gmail_thread_id=?, sent_at=?, scheduled_at=? WHERE id=?",
                (result["id"], result["threadId"], _ts, send_at.isoformat() if send_at else None, row["sr_id"])
            )
            total_sent += 1
            print(" OK")
            break
        except ConnectionResetError:
            retries += 1
            print(f" [reset, retry {retries}/3]", end="", flush=True)
            time.sleep(30)
            try:
                gmail = GmailClient(account="default")
            except Exception:
                pass
        except Exception as e:
            total_failed += 1
            safe_exec(
                "UPDATE send_records SET status='failed', error=? WHERE id=?",
                (str(e)[:500], row["sr_id"])
            )
            print(f" FAIL: {e}")
            break
    else:
        safe_exec(
            "UPDATE send_records SET status='failed', error='ConnectionResetError after 3 retries' WHERE id=?",
            (row["sr_id"],)
        )
        print(" FAIL [3 retries exhausted]")
        total_failed += 1

    delay = random.uniform(15, 25)
    time.sleep(delay)

print(f"\nDone. Sent: {total_sent}  Failed: {total_failed}")
