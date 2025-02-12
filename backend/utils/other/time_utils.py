from datetime import datetime, timedelta


def current_time():
    return datetime.utcnow() + timedelta(hours=3)
