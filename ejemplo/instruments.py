from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Ticker:
    name: str
    cash_asigned: float


