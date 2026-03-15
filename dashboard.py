import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
plt.style.use('dark_background')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
sys.path.append(os.path.join(BASE_DIR, 'src'))
from visualize import plot_rolling_betas

combined = pd.read_csv(os.path.join(BASE_DIR, 'src', 'preprocessed_data.csv'), index_col=0)
combined.index = pd.to_datetime(combined.index)

tickers_list = ['AAPL', 'AMZN', 'GOOGL', 'META', 'TSLA', 'MSFT', 'JNJ', 'JPM', 'XOM', 'PG', 'KO']

summary = pd.read_csv(os.path.join(RESULTS_DIR, 'regression_summary.csv'), index_col=0)

st.set_page_config(
    page_title='FF3 Dashboard',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded'
)
st.title('Fama French 3-Factor Model Dashboard')
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #010b01;
    color: #00ff41;
}

h1 { 
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.8rem;
    color: #00ff41;
    letter-spacing: 2px;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff4188;
    border-bottom: 1px solid #00ff4133;
    padding-bottom: 0.5rem;
}

h2, h3 {
    font-family: 'Share Tech Mono', monospace;
    color: #00cc33;
    font-size: 0.9rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 0 0 6px #00ff4166;
}

[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.8rem;
    color: #00ff41;
    text-shadow: 0 0 8px #00ff41;
}

[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #007a1f;
    text-transform: uppercase;
    letter-spacing: 2px;
}

[data-testid="stSidebar"] {
    background-color: #000a00;
    border-right: 1px solid #00ff4122;
}

.stRadio label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #00cc33;
    letter-spacing: 1px;
}

.stSelectbox label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #007a1f;
    text-transform: uppercase;
}

.stMarkdown p {
    color: #00cc33;
    font-family: 'Share Tech Mono', monospace;
    line-height: 1.8;
}

