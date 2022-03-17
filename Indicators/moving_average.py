import numpy as np


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
