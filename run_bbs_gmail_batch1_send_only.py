"""Resume sending queued emails for BBS Gmail Batch 1 from eleynxiong@gmail.com."""
import sys, time, random, sqlite3
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from gmail_client import GmailClient
from datetime import datetime

with open("CAMPAIGN_ID.txt") as f:
    CAMPAIGN_ID = f.read().strip()

print(f"Campaign ID: {CAMPAIGN_ID}")

gmail = GmailClient(account="gmail")

conn = sqlite3.connect("outreach.db", timeout=60)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys=ON"); conn.execute("PRAGMA busy_timeout=60000")

def safe_exec(sql, params=()):
    for _ in range(5):
        try:
            conn.execute(sql, params); conn.commit(); return
        except sqlite3.OperationalError as e:
            if "locked" in str(e): time.sleep(2)
            else: raise

rows = conn.execute("""
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
""", (CAMPAIGN_ID,)).fetchall()

print(f"{len(rows)} emails still queued — resuming from eleynxiong@gmail.com...")

total_sent = 0; total_failed = 0

for row in rows:
    retries = 0
    while retries < 3:
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
            break
        except ConnectionResetError as e:
            retries += 1
            print(f"  [retry {retries}/3] Connection reset for {row['primary_email']} — waiting 30s...")
            time.sleep(30)
            # Rebuild Gmail service on connection errors
            if retries < 3:
                try:
                    gmail = GmailClient(account="gmail")
                except Exception:
                    pass
        except Exception as e:
            total_failed += 1
            print(f"  [!] FAILED {row['primary_email']}: {e}")
            safe_exec(
                "UPDATE send_records SET status='failed',error=? WHERE id=?",
                (str(e)[:500], row["sr_id"])
            )
            break
    else:
        # All 3 retries exhausted
        total_failed += 1
        print(f"  [!] GAVE UP {row['primary_email']} after 3 retries")
        safe_exec(
            "UPDATE send_records SET status='failed',error='ConnectionResetError after 3 retries' WHERE id=?",
            (row["sr_id"],)
        )

    delay = random.uniform(60, 90)
    time.sleep(delay)

conn.close()

print(f"\n{'='*60}")
print(f"DONE — {total_sent} sent, {total_failed} failed")
print(f"Sender: eleynxiong@gmail.com | Campaign ID: {CAMPAIGN_ID}")
print(f"{'='*60}")
