import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import matplotlib.dates as mdates
import os


tickers = ['AAPL', 'AMZN', 'GOOGL', 'META', 'TSLA', 'MSFT', 'JNJ', 'JPM', 'XOM', 'PG', 'KO']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

def plot_factor_heatmap(summary_df: pd.DataFrame):
    betas = summary_df[['Beta_MKT', 'Beta_SMB', 'Beta_HML']]

    plt.figure(figsize=(10, 6))
    sns.heatmap(betas, annot=True, cmap='viridis', center=0)
    plt.title('Factor Exposures Heatmap')
    plt.savefig(os.path.join(RESULTS_DIR, 'factor_exposures_heatmap.png'))
    plt.show()

def plot_alpha_bars(summary_df: pd.DataFrame):

    colors = ['green' if val > 0 else 'red' for val in summary_df['Alpha']]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=summary_df.index, y='Alpha', data=summary_df, palette=colors)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.title('Alpha Values by Stock')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(RESULTS_DIR, 'alpha_bars.png'))
    plt.tight_layout()
    plt.show()

def plot_r_squared(summary_df: pd.DataFrame):
    plt.figure(figsize=(10,6))
    sns.barplot(x=summary_df.index, y='R_squared', data=summary_df, palette='Blues_d')
    plt.title('R-squared Values by Stock')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(RESULTS_DIR, 'r_squared_bars.png'))
    plt.tight_layout()
    plt.show()

def plot_rolling_betas(combined: pd.DataFrame, ticker: str, window: int = 12):
    plt.style.use('dark_background')
    results = []
    for i in range(window, len(combined)+1):
        chunk = combined.iloc[i-window:i]
        y = chunk[ticker] - chunk['RF']
        X = sm.add_constant(chunk[['Mkt-RF', 'SMB', 'HML']])
        model = sm.OLS(y,X).fit()
        results.append({
            'Date': combined.index[i - 1],
            'Beta_MKT': model.params['Mkt-RF']
        })
    
    rolling_df = pd.DataFrame(results).set_index('Date')
    rolling_df.index = pd.to_datetime(rolling_df.index)
    plt.figure(figsize=(12, 5))
    plt.plot(rolling_df.index, rolling_df['Beta_MKT'], linewidth=2)
    plt.axhline(1, color='red', linestyle='--', linewidth=0.8, label='Beta = 1')
    plt.title(f'Rolling 12-Month Market Beta — {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Beta_MKT')
    plt.legend()
    plt.gca().xaxis.set_major_locator(mdates.YearLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, f'rolling_beta_{ticker}.png'))

if __name__ == "__main__":
    combined = pd.read_csv(os.path.join(BASE_DIR, 'src', 'preprocessed_data.csv'), index_col=0)

    for ticker in tickers:
        plot_rolling_betas(combined, ticker, window=12)