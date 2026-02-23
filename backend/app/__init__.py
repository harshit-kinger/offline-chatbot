from flask import Flask
from flask_cors import CORS
from .db import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()

    from .routes import chat_bp
    app.register_blueprint(chat_bp, url_prefix="/api")
    return app