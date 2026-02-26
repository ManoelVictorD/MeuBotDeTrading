def get_signal(pred_price, current_price, ema_recent):
    if pred_price > current_price and current_price > ema_recent:
        return 'BUY'
    elif pred_price < current_price and current_price < ema_recent:
        return 'SELL'
    return 'HOLD'

def calculate_quantity(capital_usd, risk_pct, current_price):
    # Arriscar X% do capital disponível
    risk_amount = capital_usd * risk_pct
    return round(risk_amount / current_price, 6) # Ajuste de precisão