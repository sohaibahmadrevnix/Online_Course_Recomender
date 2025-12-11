from datetime import datetime, timezone
def now_utc():
    return datetime.utcnow().replace(tzinfo=timezone.utc)
