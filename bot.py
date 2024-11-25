from utils.helpers import (
    fetch_historical_data,
    fetch_live_price,
    prepare_gpt_context,
    log_gpt_signal
)
from utils.stream import stream_live_data
from strategies.rule_based import sma_crossover_strategy
from strategies.gpt_strategy import gpt_strategy
from utils.backtest import backtest_strategy
from utils.indicators import calculate_sma, calculate_rsi, calculate_latest_indicators


def print_live_prices(symbols):
    """
    Print the live prices of all selected coins.

    Parameters:
    - symbols (list): List of trading symbols to fetch prices for.
    """
    for symbol in symbols:
        try:
            price = fetch_live_price(symbol)
            print(f"The current price of {symbol} is: ${price:.2f}")
        except Exception as e:
            print(f"Error fetching live price for {symbol}: {e}")


def handle_ticker_update(message):
    """
    Callback function to handle live ticker updates.

    Parameters:
    - message (dict): WebSocket message containing price and symbol data.
    """
    if 'p' in message:  # 'p' typically contains the price in Binance ticker data
        symbol = message.get('s', 'Unknown')
        price = float(message['p'])

        # Calculate live indicators dynamically
        indicators = calculate_latest_indicators(data, price, 5, 14)

        # Prepare market context for GPT
        context = prepare_gpt_context(symbol, {"price": price}, indicators)

        # Generate GPT signal
        gpt_signal = gpt_strategy(symbol, context)
        print(f"Live GPT Signal - {symbol}: {gpt_signal}")
        
        # Log the GPT signal
        log_gpt_signal(symbol, gpt_signal, context)


if __name__ == "__main__":
    # Define the coins to stream
    symbols = ["BTCUSDT", "ETHUSDT"]
    short_window = 5
    long_window = 20

    print("Fetching historical data...")
    try:
        data = fetch_historical_data("BTCUSDT", "1h", "2023-01-01", "2023-01-10")
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        exit()

    # Apply SMA Crossover Strategy
    print("Applying SMA Crossover Strategy...")
    try:
        strategy_data = sma_crossover_strategy(data, short_window, long_window)
        print(strategy_data[['timestamp', 'close', 'signal']].tail())
    except Exception as e:
        print(f"Error applying SMA strategy: {e}")
        exit()

    # Backtest the SMA strategy
    print("Backtesting SMA strategy...")
    try:
        results = backtest_strategy(strategy_data)
        print("Backtest Results:")
        print(f"Total Return: {results['total_return']:.2%}")
        print(f"Win Rate: {results['win_rate']:.2%}")
    except Exception as e:
        print(f"Error during backtesting: {e}")
        exit()

    # Backtest GPT signals on historical data
    print("\nBacktesting GPT signals...")
    try:
        data['gpt_signal'] = data.apply(
            lambda row: gpt_strategy(row.to_dict()), axis=1
        )
        print("Signals generated successfully:")
        print(data[['timestamp', 'close', 'gpt_signal']].tail())
    except Exception as e:
        print(f"Error applying GPT strategy to DataFrame: {e}")
        exit()

    try:
        gpt_backtest_results = backtest_strategy(data)
        print("GPT Backtest Results:")
        print(f"Total Return: {gpt_backtest_results['total_return']:.2%}")
        print(f"Win Rate: {gpt_backtest_results['win_rate']:.2%}")
    except Exception as e:
        print(f"Error during GPT backtesting: {e}")
        exit()

    # Stream live prices
    print("Streaming live prices from Binance.US...")
    print("Fetching initial prices...")
    try:
        print_live_prices(symbols)
    except Exception as e:
        print(f"Error fetching live prices: {e}")

    print("\nStarting WebSocket stream for live updates...")
    try:
        stream_live_data(symbols, handle_ticker_update)
    except Exception as e:
        print(f"Error in WebSocket stream: {e}")