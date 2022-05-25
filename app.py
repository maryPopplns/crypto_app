import os
import jwt
import uuid
from functools import wraps
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy.dialects import postgresql
from flask import Flask, jsonify, request, make_response
from controllers import headlines_controller, coins_controller
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()

app = Flask(__name__)
app.config["DEBUG"] = True

# database config
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# user model
# TODO change user model
class User(db.Model):
    __table_name = 'users'
    id = db.Column(db.String(), primary_key=True, default=uuid.uuid1)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    coins = db.Column(db.PickleType, nullable=True)


def encode_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'),
                       algorithm='HS256')
    return token


@app.route('/update', methods=['PUT'])
def update_user():
    userid = request.form['user']
    user = User.query.filter_by(id=userid).first()
    user.coins = ['hola3']
    db.session.commit()
    return jsonify(message='updated')


@app.route('/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        try:

            hashed_password = generate_password_hash(password)
            user = User(email=email, password=hashed_password)

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
    email = request.form['email']
    password = request.form['password']

    try:

        user = User.query.filter_by(email=email).first()

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
