import time
import hmac
import flask
from flask import jsonify
from requests import Request, Session
from controllers import headlines_controller, topcoins_controller

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/headlines', methods=['GET'])
def headlines():
    response = headlines_controller()
    return jsonify(response)

@app.route('/topcoins', methods=['GET'])
def topcoins():
    response = topcoins_controller()
    return jsonify(response)
