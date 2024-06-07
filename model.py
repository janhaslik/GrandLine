import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Load data
data = pd.read_csv('spx.csv', parse_dates=['date'], index_col='date')

# Preprocess Data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[['close']])

# Sequence Length
SEQUENCE_LENGTH = 50

# Create Sequences
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length])
        y.append(data[i+sequence_length])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data, SEQUENCE_LENGTH)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Model Definition
model = Sequential([
    LSTM(units=100, return_sequences=True, input_shape=(SEQUENCE_LENGTH, 1)),
    Dropout(0.2),
    LSTM(units=100, return_sequences=True),
    Dropout(0.2),
    LSTM(units=100),
    Dropout(0.2),
    Dense(units=1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = ModelCheckpoint('best_model.keras', monitor='val_loss', save_best_only=True, verbose=1)

# Model Training
history = model.fit(X_train, y_train,
                    validation_split=0.1,
                    epochs=100,
                    batch_size=64,
                    callbacks=[early_stopping, checkpoint],
                    verbose=1)

# Evaluate model
model.evaluate(X_test, y_test)

# Plot loss history
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Prediction Function
def predict(forecast_time):
    best_model = load_model('best_model.keras')

    last_sequence = scaled_data[-SEQUENCE_LENGTH:].reshape(1, SEQUENCE_LENGTH, 1)
    future_predictions = []

    for i in range(forecast_time):
        prediction = best_model.predict(last_sequence)
        future_predictions.append(prediction[0, 0])

        # Update last Sequence
        last_sequence = np.roll(last_sequence, -1, axis=1)
        last_sequence[0, -1, 0] = prediction

    # Inverse scaling
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()

    # Derive future dates
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=forecast_time+1)[1:]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(future_dates, future_predictions, label='Predicted', linestyle='--')
    plt.plot(data.index[-100:], data['close'][-100:], label='Actual')
    plt.title('S&P 500 Prediction')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Call the predict function
predict(500)

