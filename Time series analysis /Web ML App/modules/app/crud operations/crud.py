import models
from sqlalchemy.orm import Session
from datetime import date

#read all prices for AAPL from the table 'aapls'
def get_all_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AAPL).offset(skip).limit(limit).all()

#read a single price from the AAPL table filtered by date parameter (DateTime.date)

def get_one_price(db: Session, Filter_date: date):
    return db.query(models.AAPL).filter(models.AAPL.date_id == Filter_date).first()

#read all predictions from Predict table

def get_all_predictions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Prediction).offset(skip).limit(limit).all()

#read one prediction from Predct table filtered by date

def get_one_prediction(db: Session, Filter_date: date):
    return db.query(models.Prediction).filter(models.Prediction.date_id == Filter_date).all()

#read one prediction from the Prediction table filtered by date and ticker parameters

def get_prediction_filtered(db: Session, Filter_date: date, Filter_ticker: str):
    return db.query(models.Prediction).filter(models.Prediction.date_id == Filter_date, models.Prediction.ticker == Filter_ticker).first()