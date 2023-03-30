from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, create_refresh_token
from flask_bcrypt import Bcrypt
import datetime
import jwt


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60  # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 3600  # seconds
jwt = JWTManager(app)
CORS(app)

@app.route('/')
def ree():
    return "ree"
    

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        print(request.headers)
        return jsonify({'status': 'success', 'access_token': access_token, 'refresh_token': refresh_token})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password!'})

@app.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)
    return jsonify({'status': 'success', 'access_token': access_token})

if __name__ == '__main__':
    app.run(debug=True)