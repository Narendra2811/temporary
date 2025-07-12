import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)

SECRET_KEY = 'stackit'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
