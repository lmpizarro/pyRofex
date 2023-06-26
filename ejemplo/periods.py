from datetime import datetime, timedelta, date
from dataclasses import dataclass
from config import Config


def by_days(days=5, end: date=datetime.now().date()):
    dates = []
    delta_dates = 0
    count_dates = 0
    while delta_dates < days:
        current_date = end - timedelta(days=count_dates)
        if current_date.isoweekday() in [1, 2, 3, 4, 5]:
            delta_dates += 1
            dates.append(current_date)
        count_dates += 1
    return (dates[0], dates[-1])


if __name__ == '__main__':
    by_days()
