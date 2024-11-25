def moving_average_strategy(data, short_window=10, long_window=30):
    """
    Simple Moving Average (SMA) strategy:
    Buy when short SMA > long SMA, sell otherwise.
    """
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    data['signal'] = data['short_ma'] > data['long_ma']
    return data