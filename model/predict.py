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
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    plt.tight_layout()
    plt.show()


def predict_lstm(model_name, data, forecast_time):
    # Load the trained model
    model = load_model(f'data/models/{model_name}.h5')

    # Convert date column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # Calculate percentage returns
    data['returns'] = data['close'].pct_change()
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
    last_sequence = np.array(data[['close', 'returns']][-sequence_length:])

    # Ensure the sequence is in the correct shape
    last_sequence = last_sequence.reshape(1, sequence_length, 2)

    # Print out the last sequence for debugging
    print("Last Sequence:", last_sequence)

    # Predict the future timeline with rolling predictions
    future_predictions = []
    for i in range(forecast_time):
        prediction = model.predict(last_sequence)
        future_predictions.append(prediction[0, 0])
        print("Prediction:", prediction[0, 0])

        # Update the last sequence with the new prediction
        new_entry = np.array([last_sequence[0, -1, 0] * (1 + prediction[0, 0]), prediction[0, 0]])
        last_sequence = np.roll(last_sequence, -1, axis=1)
        last_sequence[0, -1] = new_entry

    # Print out the future predictions (scaled returns) for debugging
    print("Future Predictions (Scaled Returns):", future_predictions)

    # Inverse transform the scaled predictions to get actual returns
    future_returns = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()

    # Print out the future returns for debugging
    print("Future Returns:", future_returns)

    # Check if future returns contain NaN values
    if np.isnan(future_returns).any():
        print("NaN values found in future returns")

    # Derive future prices from predicted returns
    last_close = data['close'].iloc[-1]
    future_prices = [last_close]
    for return_val in future_returns:
        future_prices.append(future_prices[-1] * (1 + return_val))

    # Remove the first element (the last known close price)
    future_prices = future_prices[1:]

    # Check if future prices contain NaN values
    if np.isnan(future_prices).any():
        print("NaN values found in future prices")

    # Print out the future prices for debugging
    print("Future Prices:", future_prices)

    # Generate future dates for the predictions
    last_date = data['date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_time)

    # Print out the future dates for debugging
    print("Future Dates:", future_dates)

    # Separate historical data and future predictions
    historical_dates = data['date']
    historical_prices = data['close']

    # Plot combined data
    plot(historical_dates, historical_prices, future_dates, future_prices)

    # Prepare the historical and future data
    history = [{"date": date.strftime('%Y-%m-%d'), "price": float(price)} for price, date in
               zip(historical_prices, historical_dates)]
    future = [{"date": date.strftime('%Y-%m-%d'), "price": float(price)} for price, date in
              zip(future_prices, future_dates)]

    return history, future
