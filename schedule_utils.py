"""Business-hours gate for email send pipelines.

Pacific Time (America/Los_Angeles), Mon–Fri, 9 AM – 5 PM.
Outside those hours the send step is deferred: queued records get a
scheduled_at timestamp and the pipeline exits with a message to re-run
during business hours.
"""

import sqlite3
from datetime import datetime, timedelta, timezone, time as _time

try:
    from zoneinfo import ZoneInfo
    _PACIFIC = ZoneInfo("America/Los_Angeles")
except Exception:
    # Fallback: fixed UTC-7 (PDT). Correct for Berkeley Apr–Oct.
    _PACIFIC = timezone(timedelta(hours=-7))

_START = _time(9, 0)
_END   = _time(17, 0)


def next_business_send_time():
    """Return None if currently in business hours (send now).
    Otherwise return a UTC datetime for next business day 8 AM PT.
    """
    now_pt = datetime.now(_PACIFIC)
    t = now_pt.time().replace(tzinfo=None)
    in_window = now_pt.weekday() < 5 and _START <= t < _END
    if in_window:
        return None

    nxt = now_pt.date() + timedelta(days=1)
    while nxt.weekday() >= 5:   # skip Sat / Sun
        nxt += timedelta(days=1)

    send_pt = datetime(nxt.year, nxt.month, nxt.day, 8, 0, 0, tzinfo=_PACIFIC)
    return send_pt.astimezone(timezone.utc)


def check_send_window(campaign_id=None, db_path="outreach.db"):
    """Call this at the start of a pipeline's send step.

    Returns True  → in business hours; proceed to send normally.
    Returns False → outside hours; emails scheduled; caller should exit/return.

    When campaign_id is provided, the scheduled_at field is written to all
    queued records for that campaign so the scheduled time is visible in the DB.
    """
    send_time = next_business_send_time()
    if send_time is None:
        return True

    count = 0
    if campaign_id:
        try:
            conn = sqlite3.connect(db_path, timeout=60)
            conn.execute(
                "UPDATE send_records SET scheduled_at=? "
                "WHERE campaign_id=? AND status='queued'",
                (send_time.isoformat(), campaign_id),
            )
            conn.commit()
            count = conn.execute(
                "SELECT COUNT(*) FROM send_records "
                "WHERE campaign_id=? AND status='queued'",
                (campaign_id,),
            ).fetchone()[0]
            conn.close()
        except Exception:
            pass

    try:
        pt_str = send_time.astimezone(_PACIFIC).strftime("%A, %b %d at 8:00 AM PT")
    except Exception:
        pt_str = send_time.isoformat()

    noun = f"{count} email(s)" if campaign_id else "queued emails"
    print("\n[SCHEDULED] Outside business hours (Mon–Fri 9 AM–5 PM PT).")
    print(f"  {noun} will be sent on {pt_str}.")
    print("  Re-run this script during business hours to send them.\n")
    return False
