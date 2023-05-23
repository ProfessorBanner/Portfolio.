import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, MetaData, DateTime, Date, Numeric

from database import Base
# Instantiate a class for the table to store stock prices (AAPL ticker)
class AAPL(Base):
    __tablename__ = "aapls"

    date_id = Column(Date(), primary_key=True, index=True, nullable=False)
    open = Column(Float())
    high = Column(Float())
    low = Column(Float())
    close = Column(Float())
    adjclose = Column(Float())
    volume = Column(Integer())


# Instantiate a class for the table to store price predictions

class Prediction(Base):
    __tablename__ = "predictions"

    date_id = Column(Date(), primary_key=True, index=True, unique=False, nullable=False)
    predict = Column(Integer())
    ticker = Column(String(), primary_key=True)
