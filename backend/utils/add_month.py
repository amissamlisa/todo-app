import datetime
from datetime import timedelta

def add_days(base_date: datetime.date, days: int) -> datetime.date:
    return base_date + timedelta(days=days)