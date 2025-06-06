from datetime import datetime

from pydantic import BaseModel


class CurrencyBase(BaseModel):
    name: str
    code: str
    mid: float
    date: datetime
