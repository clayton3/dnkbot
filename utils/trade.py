from binance.spot import Spot
from config.settings import API_KEY, API_SECRET

def execute_trade(signal, symbol, quantity):
    """
    Execute a trade on Binance based on GPT's signal.

    Args:
        signal (str): GPT signal ("buy", "sell").
        symbol (str): Trading pair (e.g., "BTCUSDT").
        quantity (float): Quantity to trade.

    Returns:
        dict: Trade execution details.
    """
    spot = Spot(api_key=API_KEY, api_secret=API_SECRET)
    if signal == "buy":
        return spot.new_order(symbol=symbol, side="BUY", type="MARKET", quantity=quantity)
    elif signal == "sell":
        return spot.new_order(symbol=symbol, side="SELL", type="MARKET", quantity=quantity)
    else:
        print(f"Invalid signal: {signal}")
        return None


def paper_trade(signal, current_price, position):
    """
    Simulate a trade without executing live orders.

    Args:
        signal (int): Trading signal (-1 = sell, 1 = buy, 0 = hold).
        current_price (float): Current market price.
        position (float): Current position size.

    Returns:
        float: Updated position size.
    """
    if signal == 1:  # Buy
        position += 1  # Simulate buying 1 unit
    elif signal == -1:  # Sell
        position = max(0, position - 1)  # Simulate selling 1 unit
    return position