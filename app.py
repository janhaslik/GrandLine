import os

import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from data import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from model import model, predict

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
cors = CORS(app, resource={r"/api/*": {"origins": "*"}})

model_types = {
    'LSTM': model.LSTM_Model,
    'ARIMA': model.ARIMA_Model,
}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    print(username, email, password)

    res = db.insert_user(username, email, password)

    if res["status"] == "success":
        return jsonify({'status': 'success', 'message': 'User registered successfully!'}), 200
    else:
        return jsonify({'status': res["status"], 'message': res["message"]}), 403


@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    res = db.login_user(username, password)
    if res["status"] == "success":
        access_token = create_access_token(identity=res['user_id'])
        return jsonify(access_token=access_token), 200
    elif res:
        return jsonify({'status': 'fail', 'message': 'Wrong password'}), 403
    else:
        return jsonify({'status': 'fail', 'message': 'User does not exist'}), 404


@app.route('/api/models', methods=['POST'])
@jwt_required()
def create_model():
    try:
        model_name = request.json['model_name']
        model_type = request.json['model_type']
        data_path = request.json['data_path']

        userid = get_jwt_identity()

        if model_type in model_types:
            # Add to db
            res = db.insert_model(model_name, model_type, data_path, userid)
            if res["status"] == "success":
                return jsonify({"status": "Model created successfully", "model_id": res["model_id"]}), 200
            else:
                return jsonify({"status": "fail", "message": res["message"]}), 400
        else:
            return jsonify({"status": "fail", "message": "Model type not supported"}), 400
    except KeyError as e:
        return jsonify({"status": "fail", "message": f"Missing key in request JSON: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "fail", "message": f"An error occurred: {e}"}), 500


@app.route('/api/models', methods=['GET'])
@jwt_required()
def get_models():
    userid = get_jwt_identity()
    print(userid)
    models = db.get_models(userid)

    if models == 403:
        return jsonify({"status": "fail", "message": "You do not have permission to access this resource"}), 403
    elif models == 404:
        return jsonify({"status": "fail", "message": "No models found"}), 404

    return jsonify({"status": "success", "models": models}), 200


@app.route('/api/models', methods=['DELETE'])
@jwt_required()
def delete_model():
    model_id = request.args.get('model_id')
    userid = get_jwt_identity()

    try:
        os.remove(f'/data/models/{model_id}.h5')
        os.remove(f'/data/models/{model_id}.keras')
        res = db.delete_model(model, userid)

        if res["status"] == "success":
            return jsonify({"status": "success", "message": "Model deleted successfully"}), 200
        elif res["status"] == "fail" and res["message"] == "Model not found":
            return jsonify({"status": "fail", "message": res["message"]}), 404
    except Exception as e:
        return jsonify({"status": "fail", "message": f"An error occurred: {e}"}), 500


@app.route('/api/models/deploy', methods=['POST'])
@jwt_required()
def deploy():
    model_id = request.json['model_id']
    model_type, data_path = db.get_model(model_id)
    data_path = "spx.csv"
    data = pd.read_csv(data_path)
    model_class = model_types[model_type]
    model_instance = model_class(model_id, data)
    model_instance.train_model(epochs=2)

    # Set status in db to deployed
    db.deploy_model(model_id)

    return jsonify({"status": "Model deployed successfully"}), 200


@app.route('/api/models/forecast', methods=['POST'])
@jwt_required()
def forecast():
    timeline = request.json['timeline']
    model_id = request.json['model_id']

    model_type, data_path = db.get_model(model_id)
    data_path = "spx.csv"

    if model_type is not None and data_path is not None:
        data = pd.read_csv(data_path)
        print(model_id, model_type, data_path)

        if model_type == 'LSTM':
            predictions = predict.predict_lstm(model_id, data, int(timeline))
            return jsonify({"predictions": predictions})

        return jsonify({"error": "Invalid Model Type"})
    else:
        return jsonify({"error": "Model not found"}), 400


if __name__ == '__main__':
    app.run(debug=True)