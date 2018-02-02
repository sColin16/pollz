"""Environment configurations for the pollz app. Every time
an instance of the app is created, it will use the Environment
variable APP_MODE, or default to the DevConfig."""


import os
BASEDIR = os.path.abspath(os.path.dirname(__file__) + '/app')


class Config(object):  # pylint:disable=too-few-public-methods
    """Base configuration settings. Note SQLALCHEMY_TRACK_MODIFICATIONS
    it turned off for every configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):  # pylint:disable=too-few-public-methods
    """Dev configuration for general development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'dev.db')
    SECRET_KEY = 'development key'


class TestConfig(Config):  # pylint:disable=too-few-public-methods
    """Test configuration that is used during testing. A temporary
    Sqlite database is use for faster testing, and easier managment."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'development key'


class ProdConfig(Config):  # pylint:disable=too-few-public-methods
    """Production configuration onl loaded on the Heroku production server.
    Note that the APP_MODE variable must be set to 'prod' and a secret key
    must be stored to FLASK_SECRET_KEY."""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")


CONFIG_OPTIONS = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig
}
