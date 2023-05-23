from airflow import DAG
from airflow.operators.python import PythonOperator
from sqlalchemy import Date, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import yfinance as yf


# DB credentials
DATABASE_URL = 'postgresql://postgres:postgres@localhost/test'
engine = create_engine(DATABASE_URL)

# Tickers list
tickers = ['AAPL']

selected_col = [('Open',  'AAPL'),
                ('High',  'AAPL'),
                ('Low',  'AAPL'),
                ('Volume',  'AAPL')
               ]

''' Defining our functions for DAG'''


def fetch_prices(**kwargs):
    print(' Preprocessing fetched data')
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
    return data  # <-- This list is the output of the fetch_prices_function and the input for the functions below
    print('Completed fetching and preprocessing')

def prices_upload_function(**kwargs):
    print('Pulling dataframe to insert into our database')
    data = ti.xcom_pull(task_ids='fetch_prices_task') # <-- xcom_pull is used to pull the stocks_prices dataframe
    data.to_sql('aapls', dtype={'date_id': Date}, con=engine, if_exists='append')


# 2. DEFINE AIRFLOW DAG

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
          schedule='* 23 * * *'
          )

# 3. DEFINE AIRFLOW OPERATORS


fetch_prices_task = PythonOperator(task_id='fetch_prices_task',
                                   python_callable=fetch_prices,
                                   dag=dag)

upload_prices_task = PythonOperator(task_id='upload_prices_task',
                                  python_callable=prices_upload_function,
                                  dag=dag)


# 4. DEFINE OPERATORS HIERARCHY


fetch_prices_task >> upload_prices_task