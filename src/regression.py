import pandas as pd
import os
import statsmodels.api as sm


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

tickers = ['AAPL', 'AMZN', 'GOOGL', 'META', 'TSLA', 'MSFT', 'JNJ', 'JPM', 'XOM', 'PG', 'KO']

def run_regression(combined: pd.DataFrame) -> dict:
    
    regression_results = {}
    for ticker in tickers:
        y = combined[ticker] - combined['RF']
        X = combined[['Mkt-RF', 'SMB', 'HML']]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        regression_results[ticker] = model

    return regression_results

def save_results(results: dict) -> pd.DataFrame:
    rows = []
    for ticker, model in results.items():
        rows.append({
            'Ticker':    ticker,
            'Alpha':     model.params['const'],
            'Beta_MKT':  model.params['Mkt-RF'],
            'Beta_SMB':  model.params['SMB'],
            'Beta_HML':  model.params['HML'],
            'R_squared': model.rsquared,
            'Alpha_pval': model.pvalues['const'],
            'MKT_pval':  model.pvalues['Mkt-RF'],
            'SMB_pval':  model.pvalues['SMB'],
            'HML_pval':  model.pvalues['HML'],
        })
    
    summary_df = pd.DataFrame(rows).set_index('Ticker')
    os.makedirs(RESULTS_DIR, exist_ok=True)
    summary_df.to_csv(os.path.join(RESULTS_DIR, 'regression_summary.csv'))
    return summary_df

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(BASE_DIR, 'src', 'preprocessed_data.csv'), index_col=0)
    df.index = pd.to_datetime(df.index)
    results = run_regression(df)
    summary_df = save_results(results)
    print("\nSummary: \n", summary_df)
