import time
import hmac
import flask
from flask import jsonify, request
from controllers import headlines_controller, coins_controller

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/headlines', methods=['GET'])
def headlines():
    response = headlines_controller()
    return jsonify(response)

@app.route('/topcoins', methods=['GET'])
def topcoins():
    response = coins_controller('')
    return jsonify(response)

@app.route('/coin', methods=['GET'])
def coin():
    coin = request.form['coin']
    response = coins_controller(f'?list={coin}')
    return jsonify(response)
