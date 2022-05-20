import flask
import time
import hmac
from requests import Request


app = flask.Flask(__name__)
app.config["DEBUG"] = True


ts = int(time.time() * 1000)
request = Request('GET', '<api_endpoint>')
prepared = request.prepare()
signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
signature = hmac.new('YOUR_API_SECRET'.encode(), signature_payload, 'sha256').hexdigest()

prepared.headers['FTX-KEY'] = 'YOUR_API_KEY'
prepared.headers['FTX-SIGN'] = signature
prepared.headers['FTX-TS'] = str(ts)

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

app.run()