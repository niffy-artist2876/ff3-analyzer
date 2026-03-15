import yfinance
from pandas_datareader import data as web
import os
import pandas


def save_fama_french():
    startDate = '2020-01-01'
    path = f'fama_french_factors_{startDate}.csv'
    ff_factors = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start='2020-01-01')[0]
    if (not os.path.exists(path)):
        ff_factors.to_csv(f'{path}', index=True)
    return ff_factors

ticker_hashmap = {}
tickers = ['AAPL', 'AMZN', 'GOOGL', 'META', 'TSLA', 'MSFT', 'JNJ', 'JPM', 'XOM', 'PG', 'KO']

def get_data():
    startDate = '2020-01-01'
    global ticker
    global ticker_hashmap
    for ticker in tickers:
        data = yfinance.download(ticker, startDate)
        ticker_hashmap[ticker] = data
    return ticker_hashmap

def save_stock_data():
    get_data()
    global ticker_hashmap
    for ticker, df in ticker_hashmap.items():
        df.to_csv(f'{ticker}.csv', index=True)
    
if __name__ == "__main__":
    try:
        save_stock_data()
        print("Stock data saved!")
    except Exception as e:
        print(f"An error occurred: {e}\n")
    
    try:
        save_fama_french()
        print("Fama French data saved!")
    except Exception as e:
        print(f"An error occurred: {e}")

