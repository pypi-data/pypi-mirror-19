import numpy as np

from quantx.btest import api
from quantx.factors.bundle import Bundle
from quantx.factors.factor import Factor


@api.custom_f
def SMA(f, window_len):
    return f.rolling(window_len).mean()


class MarketBundle(Bundle):
    low = Factor()
    vol = Factor()
    inc = Factor()
    bns = Factor()
    abns = Factor()
    open = Factor()
    high = Factor()
    close = Factor()
    givsr = Factor()
    active = Factor(dtype=np.bool)
