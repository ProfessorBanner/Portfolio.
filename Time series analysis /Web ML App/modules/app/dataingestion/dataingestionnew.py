'''Module to automate ETL procedures to populate the database tables, using SQLAchemy ORM paradigm'''

import yfinance as yf
import pandas as pd
import datetime
from sqlalchemy import Date, create_engine
from sqlalchemy.orm import sessionmaker
from database import engine
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

import joblib
import pickle
from pathlib import Path


DATABASE_URL = 'postgresql://postgres:postgres@localhost/test'
#DATABASE_URL = 'postgresql://postgres:postgres@webdb/test'

engine = create_engine(DATABASE_URL)


# Download price data as pd.DataFrame using yfinance API
df_aapl = yf.download(tickers = "AAPL ",  # list of tickers
            period = "10y",         # time period
            interval = "1d",       # trading interval
            prepost = False,       # download pre/post market hours data?
            repair = True)         # repair obvious price errors e.g. 100x?


# Rename columns
df_aapl.rename(columns={'Open' : 'open',
                        'High' : 'high',
                        'Low' : 'low',
                        'Close' : 'close',
                        'Adj Close':'adjclose',
                        'Volume' : 'volume'
                        }, inplace=True)
df_aapl.index.names = ['date_id']

#Upload data to the relevant database table

#df_aapl.to_sql('aapls', dtype={'date_id': Date}, con=engine, if_exists='append')


'''Download data for training ML models (predicting AAPL price for the next day) as pd.DataFrame using yfinance API'''

# Download the dataset
df = yf.download("SPY AAPL CHF=X ^TNX ^VIX", start="2010-01-01", end="2023-04-30")

# Select features
selected_col = [('Open',  'AAPL'),
                ('High',  'AAPL'),
                ('Low',  'AAPL'),
                ('Volume',  'AAPL'),
                ('Adj Close',  'AAPL'),
                ('Adj Close',   'SPY'),
                ('Adj Close',   '^VIX'),
                ('Adj Close',   '^TNX'),
                ('Adj Close',   'CHF=X')
               ]
df = df[selected_col]

# Drop MultiIndex
df.columns = df.columns.map(''.join)

#Drop Nans

df.dropna(inplace=True)

# Feature engineering
df['Day'] = df.index.day
df['Weekday'] = df.index.weekday
df['Month'] = df.index.month
df['Year'] = df.index.year
df['Quarter'] = df.index.quarter

# Setting target

# Setting target
new_data = df[["Adj CloseAAPL"]]
new_data = new_data.rename(columns = {'Adj CloseAAPL':'Actual_Close'})

# Define the target variable, to  determine whether there was an increase or decrease in price
new_data["Target"] = df.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])["Adj CloseAAPL"]

# Shift forward
data_prev = df.copy()
data_prev = data_prev.shift(1)

#Our next step involves merging the target variable with the columns that we have chosen to predict the target
predictors = ['Adj CloseAAPL',
              'VolumeAAPL',
              'OpenAAPL',
              'HighAAPL',
              'LowAAPL',
              'Day',
              'Weekday',
              'Quarter',
              'Adj Close^VIX',
              'Adj Close^TNX',
              'Adj CloseSPY' ]
#new_data = new_data.merge(data_prev[predictors],left_index=False, right_index=False)
new_data= new_data.join(data_prev[predictors]).iloc[1:]

print(new_data.head())

''' Training baseline ML model '''
# Initialize a random forest classifier.  Set min_samples_split high to ensure we don't overfit.
model = RandomForestClassifier(n_estimators=100, min_samples_split=200, random_state=77)



# Train and test samples, fitting the model

train = new_data.iloc[:-100]
test = new_data.iloc[-100:]

model.fit(train[predictors], train["Target"]);

# Predictions
predictions = model.predict(test[predictors])
predictions = pd.Series(predictions, index=test.index)
print(precision_score(test["Target"], predictions))

# Get all predictions
predictions = model.predict(new_data.iloc[:,2:])

#predictions = pd.DataFrame(predictions) convert to DataFrame, merge with initial dataset and form a table for the SQLdb
predictions = pd.DataFrame(predictions)

new_data["Date_id"] = new_data.index
new_data.reset_index(drop=True, inplace=True )
new_data['predict'] = predictions
new_data['ticker'] = 'AAPL'
new_data.index = new_data['Date_id']
new_data.index.names = ['date_id']
del new_data['Date_id']
db_predictions_aapl = new_data[['predict','ticker']]
print(db_predictions_aapl.head(5))


#upload predictions to SQL database table Prediction
#db_predictions_aapl.to_sql('predictions', dtype={'date_id': Date}, con=engine, if_exists='append')


#Check that we can upload other tickers to the same table with the same dates without getting the error from the db
db_predictions_ibm = db_predictions_aapl
del db_predictions_ibm['ticker']
db_predictions_ibm['ticker'] = 'IBM'
db_predictions_ibm.to_sql('predictions', dtype={'date_id': Date}, con=engine, if_exists='append')
print(db_predictions_ibm.head())

# If we have predictions in .csv
#df_pred_aapls = pd.read_csv("path")
#df_pred_aapls.to_sql('predictions', dtype={'Date_id': Date}, con=engine, if_exists='append')



#Serializing our model using pickle

filename = datetime.datetime.now().strftime("%Y%m%d")

my_path = Path('serializedmodels/'+ filename)
with open(my_path, 'wb') as fp:
    pickle.dump(model, fp)

# my_path = Path('serializedmodels/'+ filename)
# with my_path.open('wb') as fp:
#     pickle.dump(model, fp)