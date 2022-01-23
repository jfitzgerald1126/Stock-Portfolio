import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# create list with stock tickers
ticker_list = pd.read_csv(
    'https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')

tickers = st.multiselect("Select your stocks:", ticker_list, ["AAPL", 'MSFT'])

if not tickers:
    st.error("Please select at least one country.")
else:
    periods = ['1mo', '6mo', '1y', '5y', 'ytd', 'max']
    period = st.sidebar.selectbox('Period', periods, index=2)
    figs = {}

    total_so_far = yf.Ticker(tickers[0]).history(interval='1d', period=period)['Close']
    for i in range(len(tickers)):
        hist = yf.Ticker(tickers[i]).history(interval='1d', period=period)
        total_so_far = total_so_far.add(hist['Close'])
        fig = go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name=tickers[i])

        figs[tickers[i]] = fig

    tickerSymbol = st.sidebar.selectbox('Stock ticker', tickers)
    show_all = st.sidebar.checkbox('Show all?')
    fig = go.Figure()
    if show_all:
        total_fig = go.Scatter(
            x=total_so_far.index,
            y=total_so_far, mode='lines',
            name='Total Value'

        )
        fig.add_trace(total_fig)

        for ticker in figs:
            fig.add_trace(figs[ticker])
    else:
        fig.add_trace(figs[tickerSymbol])

    fig.update_layout(
        title="Closing Stock Price",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        legend_title="Stocks",
    )

    st.plotly_chart(fig, use_container_width=True)

    data = yf.Ticker(tickerSymbol).info

    st.header('%s Info' % data['longName'])
    st.markdown('<img src=%s>' % data['logo_url'], unsafe_allow_html=True)

    st.write('Website: %s' % data['website'])
    st.write('Current price: %s' % data['currentPrice'])
    st.write('Sector: %s' % data['sector'])
    st.write('Summary: %s' % data['longBusinessSummary'])
