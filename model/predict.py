import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras._tf_keras.keras.models import load_model
from sklearn.preprocessing import StandardScaler


def plot(historical_dates, historical_prices, future_dates, future_prices):
    plt.figure(figsize=(10, 6))
    plt.plot(historical_dates, historical_prices, label='Historical', linestyle='-')
    plt.plot(future_dates, future_prices, label='Future Predicted', linestyle='--')

    plt.title('S&P 500 Prediction')
    plt.xlabel("Date")
    plt.ylabel("Outcome")
    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()
    plt.show()


def predict_lstm(model_name, data, forecast_time, date_field='date', output_field='close'):
    # Load the trained model
    model = load_model(f'data/models/{model_name}.h5')

    # Convert date column to datetime
    data[date_field] = pd.to_datetime(data[date_field])

    # Calculate percentage returns
    data['returns'] = data[output_field].pct_change()

    # Drop missing values
    data = data.dropna()
    print("Returns: ", data.head())

    # Check if returns column contains NaN values after dropna
    if data['returns'].isna().any():
        print("NaN values found in 'returns' column after dropna")

    # Scale the returns using the same scaler used during training
    scaler = StandardScaler()
    scaler.fit(data[['returns']])  # Fit only on returns
    scaled_returns = scaler.transform(data[['returns']])

    # Check if scaled returns contain NaN values
    if np.isnan(scaled_returns).any():
        print("NaN values found in scaled returns")

    # Prepare the last sequence for prediction
    sequence_length = model.input_shape[1]
    last_sequence = np.array(data[[output_field, 'returns']][-sequence_length:])

    # Ensure the sequence is in the correct shape
    last_sequence = last_sequence.reshape(1, sequence_length, 2)

    # Predict the future timeline with rolling predictions
    future_predictions = []
    for i in range(forecast_time):
        prediction = model.predict(last_sequence)
        future_predictions.append(prediction[0, 0])

        # Update the last sequence with the new prediction
        new_entry = np.array([last_sequence[0, -1, 0] * (1 + prediction[0, 0]), prediction[0, 0]])
        last_sequence = np.roll(last_sequence, -1, axis=1)
        last_sequence[0, -1] = new_entry

    # Inverse transform the scaled predictions to get actual returns
    future_returns = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()

    # Check if future returns contain NaN values
    if np.isnan(future_returns).any():
        print("NaN values found in future returns")

    # Derive future prices from predicted returns
    last_output = data[output_field].iloc[-1]
    future_outputs = [last_output]
    for return_val in future_returns:
        future_outputs.append(future_outputs[-1] * (1 + return_val))

    # Remove the first element (the last known close price)
    future_outputs = future_outputs[1:]

    # Check if future prices contain NaN values
    if np.isnan(future_outputs).any():
        print("NaN values found in future prices")

    # Generate future dates for the predictions
    last_date = data[date_field].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_time)

    # Separate historical data and future predictions
    historical_dates = data[date_field]
    historical_outputs = data[output_field]

    # Plot combined data
    plot(historical_dates, historical_outputs, future_dates, future_outputs)

    # Prepare the historical and future data
    history = [{"date": date.strftime('%Y-%m-%d'), "price": round(float(price), 2)} for price, date in
               zip(historical_outputs, historical_dates)]
    future = [{"date": date.strftime('%Y-%m-%d'), "price": round(float(price), 2)} for price, date in
              zip(future_outputs, future_dates)]

    return history, future