/* scanline overlay */
body::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 255, 65, 0.03) 2px,
        rgba(0, 255, 65, 0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## FF3 Dashboard")
st.sidebar.markdown("---")
page = st.sidebar.radio("", ['Stock Explorer', 'Portfolio Builder', 'Stock Comparison'])
st.sidebar.markdown("---")
st.sidebar.markdown("*Fama-French 3-Factor Model*")
st.sidebar.markdown("*Data: 2020 – 2026*")

if(page=='Stock Explorer'):
    ticker = st.selectbox('Select a stock', summary.index.tolist())
    st.subheader(f'{ticker} — Factor Analysis')

    row = summary.loc[ticker]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Alpha (monthly)', f"{row['Alpha']*100:.2f}%")
    col2.metric('Market Beta', f"{row['Beta_MKT']:.2f}")
    col3.metric('R²', f"{row['R_squared']*100:.1f}%")
    col4.metric('SMB Beta', f"{row['Beta_SMB']:.2f}")
    st.dataframe(summary.loc[[ticker]])
    
    st.subheader('Factor Exposures')
    betas = pd.Series({
        'Market (MKT-RF)': row['Beta_MKT'],
        'Size (SMB)': row['Beta_SMB'],
        'Value (HML)': row['Beta_HML']
    })
    st.bar_chart(betas)

    st.subheader('What does this mean?')
    

    st.markdown(f"""
    - **Market Sensitivity:** {ticker} has a market beta of **{row['Beta_MKT']:.2f}**. 
    {'This means it moves *more* than the market — higher risk, higher potential reward.' if row['Beta_MKT'] > 1 else 'This means it moves *less* than the market — relatively defensive.'}

    - **Size:** A SMB beta of **{row['Beta_SMB']:.2f}** means {ticker} behaves like a 
    {'small-cap stock — higher growth potential but more volatile.' if row['Beta_SMB'] > 0 else 'large-cap stock — more stable and established.'}

    - **Value vs Growth:** A HML beta of **{row['Beta_HML']:.2f}** means {ticker} is a 
    {'value stock — priced cheaply relative to its fundamentals.' if row['Beta_HML'] > 0 else 'growth stock — the market expects strong future earnings.'}

    - **Model Fit:** The three factors explain **{row['R_squared']*100:.1f}%** of this stock\'s returns.

    - **Alpha:** {ticker} generates **{row['Alpha']*100:.2f}%** monthly excess return unexplained by the factors. 
    {'This is statistically significant.' if row['Alpha_pval'] < 0.05 else 'This is not statistically significant.'}
    """)

    st.subheader('Rolling 12-Month Market Beta')
    plot_rolling_betas(combined, ticker)
    st.pyplot(plt)

elif(page == 'Stock Comparison'):
    col1, col2 = st.columns(2)
    ticker1 = col1.selectbox('Select first stock', summary.index.tolist())
    ticker2 = col2.selectbox('Select second stock', summary.index.tolist(), index=1)

    st.subheader('Factor Comparison')
    comparison = summary.loc[[ticker1, ticker2], ['Beta_MKT', 'Beta_SMB', 'Beta_HML', 'R_squared', 'Alpha']]
    st.dataframe(comparison)

    # grouped bar chart
    fig, ax = plt.subplots(figsize=(8, 4))
    x = np.arange(3)
    width = 0.35
    factors = ['Beta_MKT', 'Beta_SMB', 'Beta_HML']
    labels = ['Market', 'Size (SMB)', 'Value (HML)']

    ax.bar(x - width/2, summary.loc[ticker1, factors], width, label=ticker1)
    ax.bar(x + width/2, summary.loc[ticker2, factors], width, label=ticker2)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.axhline(0, color='white', linewidth=0.5)
    ax.legend()
    ax.set_title('Factor Exposure Comparison')
    st.pyplot(fig)

    # plain English
    st.subheader('Interpretation')
    for t in [ticker1, ticker2]:
        r = summary.loc[t]
        st.markdown(f"""
        **{t}** — {'More volatile than market' if r['Beta_MKT'] > 1 else 'Less volatile than market'}, 
        {'growth stock' if r['Beta_HML'] < 0 else 'value stock'}, 
        model explains {r['R_squared']*100:.1f}% of returns.
        """)

    st.subheader('Factor Heatmap')
    comparison_betas = summary.loc[[ticker1, ticker2], ['Beta_MKT', 'Beta_SMB', 'Beta_HML']]    
    fig, ax = plt.subplots(figsize=(6, 3))
    sns.heatmap(comparison_betas, annot=True, fmt='.2f', cmap='RdYlGn', center=0, ax=ax)
    plt.tight_layout()
    st.pyplot(fig)

elif(page == 'Portfolio Builder'):
    st.subheader('Build Your Portfolio')
    st.write('Assign weights to each stock')

    weights = {}
    cols = st.columns(3)
    for i, ticker in enumerate(summary.index.tolist()):
        weights[ticker] = cols[i % 3].number_input(ticker, min_value=0.0, value=0.0, step=1.0)

    total = sum(weights.values())

    if total == 0:
        st.warning('Enter at least one non-zero weight.')
    else:
        normalized = {t: w / total for t, w in weights.items()}
        st.success(f'Weights normalized. Total entered: {total:.0f}')
        st.dataframe(pd.DataFrame.from_dict(normalized, orient='index', columns=['Weight']).T)

        portfolio_beta_mkt = sum(normalized[t] * summary.loc[t, 'Beta_MKT'] for t in tickers_list)
        portfolio_beta_smb = sum(normalized[t] * summary.loc[t, 'Beta_SMB'] for t in tickers_list)
        portfolio_beta_hml = sum(normalized[t] * summary.loc[t, 'Beta_HML'] for t in tickers_list)
        portfolio_alpha = sum(normalized[t] * summary.loc[t, 'Alpha'] for t in tickers_list)

        st.subheader('Portfolio Factor Exposure')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Portfolio Alpha', f"{portfolio_alpha*100:.2f}%")
        col2.metric('Market Beta', f"{portfolio_beta_mkt:.2f}")
        col3.metric('SMB Beta', f"{portfolio_beta_smb:.2f}")
        col4.metric('HML Beta', f"{portfolio_beta_hml:.2f}")

        st.subheader('Portfolio Summary')
        st.markdown(f"""
        - Your portfolio is **{'more aggressive' if portfolio_beta_mkt > 1 else 'more defensive'}** than the market (Beta: {portfolio_beta_mkt:.2f})
        - It has a **{'growth' if portfolio_beta_hml < 0 else 'value'}** tilt (HML: {portfolio_beta_hml:.2f})
        - It behaves more like a **{'large-cap' if portfolio_beta_smb < 0 else 'small-cap'}** portfolio (SMB: {portfolio_beta_smb:.2f})
        - Expected monthly alpha: **{portfolio_alpha*100:.2f}%** above what the factors explain
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #007a1f; font-family: Share Tech Mono, monospace; font-size: 0.8rem;'>Built by Shaurya</p>", unsafe_allow_html=True)