import numpy as np
from exponential_moving_average import *


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