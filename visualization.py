import numpy as np
# import pandas as pd
import yfinance as yf
import mplfinance as mpf
import warnings

# User Interaction program
ticker_input = input("Stock Ticker: ")
ticker_input = ticker_input.upper()
#interval_input = input("Choose time interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo): ")
#period_input = input("Choose period interval (1d, 3d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max): ")

"""
Period = 1d, 3d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
Interval = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
"""

#data = yf.download(tickers=ticker_input, period=period_input, interval=interval_input)
data_3d5m = yf.download(tickers=ticker_input, period="3d", interval="5m")
data_3d15m = yf.download(tickers=ticker_input, period="3d", interval="15m")
data_3d30m = yf.download(tickers=ticker_input, period="3d", interval="30m")
data_5d5m = yf.download(tickers=ticker_input, period="5d", interval="5m")
data_5d15m = yf.download(tickers=ticker_input, period="5d", interval="15m")
data_5d30m = yf.download(tickers=ticker_input, period="5d", interval="30m")
data_1mo30m = yf.download(tickers=ticker_input, period="1mo", interval="30m")
data_3d1d = yf.download(tickers=ticker_input, period="3d", interval="1d")
data_3y1d = yf.download(tickers=ticker_input, period="3y", interval="1d")
data_3y1wk = yf.download(tickers=ticker_input, period="3y", interval="1wk")

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


def bollinger_upper(input_data, length, stdev):
    sma = ma(input_data, length)
    std = input_data['Close'].rolling(length).std()

    return sma + std*stdev


def bollinger_lower(input_data, length, stdev):
    sma = ma(input_data, length)
    std = input_data['Close'].rolling(length).std()

    return sma - std*stdev


# Previous day high
def prev_high(input_data):
    return round(input_data['High'].iloc[-1], 2)


# Previous day low
def prev_low(input_data):
    return round(input_data['Low'].iloc[-1], 2)


# Finding Support and Resistance
def sr_levels(input_data):
    sr_list = []
    hloc_list = []

    # Fill list of hloc
    for i in range(len(input_data)):
        hloc_list.append(input_data['High'][i])
        hloc_list.append(input_data['Low'][i])
        """ hloc_list.append(input_data['Open'][i])
        hloc_list.append(input_data['Close'][i])"""

    # Calculate the average of the hloc list
    rng = max(hloc_list)-min(hloc_list)

    # Go over all high and lows to find redundant levels
    for i in hloc_list:
        add = True
        count = 0
        for j in hloc_list:
            if abs(i - j) <= 0.0005 * rng:
                count += 10
            elif abs(i - j) <= 0.001 * rng:
                count += 0.5
            elif abs(i - j) <= 0.003 * rng:
                count += 0.3
            elif abs(i - j) <= 0.005 * rng:
                count += 0.1
            elif abs(i - j) <= 0.01 * rng:
                count += 0.05
        if count >= 10:
            for k in sr_list:
                if len(sr_list) == 0 or abs(k - i) > (rng * 0.05):
                    continue
                else:
                    add = False
                    break
            if add:
                sr_list.append(i)
    sr_list.sort()
    return sr_list

# Example code containing all indicators
apd = [mpf.make_addplot(ema(data_1mo30m, 9, 2)[-len(data_5d30m):], width=1), mpf.make_addplot(ema(data_1mo30m, 21, 2)[-len(data_5d30m):], width=1),
       mpf.make_addplot(stoch_k(data_1mo30m, 14)[-len(data_5d30m):], panel=1), mpf.make_addplot(stoch_d(data_1mo30m, 14, 3)[-len(data_5d30m):], panel=1),
       mpf.make_addplot(macd(data_1mo30m, 13, 26, 2, 2)[-len(data_5d30m):], panel=2), mpf.make_addplot(signal(data_1mo30m, 13, 26, 2, 2, 9, 2)[-len(data_5d30m):], panel=2, color='orange'),
       mpf.make_addplot(ma(data_1mo30m, 21)[-len(data_5d30m):], width=1), mpf.make_addplot(bollinger_upper(data_1mo30m, 21, 2)[-len(data_5d30m):], width=1),
       mpf.make_addplot(bollinger_lower(data_1mo30m, 21, 2)[-len(data_5d30m):], width=1)]

mpf.plot(data_5d30m, type="candle", title=ticker_input + " Price", style="yahoo", figsize=(20, 9.5),
         hlines=dict(hlines=sr_levels(data_5d30m), colors=['#ff8fab'], linestyle='dotted'))

# Plotting my trade setup
