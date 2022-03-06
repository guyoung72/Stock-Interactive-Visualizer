import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# Test Case - SPY 5d5m
data = yf.download(tickers="SPY", period="3y", interval="1d")

fig = go.Figure()
fig.add_trace(go.Candlestick())
fig.add_trace(go.Candlestick(open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))

fig.update_layout(title = 'SPY share price', yaxis_title = 'Stock Price (USD)')

fig.show()