import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()  # Global DB instance

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception:
        pass

    db.init_app(app)
    CSRFProtect(app)

    from .routes import main
    app.register_blueprint(main)

    return app
