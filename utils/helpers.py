import pandas as pd
from binance.spot import Spot
import logging
import openai
from config.settings import API_KEY, API_SECRET, BASE_URL, OPENAI_API_KEY


def gpt_query(prompt, model="gpt-4"):
    """
    Query OpenAI GPT API with a prompt.

    Args:
        prompt (str): Input prompt for GPT.
        model (str): GPT model to use (e.g., "gpt-3.5-turbo" or "gpt-4").

    Returns:
        str: GPT's response.
    """
    openai.api_key = OPENAI_API_KEY
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "system", "content": "You are a financial trading assistant."},
                      {"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error querying GPT: {e}")
        return None

def prepare_gpt_context(symbol, live_data, indicators):
    """
    Prepare market context for GPT input.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        live_data (dict): Latest live price data.
        indicators (dict): Calculated technical indicators with single values.

    Returns:
        str: Formatted context for GPT prompt.
    """
    context = f"Symbol: {symbol}\n"
    context += f"Current Price: ${live_data['price']:.2f}\n"
    for name, value in indicators.items():
        context += f"{name}: {value:.2f}\n"  # Format as numeric
    return context


def log_gpt_signal(symbol, signal, context):
    """
    Log GPT's trading signal and the market context.

    Args:
        symbol (str): Trading pair symbol.
        signal (str): GPT-generated trading signal.
        context (str): Market context provided to GPT.
    """
    try:
        with open("gpt_signals.log", "a") as log_file:
            log_file.write(f"Symbol: {symbol}\n")
            log_file.write(f"Signal: {signal}\n")
            log_file.write("Context:\n")
            log_file.write(context + "\n\n")
    except Exception as e:
        print(f"Error logging GPT signal: {e}")


def prepare_gpt_context(symbol, live_data, indicators):
    """
    Prepare market context for GPT input.

    Args:
        symbol (str): Trading pair symbol (e.g., "BTCUSDT").
        live_data (dict): Latest live price data.
        indicators (dict): Calculated technical indicators.

    Returns:
        str: Formatted context for GPT prompt.
    """
    context = f"Symbol: {symbol}\n"
    context += f"Current Price: ${live_data['price']:.2f}\n"
    for name, value in indicators.items():
        context += f"{name}: {value:.2f}\n"
    return context

def setup_logging():
    """Set up logging for the bot."""
    logging.basicConfig(filename="trading_log.log", level=logging.INFO,
                        format="%(asctime)s - %(message)s")

def log_trade(symbol, action, price):
    """Log a trading decision."""
    logging.info(f"Trade executed: {action} {symbol} at ${price:.2f}")

def fetch_historical_data(symbol, interval, start_date, end_date=None):
    """
    Fetch historical candlestick (OHLCV) data from Binance Spot API.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Timeframe (e.g., '1m', '1h', '1d').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format (optional).

    Returns:
        pd.DataFrame: DataFrame containing historical OHLCV data.
    """
    try:
        spot = Spot(api_key=API_KEY, api_secret=API_SECRET, base_url=BASE_URL)

        # Convert date strings to timestamps (milliseconds since epoch)
        start_timestamp = int(pd.Timestamp(start_date).timestamp() * 1000)
        end_timestamp = int(pd.Timestamp(end_date).timestamp() * 1000) if end_date else None

        # Fetch candlestick data
        klines = spot.klines(
            symbol=symbol,
            interval=interval,
            startTime=start_timestamp,
            endTime=end_timestamp
        )

        # Convert to a Pandas DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])

        # Clean up data
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return pd.DataFrame()


def fetch_live_price(symbol):
    """
    Fetch the latest price for a specific trading pair.
    
    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').

    Returns:
        float: The current price of the trading pair.
    """
    try:
        spot = Spot(api_key=API_KEY, api_secret=API_SECRET, base_url=BASE_URL)

        # Fetch the latest price
        ticker = spot.ticker_price(symbol=symbol)
        return float(ticker['price'])
    
    except Exception as e:
        print(f"Error fetching live price for {symbol}: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    print("Fetching historical data...")
    historical_data = fetch_historical_data("BTCUSDT", "1h", "2023-01-01", "2023-01-10")
    print(historical_data.head())

    print("\nFetching live price...")
    live_price = fetch_live_price("BTCUSDT")
    print(f"BTCUSDT Live Price: ${live_price:.2f}" if live_price else "Failed to fetch live price.")
