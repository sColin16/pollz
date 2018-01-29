import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options

APP_MODE = os.environ.get('APP_MODE', 'dev')
print(APP_MODE)

app = Flask(__name__)
app.config.from_object(config_options.get(APP_MODE))

db = SQLAlchemy(app)
db.create_all()
