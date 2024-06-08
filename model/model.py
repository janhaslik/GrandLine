import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from keras._tf_keras.keras.callbacks import EarlyStopping, ModelCheckpoint

class LSTM_Model():
    def __init__(self, name, data, sequence_length=50):
        self.name = name
        self.data = data
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scaled_data = self.scaler.fit_transform(data[['close']])
        self.X, self.y = self.create_sequences(self.scaled_data, self.sequence_length)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, shuffle=False)
        self.model = self.build_model()
        self.history = None

    def create_sequences(self, data, sequence_length):
        X, y = [], []
        for i in range(len(data) - sequence_length):
            X.append(data[i:i+sequence_length])
            y.append(data[i+sequence_length])
        return np.array(X), np.array(y)

    def build_model(self):
        model = Sequential([
            LSTM(units=100, return_sequences=True),
            Dropout(0.1),
            LSTM(units=100, return_sequences=False),
            Dropout(0.1),
            Dense(25, activation='relu'),
            Dense(units=1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train_model(self, epochs=2, batch_size=64):
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        checkpoint = ModelCheckpoint(f'data/models/{self.name}.keras', monitor='val_loss', save_best_only=True, verbose=1)

        self.history = self.model.fit(self.X_train, self.y_train,
                                      validation_split=0.1,
                                      epochs=epochs,
                                      batch_size=batch_size,
                                      callbacks=[early_stopping, checkpoint],
                                      verbose=1)
        self.model.evaluate(self.X_test, self.y_test)
        self.model.save(f'data/models/{self.name}.h5')

class ARIMA_Model():
    def __init__(self, name, data):
        self.name = name
        self.data = data
