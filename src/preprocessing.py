import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


tickers = ['AAPL', 'AMZN', 'GOOGL', 'META', 'TSLA', 'MSFT', 'JNJ', 'JPM', 'XOM', 'PG', 'KO']

def preprocess():
    stock_data = {}
    for ticker in tickers:
        df = pd.read_csv(os.path.join(DATA_DIR, f'{ticker}.csv'), skiprows=[1,2], index_col=0)
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        stock_data[ticker] = df

    monthly_returns_list = []
    for ticker, df in stock_data.items():
        monthly_price = df['Close'].resample('ME').last()
        monthly_return = monthly_price.pct_change()
        monthly_return.name = ticker
        monthly_returns_list.append(monthly_return)

    stock_returns_df = pd.concat(monthly_returns_list, axis=1)
    stock_returns_df.index = pd.to_datetime(stock_returns_df.index)
    stock_returns_df.index = stock_returns_df.index + pd.offsets.MonthEnd(0)


    ff_factors = pd.read_csv(os.path.join(DATA_DIR, 'fama_french_factors_2020-01-01.csv'), index_col=0)
    ff_factors.index = pd.to_datetime(ff_factors.index)
    ff_factors.index = ff_factors.index + pd.offsets.MonthEnd(0)
    ff_factors.index.name = 'Date'

    combined = pd.concat([stock_returns_df, ff_factors], axis=1)
    combined = combined.dropna()
    ff_cols = ['Mkt-RF', 'SMB', 'HML', 'RF']
    combined[ff_cols] = combined[ff_cols] / 100
    combined.to_csv('preprocessed_data.csv', index=True)  
    return combined

if __name__ == "__main__":
    combined = preprocess()
    print("Preprocessing complete\n")
    df = pd.read_csv('preprocessed_data.csv', index_col=0)
    print(df.shape)
    print(df.head())
    