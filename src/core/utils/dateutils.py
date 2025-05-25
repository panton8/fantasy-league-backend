
from datetime import date, datetime, timedelta


def gmt3_date_to_utc_dtm(gmt3_date: date) -> datetime:
    return datetime.combine(gmt3_date, datetime.min.time()) - timedelta(hours=3)


def utc_dtm_to_gmt3_dtm(utc_dtm: datetime) -> datetime:
    return utc_dtm + timedelta(hours=3)
