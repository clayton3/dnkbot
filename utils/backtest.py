def backtest_strategy(data):
    """
    Backtest a strategy using generated signals.

    Args:
        data (pd.DataFrame): Data with 'signal' column.

    Returns:
        dict: Backtest results (e.g., total returns, win rate).
    """
    data['returns'] = data['close'].pct_change()
    data['strategy_returns'] = data['returns'] * data['signal'].shift(1)
    total_return = (1 + data['strategy_returns']).prod() - 1
    win_rate = (data['strategy_returns'] > 0).mean()
    return {
        "total_return": total_return,
        "win_rate": win_rate
    }

def backtest_gpt_signals(data, gpt_strategy):
    """
    Backtest GPT signals on historical data.

    Args:
        data (pd.DataFrame): Historical OHLCV data.
        gpt_strategy (function): GPT strategy function.

    Returns:
        dict: Backtest performance metrics.
    """
    data['gpt_signal'] = data.apply(
        lambda row: gpt_strategy(row['symbol'], row['live_data'], row['indicators']), axis=1
    )
    return backtest_strategy(data)