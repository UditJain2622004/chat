from functools import wraps
from flask import request, jsonify, g
from firebase_setup import verify_token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # Expected format: "Bearer <token>"
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        user = verify_token(token)
        if not user:
            return jsonify({'message': 'Token is invalid or expired!'}), 401

        # Make user info available to the decorated route
        g.user = user
        
        return f(*args, **kwargs)

    return decorated_function
