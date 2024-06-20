# Grand Line: Time-Series Models Platform

Welcome to Grand Line, a platform designed for time-series modeling using LSTM and ARIMA models. This project combines the power of machine learning with a user-friendly interface to facilitate automatic model creation and deployment.

## Features

- **LSTM and ARIMA Models**: Implemented using Keras and TensorFlow for accurate time-series forecasting.
  
- **Automatic Model Creation and Deployment**: Backend developed with Python Flask to automate the process of training models and deploying them seamlessly.

- **Responsive Frontend**: Built with React TSX to provide an intuitive user interface. Users can upload datasets, initiate model training, and view forecasts effortlessly.

- **Database Management**: MySQL is utilized for efficient data storage and management.

## Components

### Backend (Python Flask)

The backend handles the core functionalities of the platform:
- **Model Training**: Automatically trains LSTM and ARIMA models based on user-uploaded datasets.
- **Deployment**: Provides endpoints for deploying trained models to generate forecasts.
- **API Integration**: Supports integration with the frontend for seamless data flow and model execution.

### Frontend (React TSX)

The frontend offers a responsive interface accessible via web browsers:
- **Dataset Upload**: Allows users to upload time-series datasets in various formats.
- **Model Training**: Initiates training of LSTM and ARIMA models with just a few clicks.
- **Forecast Visualization**: Displays forecasted results in an easy-to-understand format.
- **User Management**: User authentication and session management functionalities.

### Database (MySQL)

MySQL is used for:
- **Data Storage**: Storing uploaded datasets securely.
- **Model Persistence**: Saving trained model parameters and metadata.
- **Configuration Management**: Handling user preferences and system configurations.

## Contributors

- [Jan Haslik](https://github.com/janhaslik)

Feel free to contribute to this project by submitting pull requests or reporting issues.
