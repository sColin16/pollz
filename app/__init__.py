"""Module file for the pollz app. Instantiates the app based on
the enviornment variable APP_MODE, which is automaticaly set to dev
if not specified. Sets up the database as well."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options

APP_MODE = os.environ.get('APP_MODE', 'dev')
print(APP_MODE)

app = Flask(__name__)  # pylint:disable=invalid-name
app.config.from_object(config_options.get(APP_MODE))

db = SQLAlchemy(app)  # pylint:disable=invalid-name
db.create_all()
