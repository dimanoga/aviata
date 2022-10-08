import datetime


def get_expire_timestamp() -> float:
    date = datetime.datetime.utcnow()
    date = date + datetime.timedelta(days=1)
    time = datetime.time(hour=12, minute=00)
    tomorrow = datetime.datetime.combine(date, time)
    return tomorrow.timestamp()
