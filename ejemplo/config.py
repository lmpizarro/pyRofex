import pytz
from dataclasses import dataclass
import pyRofex
from decouple import config
from instruments import Ticker


@dataclass(frozen=True)
class Config:
    project_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    user = config('NAME')
    password = config('PASS')
    account = config('ACCOUNT')
    environment = pyRofex.Environment.REMARKET
    rofex_ggal_ago23 = Ticker(name='GGAL/AGO23', cash_asigned=10_000)
    rofex_entries = [pyRofex.MarketDataEntry.BIDS,
                     pyRofex.MarketDataEntry.OFFERS,
                     pyRofex.MarketDataEntry.LAST]

    # 1-Initialize the environment
    pyRofex.initialize(
        user=user,
        password=password,
        account=account,
        environment=pyRofex.Environment.REMARKET)
