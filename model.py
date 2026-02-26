import tensorflow as tf

def build_lstm_model(input_shape=(90, 2), output_shape=5):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dense(32),
        tf.keras.layers.Dense(output_shape)  # Camada de saída para o horizonte de previsão
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model