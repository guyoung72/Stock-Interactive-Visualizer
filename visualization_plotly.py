import numpy as np
# import pandas as pd
import warnings
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
def chart_data(ticker, period, interval):
    return yf.download(tickers=ticker, period=period, interval=interval)


data_1d5m = chart_data(ticker_input, "1d", "5m")
data_3d5m = chart_data(ticker_input, "3d", "5m")
data_3d1d = chart_data(ticker_input, "3d", "1d")
data_6mo1d = chart_data(ticker_input, "6mo", "1d")


# Moving Average
def ma(input_data, period):
    ma_list = []
    close = input_data['Close'].to_list()
    for i in range(len(close)):
        if i < period - 1:
            ma_list.append(np.NAN)
        else:
            ma_list.append(round(np.nanmean(close[i - period + 1: i + 1]), 2))
    input_data['MA %s' % period] = ma_list
    return input_data['MA %s' % period]


# Exponential Moving Average (EMA)
def ema(input_data, period, smoothing):
    ema_list = []
    close = input_data['Close'].to_list()
    for i in range(len(close)):
        if i < period - 1:
            ema_list.append(np.NAN)
        elif i == period - 1:
            ema_list.append(round(np.nanmean(close[i - period + 1: i + 1]), 2))
        else:
            ema_list.append(round((close[i] * (smoothing / (1 + period)))
                                  + ema_list[-1] * (1 - (smoothing / (1 + period))), 2))
    input_data['EMA %s' % period] = ema_list
    return input_data['EMA %s' % period]


# Fast Stochastic %K
def stoch_k(input_data, period):
    stoch_list = []
    close = input_data['Close'].to_list()
    for i in range(len(close)):
        if i < period - 1:
            stoch_list.append(np.NAN)
        else:
            last_close = close[i - 1]
            max_close = np.nanmax(input_data['High'].to_list()[i - period + 1: i + 1])
            min_close = np.nanmin(input_data['Low'].to_list()[i - period + 1: i + 1])
            stoch_list.append(round((last_close - min_close)/(max_close - min_close), 2))
    input_data['Stochastic Fast (%s)' % period] = stoch_list
    return input_data['Stochastic Fast (%s)' % period]


# Slow Stochastic %D
def stoch_d(input_data, period, length):
    stoch_k_list = []
    stoch_d_list = []
    close = input_data['Close'].to_list()
    for i in range(len(close)):
        if i < period - 1:
            stoch_k_list.append(np.NAN)
        else:
            last_close = close[i - 1]
            max_close = np.nanmax(input_data['High'].to_list()[i - period + 1: i + 1])
            min_close = np.nanmin(input_data['Low'].to_list()[i - period + 1: i + 1])
            stoch_k_list.append(round((last_close - min_close)/(max_close - min_close), 2))
    for j in range(len(stoch_k_list)):
        if j < length - 1:
            stoch_d_list.append(np.NAN)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                stoch_d_list.append(round(np.nanmean(stoch_k_list[j - length + 1: j+1]), 2))
    input_data['Stochastic Slow (%s,%s)' % (period, length)] = stoch_d_list
    return input_data['Stochastic Slow (%s,%s)' % (period, length)]


# MACD
def macd(input_data, fast, slow, fast_smoothing, slow_smoothing):
    ema_fast = ema(input_data, fast, fast_smoothing).to_list()
    ema_slow = ema(input_data, slow, slow_smoothing).to_list()
    macd_list = []
    for i in range(len(ema_fast)):
        macd_list.append(ema_fast[i] - ema_slow[i])
    input_data['MACD (%s,%s)' % (fast, slow)] = macd_list
    return input_data['MACD (%s,%s)' % (fast, slow)]


# Signal
def signal(input_data, fast, slow, fast_smoothing, slow_smoothing, period, smoothing):
    signal_list = []
    macd_value = macd(input_data, fast, slow, fast_smoothing, slow_smoothing).to_list()
    for i in range(len(macd_value)):
        if i < slow + period - 2:
            signal_list.append(np.NAN)
        elif i == slow + period - 2:
            signal_list.append(round(np.nanmean(macd_value[i - period + 1: i + 1]), 2))
        else:
            signal_list.append(round((macd_value[i] * (smoothing / (1 + period)))
                                     + signal_list[-1] * (1 - (smoothing / (1 + period))), 2))
    input_data['Signal %s' % period] = signal_list
    return input_data['Signal %s' % period]

# Previous day high
def prev_high(input_data):
    return round(input_data['High'].iloc[-1], 2)


# Previous day low
def prev_low(input_data):
    return round(input_data['Low'].iloc[-1], 2)


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
