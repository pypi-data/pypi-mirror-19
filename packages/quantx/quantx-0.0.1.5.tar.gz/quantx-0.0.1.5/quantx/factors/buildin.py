from quantx.btest import api


@api.custom_f
def SMA(f, window_len):
    return f.rolling(window_len).mean()
