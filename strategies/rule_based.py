from utils.indicators import calculate_sma

def sma_crossover_strategy(data, short_window, long_window):
    """
    Generate buy/sell signals based on SMA crossover.

    Args:
        data (pd.DataFrame): Historical OHLCV data.
        short_window (int): Short SMA window.
        long_window (int): Long SMA window.

    Returns:
        pd.DataFrame: Data with 'signal' column (1 = buy, -1 = sell, 0 = hold).
    """
    data['short_sma'] = calculate_sma(data, short_window)
    data['long_sma'] = calculate_sma(data, long_window)
    data['signal'] = 0
    data.loc[data['short_sma'] > data['long_sma'], 'signal'] = 1  # Buy
    data.loc[data['short_sma'] < data['long_sma'], 'signal'] = -1  # Sell
    return data
