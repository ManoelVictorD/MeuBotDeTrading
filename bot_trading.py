import time
import numpy as np
from tensorflow import keras
from data_handler import fetch_historical_data, prepare_input_data
from strategy import get_signal, calculate_quantity
from exchange_connector import get_binance_conn, get_usdt_brl_rate, execute_limit_order

# CONFIGURAÇÕES
SYMBOL = 'BTC/USDT'
TIMEFRAME = '15m'
FEATURE_LOOKBACK = 90
MODEL_FILE = 'lstm_model_advanced.h5'
TRADING_CAPITAL_BRL = 100
RISK_PER_TRADE = 0.01 # 1%

def run():
    print("🚀 MÁQUINA DE TRADING INICIADA...")
    exchange = get_binance_conn()
    model = keras.models.load_model(MODEL_FILE)
    trade_active = False

    while True:
        try:
            # 1. Câmbio e Dados
            brl_rate = get_usdt_brl_rate(exchange)
            if brl_rate is None:
                print("⚠️ Falha ao obter taxa BRL. Tentando novamente...")
                time.sleep(10)
                continue
                
            capital_usd = TRADING_CAPITAL_BRL / brl_rate
            
            df = fetch_historical_data(SYMBOL, TIMEFRAME, FEATURE_LOOKBACK, 20, 20)
            if df is None or df.empty:
                print("⚠️ Falha ao obter dados históricos.")
                time.sleep(60)
                continue
                
            X_input, scaler = prepare_input_data(df, FEATURE_LOOKBACK)
            
            current_price = df['close'].iloc[-1]
            ema_recent = df['ema_20'].iloc[-1]

            # 2. Previsão Robusta (Ajustado para Horizonte 5 e Scaler de 2 Colunas)
            # O modelo retorna (1, 5)
            pred_scaled = model.predict(X_input, verbose=0)
            
            # Extraímos o primeiro valor da previsão (próximo candle)
            next_step_scaled = pred_scaled[0, 0]
            
            # Criamos o array dummy (1 linha, 2 colunas) para o Scaler
            dummy = np.zeros((1, 2))
            dummy[0, 0] = next_step_scaled # Inserimos a previsão na coluna do Preço
            
            # Invertemos a escala
            pred_prices_unscaled = scaler.inverse_transform(dummy)
            target_price = pred_prices_unscaled[0, 0]

            # 3. Execução
            signal = get_signal(target_price, current_price, ema_recent)
            print(f"--- STATUS ---")
            print(f"BTC Atual: ${current_price:.2f} | Previsto: ${target_price:.2f}")
            print(f"EMA 20: ${ema_recent:.2f} | Sinal: {signal}")
            print(f"--------------")

            if signal == 'BUY' and not trade_active:
                qty = calculate_quantity(capital_usd, RISK_PER_TRADE, current_price)
                if execute_limit_order(exchange, SYMBOL, 'buy', qty, current_price):
                    trade_active = True
                    print(f"✅ Ordem de Compra Executada: {qty} BTC")
            
            # Lógica de Venda/Stop pode ser integrada aqui

        except Exception as e:
            print(f"🚨 Erro no Loop: {e}")
        
        time.sleep(60) # Verifica a cada 1 minuto

if __name__ == "__main__":
    run()