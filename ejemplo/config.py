import pytz
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    project_tz = pytz.timezone('America/Argentina/Buenos_Aires')