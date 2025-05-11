
from datetime import date, datetime, timedelta


def gmt3_date_to_utc_dtm(gmt3_date: date) -> datetime:
    return datetime.combine(gmt3_date, datetime.min.time()) - timedelta(hours=3)
