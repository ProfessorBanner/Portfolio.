from pydantic import BaseModel
from typing import Union
from datetime import date


class AAPL(BaseModel):
    date_id: date
    open: float
    high: float
    low: float
    close: float
    adjclose: float
    volume: int

    class Config:
        orm_mode = True


class Prediction(BaseModel):
    date_id: date
    predict: int
    ticker: str


    class Config:
        orm_mode = True
