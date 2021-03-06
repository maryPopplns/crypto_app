import os
import jwt
import uuid
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response
from controllers import headlines_controller, coins_controller
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

# database config
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# user model
class User(db.Model):
    __table_name = 'users'
    id = db.Column(db.String(), primary_key=True, default=uuid.uuid1)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    coins = db.Column(db.PickleType, nullable=True, default=[])


# jwt generator
def encode_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'),
                       algorithm='HS256')
    return token


# auth middleware
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
            current_user = User.query.filter_by(
                id=data['sub']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


def get_jwt():
    token = request.headers["Authorization"].split(" ")[1]
    data = jwt.decode(
        token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    return data["sub"]


@app.route('/addcoin', methods=['PUT'])
@token_required
# TODO figure out a way to get the user from the token
def add_coin(f):
    user_id = get_jwt()
    coin_id = request.form['id']
    coin_price = request.form['price']

    user = User.query.filter_by(id=user_id).first()

    coins = list(user.coins)

    # create list of coin ids
    def coins_id_extractor(coin):
        return coin["id"]
    coin_ids = list(map(coins_id_extractor, coins))

    if coin_id in coin_ids:
        return jsonify(message='coins has already been added')

    coins.append({"id": coin_id, "price": coin_price})
    user.coins = coins
    db.session.commit()

    return jsonify(message=coins)


@app.route('/removecoin', methods=['PUT'])
@token_required
def remove_coin(f):
    user_id = get_jwt()
    coin_id = request.form['id']

    user = User.query.filter_by(id=user_id).first()

    # remove coin from coins
    def compare_coins(coin):
        if coin["id"] == coin_id:
            return False

        return True
    allcoins = list(user.coins)
    coins = list(filter(compare_coins, allcoins))

    user.coins = coins
    db.session.commit()

    return jsonify(coins=coins)


@app.route('/usercoins', methods=['GET'])
@token_required
def usercoins(f):
    userid = get_jwt()

    user = User.query.filter_by(id=userid).first()

    return jsonify(message=user.coins)


@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        try:

            hashed_password = generate_password_hash(password)
            user = User(username=username, password=hashed_password)

            db.session.add(user)
            db.session.commit()
            resp = {
                "status": "success",
                "message": "User successfully registered",
            }
            return make_response(jsonify(resp)), 201

        except Exception as e:
            print(e)
            resp = {
                "status": "Error",
                "message": " Error occured, user registration failed"
            }
            return make_response(jsonify(resp)), 401
    else:
        resp = {
            "status": "error",
            "message": "User already exists"
        }
        return make_response(jsonify(resp)), 202


@app.route('/login', methods=['POST'])
def post():
    username = request.form['username']
    password = request.form['password']

    try:

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password) == True:
            auth_token = encode_token(user.id)
            resp = {
                "status": "success",
                "message": "Successfully logged in",
                'auth_token': auth_token
            }
            return make_response(jsonify(resp)), 200
        else:
            resp = {
                "status": "Error",
                "message": "User does not exist"
            }
            return make_response(jsonify(resp)), 404

    except Exception as e:
        print(e)
        resp = {
            "Status": "error",
            "Message": "User login failed"
        }
        return make_response(jsonify(resp)), 404


@app.route('/headlines', methods=['GET'])
def headlines():
    response = headlines_controller()
    return jsonify(response)


@app.route('/topcoins', methods=['GET'])
def topcoins():
    response = coins_controller('')
    return jsonify(response)


@app.route('/coin', methods=['POST'])
def coin():
    coin = request.form['coin']
    response = coins_controller(f'?list={coin}')
    return jsonify(response)
