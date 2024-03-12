import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

## Flask (and extensions) config class
class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, './cam-to-web-db/cam_to_web.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "tempsecretkey"