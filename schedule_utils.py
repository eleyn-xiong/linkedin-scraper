"""Business-hours scheduling utilities for email send pipelines.

Pacific Time (America/Los_Angeles), Mon–Fri, 8 AM – 5 PM.

Usage in a pipeline's send step:
    from schedule_utils import next_business_send_time, _PACIFIC

    send_at = next_business_send_time()   # None = send now; datetime = schedule
    if send_at:
        pt_str = send_at.astimezone(_PACIFIC).strftime("%A, %b %d at 8:00 AM PT")
        print(f"[SCHEDULING] Outside business hours — scheduling via Gmail for {pt_str}.")

    result = gmail.send_email(..., send_at=send_at)
"""

from datetime import datetime, timedelta, timezone, time as _time

try:
    from zoneinfo import ZoneInfo
    _PACIFIC = ZoneInfo("America/Los_Angeles")
except Exception:
    # Fallback: fixed UTC-7 (PDT). Correct for Berkeley Apr–Oct.
    _PACIFIC = timezone(timedelta(hours=-7))

_START = _time(8, 0)
_END   = _time(17, 0)


def next_business_send_time():
    """Return None if currently in business hours (send immediately).
    Otherwise return a UTC datetime for the next business day at 8 AM PT.
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
