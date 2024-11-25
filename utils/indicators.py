import pandas as pd

def calculate_sma(data, window):
    """Calculate Simple Moving Average."""
    return data['close'].rolling(window=window).mean()

def calculate_ema(data, window):
    """Calculate Exponential Moving Average."""
    return data['close'].ewm(span=window, adjust=False).mean()

def calculate_rsi(data, window):
    """Calculate Relative Strength Index."""
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_latest_indicators(data, price, sma_window, rsi_window):
    """
    Calculate the latest indicators (SMA, RSI) using historical and current data.

    Args:
        data (pd.DataFrame): Historical OHLCV data.
        price (float): Latest price to include.
        sma_window (int): Window for SMA calculation.
        rsi_window (int): Window for RSI calculation.

    Returns:
        dict: Latest SMA and RSI values.
    """
    # Append the latest price to the data
    updated_data = data.append({"close": price}, ignore_index=True)
    latest_sma = calculate_sma(updated_data, sma_window).iloc[-1]
    latest_rsi = calculate_rsi(updated_data, rsi_window).iloc[-1]
    return {"sma_5": latest_sma, "rsi_14": latest_rsi}
