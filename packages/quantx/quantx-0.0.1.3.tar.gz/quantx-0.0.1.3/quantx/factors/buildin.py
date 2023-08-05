import quantx.btest.api
from quantx.factors import factor
from quantx.btest import api


@api.custom_f
def SMA(f, window_len):
    return f.groupby(level=1, group_keys=False).rolling(window_len).mean()
