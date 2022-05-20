import os
import time
import hmac
import flask
from flask import jsonify
from dotenv import load_dotenv
from requests import Request, Session

load_dotenv()

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

def api_request():
  s = Session()
  ts = int(time.time() * 1000)
  request = Request('GET', 'https://ftx.com/api')
  prepared = request.prepare()
  signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
  signature = hmac.new(api_secret.encode(), signature_payload, 'sha256').hexdigest()

  prepared.headers['FTX-KEY'] = api_key
  prepared.headers['FTX-SIGN'] = signature
  prepared.headers['FTX-TS'] = str(ts)

  resp = s.send(prepared)
  return resp.json()

print(api_request())

# @app.route('/', methods=['GET'])
# def home():
#     return jsonify(apikey=api_key)

# app.run()