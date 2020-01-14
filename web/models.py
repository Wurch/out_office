from app import app

from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    amdin = db.Column(db.Boolean)

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50))

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Columns(db.String(20))
    place_id = db.Column(db.String(50), db,ForeignKey('places.id', ondelete="CASCADE"))