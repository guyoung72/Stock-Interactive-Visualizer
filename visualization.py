import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# User Interaction program
ticker_input = input("Stock Ticker: ")
ticker_input = ticker_input.upper()

data = yf.download(tickers=ticker_input, period="3y", interval="1d")

fig = go.Figure()
fig.add_trace(go.Candlestick())
fig.add_trace(go.Candlestick(open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))

fig.update_layout(title = ticker_input + ' share price', yaxis_title = 'Stock Price (USD)')

fig.show()