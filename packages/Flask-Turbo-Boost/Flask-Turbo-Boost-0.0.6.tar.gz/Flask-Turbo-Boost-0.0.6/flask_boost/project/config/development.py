# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = "postgresql://jing:@localhost/marcop"

    # Flask Security
    # https://pythonhosted.org/Flask-Security/configuration.html
    # SECURITY_PASSWORD_HASH
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
