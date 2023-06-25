from datetime import datetime, timedelta
from dataclasses import  dataclass
from config import Config

def period(days = 5):
    end = datetime.now().date()
    dates = []
    n = 0
    m = 0
    while n < 5:
        current_date = end - timedelta(days=m)
        if current_date.isoweekday() in [1,2,3,4,5]:
            n += 1
            dates.append(current_date)
        m += 1
    return (dates[0], dates[-1])

if __name__ == '__main__':
    period()







