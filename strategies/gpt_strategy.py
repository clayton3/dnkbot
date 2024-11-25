from ai.gpt_signals import gpt_generate_signal
from utils.helpers import prepare_gpt_context

def gpt_strategy(context):
    signal = gpt_generate_signal(context)
    if signal == "error":
        return 0  # Neutral signal
    elif signal == "buy":
        return 1
    elif signal == "sell":
        return -1
    else:
        return 0  # Default to neutral for unrecognized signals