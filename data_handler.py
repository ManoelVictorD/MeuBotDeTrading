import ccxt
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def fetch_historical_data(symbol, timeframe, lookback, ema_period, volatility_lookback):
    limit = lookback + ema_period + 50
    try:
        exchange = ccxt.binance({'enableRateLimit': True})
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Indicadores
        df['range'] = df['high'] - df['low']
        df['atr'] = df['range'].rolling(window=volatility_lookback, min_periods=1).mean()
        df['ema_20'] = df['close'].ewm(span=ema_period, adjust=False).mean()
        
        return df.dropna()
    except Exception as e:
        print(f"❌ Erro DataHandler: {e}")
        return None

def prepare_input_data(df, lookback):
    # IMPORTANTE: O modelo espera 2 colunas: [close, atr]
    features = df[['close', 'atr']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(features)
    
    X_input = scaled_data[-lookback:].reshape(1, lookback, 2)
    return X_input, scaler