# for some reason this is not importing, so i'm getting error
from os import access
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pymongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_pymongo import PyMongo
import sys

# Initializing flask app
app = Flask(__name__)
# configs
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["JWT_SECRET_KEY"] = "djinn-secret-key"
app.config["MONGO_URI"] = "mongodb://localhost:27017/djinn_db"

mongo = PyMongo(app)
db = mongo.db


# CORS(app, support_crednetials=True,   resources={
#      r"/login/*": {"origins": "http://localhost:8082"}})
CORS(app)

jwt = JWTManager(app)
try:
    user = db["User"]
    print("created user collection", flush=True)
except:
    print("Couldn't create user collection", flush=True)


@app.route('/test')
def hello_world():
    return "Naveed khan"


@app.route("/register", methods=["POST", "OPTIONS"])
def register():
    print(request.json, flush=True)
    email = request.json["email"]
    username = request.json["username"]
    verifyEmail = user.find_one({"email": email})
    verifyUsername = user.find_one({"username": username})

    if verifyEmail:
        return jsonify(message="Email already exists!"), 409
    elif verifyUsername:
        return jsonify(message="Username already exists!"), 409
    else:
        password = request.json["password"]
        user_info = dict(email=email, password=password, username=username)
        user.insert_one(user_info)
        return jsonify(message="user added successfully"), 201


@app.route("/login", methods=["POST", "OPTIONS"])
def login():
    print(request, flush=True)
    email = request.json["email"]
    password = request.json["password"]

    check_user = user.find_one({"email": email, "password": password})
    if check_user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", access_token=access_token), 201
    else:
        return jsonify(message="Incorrect email or password!"), 401


app.route("/dashboard")


@jwt_required
def dashboard():
    return jsonify(message="Welcome to djinn!")


if __name__ == '__main__':
    # same as electron server
    app.run(host='localhost', debug=True)
