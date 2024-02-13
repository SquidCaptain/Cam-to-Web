from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import UserMixin

db = SQLAlchemy()

## --Database Models--
# Users table
# primary key: user_id
class Users(db.Model, UserMixin):
    __tabelname__= 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<User id: {self.user_id}, Userame: {self.username}, Password: {self.password}>'
    
    def get_id(self):
           return (self.user_id)

# Cameras table
# primary key: camera_id
class Cameras(db.Model):
    __tabelname__= 'cameras'
    camera_id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(30), unique=True, nullable=False)
    uri = db.Column(db.String(), nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Camera id: {self.camera_id} Alias: {self.alias} URI: {self.uri} Resolution: {self.width}x{self.height}>'