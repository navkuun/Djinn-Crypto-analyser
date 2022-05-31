import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

from routes import crypto_processes
app = Flask(__name__)
app.register_blueprint(crypto_processes)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

jwt = JWTManager(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JWT_SECRET_KEY'] = 'djinn_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

client = MongoClient("mongodb://localhost:27017/")  # connection string
db = client["djinn_db"]
# DB collections
users_collection = db["users"]
print("User collection created", flush=True)
# DB collections


@ app.route("/api/register", methods=["POST", "OPTIONS"])
@cross_origin()
def register():
    # creates a new user
    new_user = request.get_json()  # store the json body request
    new_user["password"] = hashlib.sha256(
        new_user["password"].encode("utf-8")).hexdigest()  # encrpt password
    doc = users_collection.find_one(
        {"username": new_user["username"]})  # check if user exist
    if not doc:
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created successfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409


@ app.route("/api/login", methods=["POST", "OPTIONS"])
@cross_origin()
def login():
    # returns a jwt key for the user logging in to use and does some verification
    print(request.get_json(), flush=True)
    login_details = request.get_json()  # store the json body request
    user_from_db = users_collection.find_one(
        {'username': login_details['username']})  # search for user in database

    if user_from_db:
        encrpted_password = hashlib.sha256(
            login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(
                identity=user_from_db['username'])  # create jwt token
            return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'The username or password is incorrect'}), 401


@ app.route("/api/user", methods=["GET"])
@ jwt_required
def profile():
    current_user = get_jwt_identity()  # Get the identity of the current user
    user_from_db = users_collection.find_one({'username': current_user})
    if user_from_db:
        # delete data we don't want to return
        del user_from_db['_id'], user_from_db['password']
        return jsonify({'profile': user_from_db}), 200
    else:
        return jsonify({'msg': 'Profile not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
