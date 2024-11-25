import websocket
import json
import ssl
import datetime
import threading

# Global exit flag
exit_event = threading.Event()


def stream_live_data(symbols, callback):
    """Stream live data for selected symbols."""
    BASE_URL = "wss://stream.binance.us:9443/ws"
    # Combine symbols and their streams
    streams = "/".join([f"{symbol.lower()}@ticker" for symbol in symbols])
    socket = f"{BASE_URL}/{streams}"

    print(f"Connecting to WebSocket URL: {socket}")  # Debug URL


    def on_message(ws, message):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            print(f"[{datetime.datetime.now()}] Message received: {data}")
            callback(data)
        except json.JSONDecodeError as e:
            print(f"Failed to parse message: {message}, Error: {e}")

    def on_error(ws, error):
        """Handle WebSocket errors."""
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        """Handle WebSocket closure."""
        print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")
        if not exit_event.is_set():
            print("Reconnecting in 5 seconds...")
            threading.Timer(5, stream_live_data, args=(symbols, callback)).start()

    def on_open(ws):
        """Log WebSocket connection."""
        print(f"WebSocket connected for symbols: {symbols}")

    ws = websocket.WebSocketApp(
        socket,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    # Run the WebSocket in the current thread
    try:
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    except KeyboardInterrupt:
        print("Exiting WebSocket...")
        exit_event.set()
        ws.close()


def exit_stream():
    """Signal the WebSocket to exit."""
    print("Stopping WebSocket...")
    exit_event.set()


# Example callback function
def handle_ticker(data):
    """Process and display live ticker updates."""
    if "s" in data and "c" in data:  # Check if symbol and price are in the message
        symbol = data["s"]
        price = data["c"]
        print(f"[{datetime.datetime.now()}] {symbol} price: ${price}")


# Example usage
if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT"]
    print(f"Streaming live prices for: {symbols}")
    stream_thread = threading.Thread(target=stream_live_data, args=(symbols, handle_ticker), daemon=True)
    stream_thread.start()

    # Stop after 60 seconds for testing
    threading.Timer(60, exit_stream).start()