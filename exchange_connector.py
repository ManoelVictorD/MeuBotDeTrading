import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

def get_binance_conn():
    return ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_API_SECRET'),
        'enableRateLimit': True,
    })

def get_usdt_brl_rate(exchange):
    try:
        ticker = exchange.fetch_ticker('USDT/BRL')
        return float(ticker['last'])
    except Exception as e:
        print(f"Erro Câmbio: {e}")
        return None

def execute_limit_order(exchange, symbol, side, quantity, price):
    try:
        price_str = f"{price:.8f}"
        if side == 'buy':
            order = exchange.create_limit_buy_order(symbol, quantity, price)
        else:
            order = exchange.create_limit_sell_order(symbol, quantity, price)
        print(f"✅ ORDEM {side.upper()} ENVIADA: {order['id']} a {price_str}")
        return True
    except Exception as e:
        print(f"❌ ERRO NA ORDEM: {e}")
        return False