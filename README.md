Advanced Crypto Predictor: LSTM-Based Trading Bot
📌 Visão Geral
Este projeto é uma solução de Trading Algorítmico de alta performance para o par BTC/USDT na exchange Binance. O diferencial competitivo reside na integração de Redes Neurais Recorrentes (LSTM) para a previsão de preços, combinada com uma camada rigorosa de Gerenciamento de Risco e análise técnica clássica.

O sistema foi desenhado de forma modular, permitindo a escalabilidade para novos pares e o refinamento contínuo dos modelos preditivos.

🛠️ Stack Tecnológica
Linguagem: Python 3.x.

Inteligência Artificial: TensorFlow & Keras (Arquitetura LSTM).

Processamento de Dados: Pandas, NumPy, Scikit-learn (MinMaxScaler).

Exchange Integration: CCXT & Binance Python Client.

Indicadores Técnicos: EMA (Média Móvel Exponencial) e ATR (Average True Range).

🧠 Arquitetura do Modelo (Deep Learning)
O "cérebro" do bot utiliza uma rede LSTM (Long Short-Term Memory) projetada para capturar dependências temporais em séries financeiras complexas:

Input Shape: Janela deslizante de 90 períodos (FEATURE_LOOKBACK).

Features: Preço de fechamento, Volatilidade (ATR) e EMA 20.

Camadas: Duas camadas LSTM de 64 neurônios seguidas de camadas densas para regressão.

Objetivo: Previsão do próximo passo (PREDICTION_HORIZON = 1) para decisões de curtíssimo prazo.

🛡️ Estratégia e Gestão de Risco
A execução não depende apenas da IA, mas de um conjunto de regras de governança financeira:

Filtro de Tendência: Compras só são autorizadas se o preço atual estiver acima da EMA 20.

Stop Loss Dinâmico: Fixado em 1.5% para proteção de capital.

Take Profit: Alvo de saída em 3.0%.

Dimensionamento de Posição: Risco limitado a 1% do capital total por operação, calculado dinamicamente com base no preço de mercado.

🚀 Como Executar
Configuração de Ambiente:

Bash
pip install ccxt pandas numpy tensorflow scikit-learn python-binance
Credenciais: Insira suas chaves de API da Binance em bot_trading.py (Recomenda-se o uso de variáveis de ambiente por segurança).

Execução:

Bash
python bot_trading.py
⚠️ Disclaimer
Este software é para fins educacionais e de pesquisa. O mercado de criptoativos é volátil e envolve alto risco. O desenvolvedor não se responsabiliza por perdas financeiras decorrentes do uso deste bot.

Desenvolvido por Manoel Victor Duarte — Transformação Digital e IA Aplicada.
