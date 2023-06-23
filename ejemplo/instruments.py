from dataclasses import dataclass

@dataclass
class Ticker:
    name :str
    cash_asigned : float

dlr_ene_24 = Ticker(name='DLR/ENE24', cash_asigned=10_000)

