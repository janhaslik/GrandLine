import pandas as pd
import numpy as np
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras._tf_keras.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import mean_squared_error
from math import sqrt


class LSTM_Model():
    def __init__(self, name, data, sequence_length=50, date_field='date', output_field='close'):
        self.name = name
        self.data = data
        self.sequence_length = sequence_length
        self.data.dropna(inplace=True)

        # Calculate percentage returns
        self.data['returns'] = self.data[output_field].pct_change()
        self.data.dropna(inplace=True)

        # Scale the 'close' prices along with the percentage returns
        self.scaler = StandardScaler()
        self.scaled_data = self.scaler.fit_transform(data[[output_field, 'returns']].values)

        self.X, self.y = self.create_sequences(self.scaled_data, self.sequence_length)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2,
                                                                                shuffle=False)
        self.model = self.build_model()
        self.history = None

    def build_model(self):
        model = Sequential([
            LSTM(units=100, return_sequences=True, input_shape=(self.sequence_length, 2)),  # Two features: close, returns
            Dropout(0.1),
            LSTM(units=100, return_sequences=False),
            Dropout(0.1),
            Dense(25, activation='relu'),
            Dense(units=1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def create_sequences(self, data, sequence_length):
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:i + sequence_length])
            y.append(data[i + sequence_length][1])  # Use the returns as the target
        return np.array(X), np.array(y)

    def train_model(self, epochs=30, batch_size=64):
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        checkpoint = ModelCheckpoint(f'data/models/{self.name}.keras', monitor='val_loss', save_best_only=True, verbose=1)

        self.history = self.model.fit(self.X_train, self.y_train,
                                      validation_split=0.1,
                                      epochs=epochs,
                                      batch_size=batch_size,
                                      callbacks=[early_stopping, checkpoint],
                                      verbose=1)
        self.model.evaluate(self.X_test, self.y_test)

        self.model.save(f'data/models/{self.name}.h5')

    def baseline_rmse(self):
        # Naive forecast: Predicting the next value as the current value
        naive_predictions = self.data['returns'].shift(1).dropna().values
        naive_rmse = sqrt(mean_squared_error(self.data['returns'].iloc[-len(naive_predictions):], naive_predictions))
        print(f'Baseline RMSE (Naive Forecast): {naive_rmse}')



class ARIMA_Model():
    def __init__(self, name, data):
        self.name = name
        self.data = data
