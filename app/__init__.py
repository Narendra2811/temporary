# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    db.init_app(app)
    CSRFProtect(app)

    from .routes import main
    app.register_blueprint(main)

    return app
