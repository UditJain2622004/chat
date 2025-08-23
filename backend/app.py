from flask import Flask
from flask_cors import CORS
import firebase_setup
from mongo import db
from controllers.auth_controller import auth_bp
from routes.user_routes import users_bp
from routes.bot_routes import bots_bp
from routes.chat_routes import chats_bp

app = Flask(__name__)

# Enable CORS and allow requests only from http://localhost:5173
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(bots_bp, url_prefix='/bots')
app.register_blueprint(chats_bp, url_prefix='/chats')

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)
