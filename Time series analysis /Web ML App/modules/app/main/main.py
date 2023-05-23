'''And now in the file sql_app/main.py let's integrate and use all the other parts we created before.'''
import datetime
from datetime import date
import crud
import models
import schemas
from database import engine, SessionLocal
from fastapi import Depends, FastAPI, HTTPException, Request, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory='templates/')


'''New dependency to create a new SQLAlchemy SessionLocal that is used in requests,
 and then close the session when the request is done.'''

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# API to get all prices from the table AAPL in the database
@app.get("/Prices_all/", response_model=list[schemas.AAPL])
def read_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = crud.get_all_prices(db, skip=skip, limit=limit)
    return prices

#  API  to retrieve one price from the database table AAPL, filtered by date parameter

@app.get("/Prices/{Filter_date}", response_model=schemas.AAPL)
def read_price(Filter_date: date, db: Session = Depends(get_db)):
    price = crud.get_one_price(db, Filter_date=Filter_date)
    if price is None:
        raise HTTPException(status_code=404, detail="Price is not found")
    return price


# API to retrieve all predictions from Predict table


@app.get("/Predictions_all/", response_model=list[schemas.Prediction])
def read_predictions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    result = crud.get_all_predictions(db, skip=skip, limit=limit)
    return result

# API to retrieve a single prediction from Predict table, filtered by date parameter

@app.get("/Predictions_all/{Filter_date}", response_model=list[schemas.Prediction])
def read_prediction(Filter_date: date, db: Session = Depends(get_db)):
    prediction = crud.get_one_prediction(db, Filter_date=Filter_date)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction is not found")
    return prediction

# API to retrieve a single prediction from Predict table, filtered by date and ticker parameters

@app.get("/Predictions_filtered", response_model=schemas.Prediction)
def read_prediction_filtered(Filter_date: date, Filter_ticker : str, db: Session = Depends(get_db)):
    prediction = crud.get_prediction_filtered(db, Filter_date=Filter_date, Filter_ticker=Filter_ticker)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction is not found")
    return prediction


#API to get price filtered by date parameter using HTML form request and HTML form for response

@app.get('/form2')
def form_post(request: Request):
    result = ''
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})

@app.post('/form2', response_model=schemas.Prediction)
def form_post(request: Request, Filter_date: date = Form(...), Filter_ticker: str = Form(...), db: Session = Depends(get_db)):
    result = crud.get_prediction_filtered(db, Filter_date=Filter_date, Filter_ticker=Filter_ticker)
    return templates.TemplateResponse('form2.html', context={'request': request,
                                                            'Filter_date': result.date_id,
                                                            'Filter_ticker': result.ticker,
                                                            'result': result.predict})


# API to download serialized models trained today
model_date = datetime.datetime.now().strftime("%Y%m%d")

#file_path = "api/app/serializedmodels/" + model_date
file_path = "serializedmodels/" + model_date

@app.get("/get_ser_model")
async def main():
    return FileResponse(file_path)




# Swagger documentation at http://127.0.0.1:8000/docs
# And at http://127.0.0.1:8000/redoc
