import numpy as np
# import pandas as pd
import yfinance as yf
import mplfinance as mpf

# User Interaction program
ticker_input = input("Stock Ticker: ")
ticker_input = ticker_input.upper()

data = yf.download(tickers=ticker_input, period="3d", interval="5m")


# Moving Average
def ma(input_data, period):
    ma_list = []
    close = input_data['Close'].to_list()
    for i in range(len(close)):
        if i < period - 1:
            ma_list.append(np.NAN)
        else:
            ma_list.append(round(np.nanmean(close[i - period + 1: i + 1]), 2))
    input_data['MA %s' % (period)] = ma_list
    return input_data['MA %s' % (period)]


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
    input_data['EMA %s' %(period)] = ema_list
    return input_data['EMA %s' %(period)]


apd = [mpf.make_addplot(ema(data, 9, 2)), mpf.make_addplot(ema(data, 21, 2))]
mpf.plot(data, type="candle", title=ticker_input + " Price", style="yahoo", addplot=apd)

