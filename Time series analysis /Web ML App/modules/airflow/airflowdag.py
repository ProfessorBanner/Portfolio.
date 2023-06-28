from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import Date, create_engine
from datetime import datetime
import pandas as pd
import yfinance as yf

# DB credentials
DATABASE_URL = 'postgresql://postgres:postgres@localhost/test'
engine = create_engine(DATABASE_URL)

# Tickers list
tickers = ['AAPL']

selected_col = [('Open', 'AAPL'),
                ('High', 'AAPL'),
                ('Low', 'AAPL'),
                ('Volume', 'AAPL')
               ]

def fetch_prices():
    print('Fetching and preprocessing data')
    df = yf.download(tickers, start="2010-01-01", end="2023-04-30")
    df.rename(columns={'Open': 'open',
                       'High': 'high',
                       'Low': 'low',
                       'Close': 'close',
                       'Adj Close': 'adjclose',
                       'Volume': 'volume'
                       }, inplace=True)
    df.index.names = ['date_id']
    df.dropna(inplace=True)
    df = df.pct_change()
    df = df.drop(df.index[0])
    data = df.append(df)
    return data

def prices_upload_function():
    print('Inserting data into the database')
    data = fetch_prices()
    data.to_sql('aapls', dtype={'date_id': Date}, con=engine, if_exists='append')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['user@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG('download_prices_23PM',
          default_args=default_args,
          description='Fetch prices for DB update',
          catchup=False,
          start_date=datetime(2023, 4, 1),
          schedule_interval='0 23 * * *'  # Run at 23:00 every day
          )

fetch_prices_task = PythonOperator(task_id='fetch_prices_task',
                                   python_callable=fetch_prices,
                                   dag=dag)

upload_prices_task = PythonOperator(task_id='upload_prices_task',
                                    python_callable=prices_upload_function,
                                    dag=dag)

fetch_prices_task >> upload_prices_task
