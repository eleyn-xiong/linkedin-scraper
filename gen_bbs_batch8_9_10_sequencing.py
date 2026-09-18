"""Generate sequencing CSV for BBS Batches 8, 9, and 10."""
import sys, sqlite3, csv, datetime
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

conn = sqlite3.connect("outreach.db")
conn.row_factory = sqlite3.Row

BATCH_NAMES = [
    "BBS Batch 8 - July 2026",
    "BBS Batch 9 - July 2026",
    "BBS Batch 10 - July 2026",
]

campaigns = []
for name in BATCH_NAMES:
    row = conn.execute("SELECT id, name FROM campaigns WHERE name=?", (name,)).fetchone()
    if row:
        campaigns.append(row)
        n = conn.execute("SELECT COUNT(*) as n FROM send_records WHERE campaign_id=?", (row["id"],)).fetchone()["n"]
        s = conn.execute("SELECT COUNT(*) as n FROM send_records WHERE campaign_id=? AND status='sent'", (row["id"],)).fetchone()["n"]
        print(f"  Found: {row['name']}  ({n} records, {s} sent)")
    else:
        print(f"  NOT FOUND: {name}")

if not campaigns:
    print("No matching campaigns found."); sys.exit(1)

campaign_ids = [c["id"] for c in campaigns]
ph = ",".join("?" * len(campaign_ids))

rows = conn.execute(f"""
    SELECT
        co.name                                                                 AS company,
        co.domain,
        co.industry,
        COUNT(sr.id)                                                            AS total_records,
        SUM(CASE WHEN sr.status IN ('sent','replied')                     THEN 1 ELSE 0 END) AS total_sent,
        SUM(CASE WHEN sr.reply_detected_at IS NOT NULL                    THEN 1 ELSE 0 END) AS replies,
        SUM(CASE WHEN sr.bounced_at IS NOT NULL
                   OR sr.status = 'bounced'                               THEN 1 ELSE 0 END) AS bounces,
        SUM(CASE WHEN sr.status = 'failed'                                THEN 1 ELSE 0 END) AS failed,
        SUM(CASE WHEN sr.status = 'queued'                                THEN 1 ELSE 0 END) AS queued,
        MIN(sr.reply_detected_at)                                               AS first_reply,
        MAX(sr.sent_at)                                                         AS last_sent,
        GROUP_CONCAT(DISTINCT c.name)                                           AS campaign
    FROM send_records sr
    JOIN contacts  ct ON sr.contact_id  = ct.id
    JOIN companies co ON ct.company_id  = co.id
    JOIN campaigns c  ON sr.campaign_id = c.id
    WHERE sr.campaign_id IN ({ph})
    GROUP BY co.id
    ORDER BY c.name, co.name
""", campaign_ids).fetchall()

total_sent    = sum(r["total_sent"] for r in rows)
total_replies = sum(r["replies"]    for r in rows)
total_bounces = sum(r["bounces"]    for r in rows)
total_failed  = sum(r["failed"]     for r in rows)
total_queued  = sum(r["queued"]     for r in rows)

r_pct = f"{100*total_replies/total_sent:.1f}%" if total_sent else "0.0%"
b_pct = f"{100*total_bounces/total_sent:.1f}%" if total_sent else "0.0%"

summary = (
    f"BBS Batches 8, 9 & 10 — {len(campaigns)} campaigns — "
    f"{len(rows)} companies — "
    f"{total_sent} sent | {total_replies} replies ({r_pct}) | "
    f"{total_bounces} bounces ({b_pct})"
    + (f" | {total_queued} still queued" if total_queued else "")
)
print(f"\n{summary}\n")

def fmt_date(iso):
    if not iso:
        return ""
    try:
        return datetime.datetime.fromisoformat(iso).strftime("%Y-%m-%d")
    except Exception:
        return str(iso)[:10]

out_path = "bbs_batch8_9_10_sequencing.csv"
with open(out_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow([summary])
    w.writerow([])
    w.writerow([
        "Company", "Domain", "Industry",
        "Sent", "Replies", "Reply %", "Bounces", "Bounce %", "Failed", "Queued",
        "First Reply", "Last Sent", "Campaign",
    ])
    for r in rows:
        s, rp, bp = r["total_sent"], r["replies"], r["bounces"]
        w.writerow([
            r["company"], r["domain"], r["industry"] or "",
            s, rp,
            f"{100*rp/s:.1f}%" if s else "—",
            bp,
            f"{100*bp/s:.1f}%" if s else "—",
            r["failed"],
            r["queued"],
            fmt_date(r["first_reply"]),
            fmt_date(r["last_sent"]),
            r["campaign"],
        ])

print(f"Wrote {len(rows)} companies → {out_path}")
print()
print(f"{'Company':<38} {'Batch':<8} {'Sent':>5} {'Rep':>4} {'Rep%':>5} {'Bnc':>4} {'Bnc%':>5} {'Fail':>4} {'Q':>4}  First Reply")
print("-" * 108)
for r in rows:
    s, rp, bp = r["total_sent"], r["replies"], r["bounces"]
    batch = r["campaign"].replace("BBS Batch ","B").replace(" - July 2026","") if r["campaign"] else ""
    print(
        f"{r['company']:<38} {batch:<8} {s:>5} {rp:>4} "
        f"{'—' if not s else f'{100*rp/s:.0f}%':>5} "
        f"{bp:>4} {'—' if not s else f'{100*bp/s:.0f}%':>5} "
        f"{r['failed']:>4} {r['queued']:>4}  {fmt_date(r['first_reply'])}"
    )

print(f"\nTotals: {len(rows)} companies | {total_sent} sent | {total_replies} replies ({r_pct}) | {total_bounces} bounces ({b_pct}) | {total_failed} failed | {total_queued} queued")
conn.close()
