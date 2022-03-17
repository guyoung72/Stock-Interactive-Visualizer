import numpy as np
# import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# User Interaction program
ticker_input = input("Stock Ticker: ")
ticker_input = ticker_input.upper()

"""
Timeframe Options:

    Period = 1d, 3d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    Interval = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
"""

# Data with various period and interval
data_1d5m = yf.download(tickers=ticker_input, period="1d", interval="5m")
data_3d5m = yf.download(tickers=ticker_input, period="3d", interval="5m")
data_3d1d = yf.download(tickers=ticker_input, period="3d", interval="1d")
data_6mo1d = yf.download(tickers=ticker_input, period="6mo", interval="1d")


# Draw figure
fig = go.Figure(data=[go.Candlestick(x=data_6mo1d.index,
                                     open=data_6mo1d['Open'],
                                     high=data_6mo1d['High'],
                                     low=data_6mo1d['Low'],
                                     close=data_6mo1d['Close'])])


# Set background colors grid_color="rgb(36,38,49)"
fig.update_layout(plot_bgcolor='rgb(25,28,38)',
                  xaxis={'gridcolor': 'rgb(36,38,49)'},
                  yaxis={'gridcolor': 'rgb(36,38,49)'})


# Set candle colors
increasing_color = 'rgb(82, 164, 154)'
decreasing_color = 'rgb(221,94,86)'

fig.data[0].increasing.fillcolor = increasing_color
fig.data[0].increasing.line.color = increasing_color
fig.data[0].decreasing.fillcolor = decreasing_color
fig.data[0].decreasing.line.color = decreasing_color


# Remove weekends
fig.update_xaxes(
    rangebreaks=[
        dict(bounds=["sat", "mon"])
    ]
)

# Show chart
fig.show()
