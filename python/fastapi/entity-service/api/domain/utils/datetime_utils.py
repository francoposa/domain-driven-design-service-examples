import datetime


def datetime_now_with_utc_timezone() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)
