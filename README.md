# ff3-analyzer

A quantitative finance project that applies the Fama-French 3-Factor Model to a portfolio of 11 US equities using monthly return data from 2020–2024. Includes OLS regression analysis, factor exposure visualizations, and an interactive Streamlit dashboard.

---

## What is the Fama-French Model?

The Fama-French 3-Factor Model extends CAPM by explaining stock returns through three systematic risk factors:

- **Market (MKT-RF)** — excess return of the market over the risk-free rate
- **Size (SMB)** — Small Minus Big, captures the size premium
- **Value (HML)** — High Minus Low, captures the value premium

The model is expressed as:

```
R_i - R_f = α + β₁(MKT-RF) + β₂(SMB) + β₃(HML) + ε
```

---

## Project Structure

```
ff3-analyzer/
├── data/                   # raw stock prices and FF factor CSVs
├── src/
│   ├── data_fetcher.py     # downloads stock prices and FF factors
│   ├── preprocessing.py    # cleans, aligns, and merges data
│   ├── regression.py       # OLS regression for each stock
│   └── visualize.py        # factor exposure plots
├── frontend/
│   └── dashboard.py        # Streamlit interactive dashboard
├── results/                # regression summary CSV and plots
└── requirements.txt
```

---

## Data Sources

- **Stock prices** — Yahoo Finance via `yfinance` (2020–2024, monthly)
- **Fama-French factors** — [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) via `pandas-datareader`

---

## Portfolio

`AAPL` `AMZN` `GOOGL` `META` `TSLA` `MSFT` `JNJ` `JPM` `XOM` `PG` `KO`

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| pandas, numpy | Data manipulation |
| yfinance | Stock price data |
| pandas-datareader | Fama-French factor data |
| statsmodels | OLS regression |
| matplotlib, seaborn | Visualizations |
| Streamlit | Interactive dashboard |

---

## Pipeline

```
data_fetcher.py → preprocessing.py → regression.py → visualize.py → dashboard.py
```

1. **Fetch** — download raw stock prices and FF factor data
2. **Preprocess** — compute monthly returns, align date indices, merge into a single dataframe
3. **Regression** — run OLS for each stock, extract alpha, betas, R², p-values
4. **Visualize** — generate factor heatmap, alpha bars, R² bars, rolling beta plots
5. **Dashboard** — interactive Streamlit app for stock exploration, comparison, and portfolio construction

---

## Setup

### Option 1 — Live Demo

[Click here to view the dashboard](https://ff3-analyzer.streamlit.app/)

### Option 2 — Run Locally

1. Clone the repository

```bash
git clone https://github.com/yourusername/ff3-analyzer.git
cd ff3-analyzer
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the full pipeline

```bash
python src/data_fetcher.py
python src/preprocessing.py
python src/regression.py
```

4. Launch the dashboard

```bash
streamlit run frontend/dashboard.py
```

---

## Key Findings

| Ticker | Market Beta | SMB Beta | HML Beta | R² |
|--------|-------------|----------|----------|----|
| AAPL   | 1.14        | -0.11    | -0.41    | 56.2% |
| AMZN   | 1.15        | 0.09     | -0.94    | 63.6% |
| TSLA   | 2.09        | 1.80     | -1.36    | 51.4% |
| JPM    | 1.09        | 0.14     | 0.71     | 73.9% |
| XOM    | 0.83        | -0.11    | 1.22     | 52.7% |
| JNJ    | 0.49        | -0.26    | 0.32     | 27.7% |

- **No stock produced statistically significant alpha** — consistent with the efficient market hypothesis
- **TSLA** is the most aggressive stock — twice the market volatility, strong small-cap behavior despite its size
- **Growth vs Value split is clear** — tech stocks (AAPL, AMZN, MSFT, META) load negatively on HML while energy and financials (XOM, JPM) load positively
- **JNJ** is the most defensive stock with the lowest market beta (0.49) and lowest R² (27.7%)
- **JPM** has the highest R² (73.9%) — its returns are most explained by systematic factors
- **Rolling beta analysis** reveals AAPL's market sensitivity is time-varying, dropping sharply during the 2022 rate hike cycle

---

## Acknowledgements

- [Fama & French (1992)](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1992.tb04398.x) — The Cross-Section of Expected Stock Returns
- [Ken French's Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) — FF factor data
- [yfinance](https://github.com/ranaroussi/yfinance) — stock price data

---

## License

MIT License — free to use and modify.
