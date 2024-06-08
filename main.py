import pandas as pd
from flask import Flask, request, jsonify
from data import db

from model import model, predict

app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    res = db.insert_user(username, email, password)

    if res["status"] == "success":
        return jsonify({'status': 'success', 'message': 'User registered successfully!'}), 200
    else:
        return jsonify({'status': res["status"], 'message': res["message"]}), 403


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    res = db.login_user(username, password)
    if res["status"] == "success":
        return jsonify({'status': res['status'], 'message': 'User logged in!', 'userid': res['user_id']}), 200
    elif res["status"] == "fail" and res["message"] == "Wrong password":
        return jsonify({'status': res["status"], 'message': res["message"]}), 403
    else:
        return jsonify({"status": "fail", "message": "User does not exist"}), 404


@app.route('/models', methods=['POST'])
def create_model():
    model_name = request.json['model_name']
    model_type = request.json['model_type']
    data_path = request.json['data_path']
    userid = request.json['userid']

    model_types = {
        'LSTM': model.LSTM_Model,
        'ARIMA': model.ARIMA_Model,
    }

    if model_type in model_types:

        # Add to db
        res = db.insert_model(model_name, model_type, data_path, userid)

        if res == 400:
            return jsonify({'status': 'fail', 'message': 'Model already exists'}), 400

        return jsonify({"status": "Model created successfully", "model": res}), 200
    else:
        return jsonify({"error": "Model type not supported"}), 404


@app.route('/models/deploy', methods=['POST'])
def deploy():
    model_types = {
        'LSTM': model.LSTM_Model,
        'ARIMA': model.ARIMA_Model,
    }

    model_id = request.json['model_id']
    model_type, data_path = db.get_model(model_id)
    data = pd.read_csv(data_path)
    model_class = model_types[model_type]
    model_instance = model_class(model_id, data)
    model_instance.train_model()

    return jsonify({"status": "Model deployed successfully"}), 200
    # return jsonify({"error": "Model instance failed"}), 500


@app.route('/models/forecast', methods=['POST'])
def forecast():
    timeline = request.json['timeline']
    model_id = request.json['model_id']

    model_type, data_path = db.get_model(model_id)

    if model_type and data_path:
        data = pd.read_csv(data_path)

        if model_type == 'LSTM':
            predictions = predict.predict_lstm(model_id, data, int(timeline))
            return jsonify({"predictions": predictions})

        return jsonify({"error": "Invalid Model Type"})
    else:
        return jsonify({"error": "Model not found"}), 400


if __name__ == '__main__':
    app.run(debug=True)
