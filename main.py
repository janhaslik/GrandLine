from flask import Flask, request
import model

app = Flask(__name__)


@app.route('/models/deploy', methods=['POST'])
def deploy():
    model_name = request.json['model']
    data = request.json['data']


@app.route('/models/forecast', methods=['POST'])
def predict():
    timeline = request.json['timeline']
    model = request.json['model']

    model.predict(timeline)
