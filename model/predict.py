import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


def plot(full_dates, actual_prices, predicted_prices, future_dates, future_predictions):
    plt.figure(figsize=(10, 6))
    plt.plot(full_dates.dt.strftime('%Y-%m-%d'), actual_prices, label='Actual')
    plt.plot(full_dates.dt.strftime('%Y-%m-%d'), predicted_prices, label='Predicted', linestyle='--')

    future_dates_dt = pd.to_datetime(future_dates).strftime('%Y-%m-%d')
    plt.plot(future_dates_dt, future_predictions, label='Future Predicted', linestyle='--')

    plt.title('S&P 500 Prediction')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()
    plt.show()


def predict_lstm(model_name, data, forecast_time):
    model = load_model(f'data/models/{model_name}.h5')
    data['date'] = pd.to_datetime(data['date'])
    sequence_length = model.input_shape[1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data[['close']])

    # Predict the historical timeline
    predictions = []
    for i in range(sequence_length, len(scaled_data)):
        sequence = scaled_data[i - sequence_length:i].reshape(1, sequence_length, 1)
        prediction = model.predict(sequence)
        predictions.append(prediction[0, 0])

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()

    # Predict the future timeline with rolling predictions
    last_sequence = scaled_data[-sequence_length:].copy()  # Use copy to avoid altering the original scaled data
    future_predictions = []

    last_date = data['date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_time).strftime('%Y-%m-%d')

    for i in range(forecast_time):
        sequence = last_sequence.reshape(1, sequence_length, 1)
        prediction = model.predict(sequence)
        future_predictions.append(prediction[0, 0])

        # Update the last sequence with the new prediction
        last_sequence = np.append(last_sequence[1:], prediction).reshape(-1, 1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()

    # Combine historical dates with predicted prices
    prediction_dates = data['date'][sequence_length:]
    actual_prices = data['close'][sequence_length:]

    # Plot combined data
    plot(prediction_dates, actual_prices, predictions, future_dates, future_predictions)

    historical_result = [{"date": date.strftime('%Y-%m-%d'), "price": float(price)} for price, date in
                         zip(predictions, prediction_dates)]
    future_result = [{"date": date, "price": float(price)} for price, date in zip(future_predictions, future_dates)]

    return historical_result + future_result