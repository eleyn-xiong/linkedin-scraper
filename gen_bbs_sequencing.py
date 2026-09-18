"""Regenerate bbs_master_sequencing.csv from ALL BBS campaigns.

Reply counting:  reply_detected_at IS NOT NULL  (Gmail API verified; filters
                 out the 584 phantom 'replied' rows in bbs_outreach_1 that
                 have no timestamp)
Bounce counting: bounced_at IS NOT NULL OR status='bounced'  (catches both
                 new campaigns with timestamped bounces and old campaigns
                 that only set the status field)
"""
import sys, sqlite3, csv, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row

campaigns = conn.execute("""
    SELECT id, name FROM campaigns
    WHERE name LIKE '%BBS%' OR name LIKE '%bbs%' OR name LIKE '%Berkeley Business%'
    ORDER BY created_at
""").fetchall()

print("BBS campaigns included:")
for c in campaigns:
    n = conn.execute(
        "SELECT COUNT(*) as n FROM send_records WHERE campaign_id=?",
        (c["id"],)).fetchone()["n"]
    print(f"  {c['name']}  ({n} records)")

campaign_ids = [c["id"] for c in campaigns]
if not campaign_ids:
    print("No BBS campaigns found."); sys.exit(1)

ph = ",".join("?" * len(campaign_ids))

rows = conn.execute(f"""
    SELECT
        co.name                                                         AS company,
        co.domain,
        COUNT(sr.id)                                                    AS total_sent,
        SUM(CASE WHEN sr.reply_detected_at IS NOT NULL THEN 1 ELSE 0 END) AS replies,
        SUM(CASE WHEN sr.bounced_at IS NOT NULL
                   OR sr.status = 'bounced'         THEN 1 ELSE 0 END) AS bounces,
        MIN(sr.reply_detected_at)                                       AS first_reply,
        GROUP_CONCAT(DISTINCT c.name)                                   AS campaigns
    FROM send_records sr
    JOIN contacts  ct ON sr.contact_id  = ct.id
    JOIN companies co ON ct.company_id  = co.id
    JOIN campaigns c  ON sr.campaign_id = c.id
    WHERE sr.campaign_id IN ({ph})
      AND sr.status IN ('sent','bounced','replied','failed')
    GROUP BY co.id
    ORDER BY replies DESC, total_sent DESC
""", campaign_ids).fetchall()

total_sent    = sum(r["total_sent"] for r in rows)
total_replies = sum(r["replies"]    for r in rows)
total_bounces = sum(r["bounces"]    for r in rows)
num_campaigns = len(campaigns)

r_pct = f"{100*total_replies/total_sent:.1f}%" if total_sent else "0.0%"
b_pct = f"{100*total_bounces/total_sent:.1f}%" if total_sent else "0.0%"

summary = (f"BBS Master Sequencing — {num_campaigns} campaigns — "
           f"{total_sent} sent | {total_replies} replies ({r_pct}) | "
           f"{total_bounces} bounces ({b_pct})")

print(f"\n{summary}\n")

def fmt_date(iso):
    if not iso:
        return ""
    try:
        return datetime.datetime.fromisoformat(iso).strftime("%a, %-d %b %Y")
    except Exception:
        return iso[:10]

out_path = "bbs_master_sequencing.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([summary])
    w.writerow([])
    w.writerow(["Company", "Domain", "Total Sent", "Replies", "Bounces",
                "Reply %", "Bounce %", "First Reply Date", "Campaign(s)"])
    for r in rows:
        s, rp, bp = r["total_sent"], r["replies"], r["bounces"]
        w.writerow([
            r["company"], r["domain"], s, rp, bp,
            f"{100*rp/s:.1f}%" if s else "0.0%",
            f"{100*bp/s:.1f}%" if s else "0.0%",
            fmt_date(r["first_reply"]),
            r["campaigns"],
        ])

print(f"Wrote {len(rows)} companies to {out_path}\n")

print(f"{'Company':<40} {'Sent':>6} {'Replies':>8} {'Reply%':>7} {'Bounces':>8} {'Bounce%':>8}  First Reply")
print("-" * 102)
for r in rows:
    s, rp, bp = r["total_sent"], r["replies"], r["bounces"]
    print(f"{r['company']:<40} {s:>6} {rp:>8} {100*rp/s:>6.1f}% {bp:>8} {100*bp/s:>7.1f}%  {fmt_date(r['first_reply'])}")

conn.close()
