import numpy as np
import warnings


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