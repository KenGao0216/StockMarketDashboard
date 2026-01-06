from pydantic import BaseModel
from typing import List

class Quote(BaseModel):
    symbol: str
    price: float
    change: float
    change_percent: float
    as_of: str

class HistoryPoint(BaseModel):
    symbol: str
    date: str
    close: float

class HistorySeries(BaseModel):
    symbol: str
    points: List[HistoryPoint]
