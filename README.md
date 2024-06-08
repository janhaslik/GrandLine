# Grand Line: Time-series Model Orchestration

Grand Line is a project designed to facilitate the creation, deployment, and management of machine learning models.

## Dataset

The project utilizes the S&P 500 Daily dataset available on [Kaggle](https://www.kaggle.com/datasets/pdquant/sp500-daily-19862018). This dataset is for testing. A user can provide a own dataset. 

## Installation and Setup

To set up Grand Line, follow these steps:

1. Clone the repository to your local machine.
2. Install packages.
3. Configure the database connection details in `data/db.py`.
4. Have fun ;)

## Usage

### Registering Users

To register a new user, send a POST request to `/register` with the following JSON payload:

```json
{
    "username": "example_user",
    "email": "user@example.com",
    "password": "password123"
}
```

### Logging In

To log in, send a POST request to `/login` with the following JSON payload:

```json
{
    "username": "example_user",
    "password": "password123"
}
```

### Creating Models

To create a new machine learning model, send a POST request to `/models` with the following JSON payload:

```json
{
    "model_name": "example_model",
    "model_type": "LSTM",
    "data_path": "path/to/data",
    "userid": 1
}
```

### Deploying Models

To deploy a model for prediction, send a POST request to `/models/deploy` with the following JSON payload:

```json
{
    "model_id": 1
}
```

### Making Forecasts

To make forecasts using a deployed model, send a POST request to `/models/forecast` with the following JSON payload:

```json
{
    "timeline": 30,
    "model_id": 1
}
```

## Project Structure

The project consists of the following components:

- **app.py**: Flask application defining routes for user registration, login, model creation, deployment, and forecasting.
- **model.py**: Contains classes for defining machine learning models, including LSTM_Model and ARIMA_Model.
- **predict.py**: Implements functions for making predictions using deployed models.
- **data/db.py**: Handles database interactions, including user authentication, model creation, and retrieval.

## Running the Application

To run the Grand Line application, execute `app.py` in your terminal. The Flask server will start, and you can then access the endpoints using a tool like cURL or by integrating with the provided APIs.

## Contributors

- [Jan Haslik](https://github.com/janhaslik)

Feel free to contribute to this project by submitting pull requests or reporting issues. Happy modeling!
