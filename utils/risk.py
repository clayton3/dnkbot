def calculate_position_size(balance, risk_percentage, entry_price):
    """Calculate position size based on risk."""
    risk_amount = balance * (risk_percentage / 100)
    return risk_amount / entry_price

def apply_stop_loss(data, stop_loss_percentage):
    """Apply stop-loss logic."""
    data['stop_loss'] = data['close'] * (1 - stop_loss_percentage / 100)
    return data
