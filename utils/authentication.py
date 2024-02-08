import jwt
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        print("askdjhjaoslkhd")

        load_dotenv()
        SECRET_KEY = os.environ.get('SECRET_KEY')

        token = None

        # Check if the token is in the authorization header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Assuming the token is sent as "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # data from the jwt
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated_function
