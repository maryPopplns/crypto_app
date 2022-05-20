import time
import hmac
import flask
from flask import jsonify
from requests import Request, Session
from headline_request import headline_request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/headlines', methods=['GET'])
def headline():
    response = headline_request()
    return jsonify(response)
