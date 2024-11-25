from ai.gpt_signals import gpt_generate_signal

def gpt_strategy(row):
    """
    Determines a trading signal based on GPT-generated insights.

    Parameters:
    - row (pd.Series): A row of a DataFrame containing the necessary context data.

    Returns:
    - int: A trading signal (1 for 'buy', -1 for 'sell', 0 for 'hold').
    """
    try:
        # Extract the context (ensure 'context' is a valid key in the DataFrame)
        context = row.get('context', None)
        if context is None:
            print("No context provided. Defaulting to 'hold'.")
            return 0  # Neutral signal if no context is available

        # Generate a signal using GPT
        signal = gpt_generate_signal(context)
        if signal is None:
            print("GPT did not return a valid signal. Defaulting to 'hold'.")
            return 0  # Neutral signal if GPT response is invalid

        # Map GPT response to a trading signal
        if 'buy' in signal:
            return 1
        elif 'sell' in signal:
            return -1
        else:
            return 0  # Default to 'hold' for unrecognized signals

    except Exception as e:
        print(f"Error in gpt_strategy: {e}")
        return 0  # Default to 'hold' on error