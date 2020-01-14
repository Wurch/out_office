# app.py - a minimal flask api using flask_restful
from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'initial.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)

#init ma
ma = Marshmallow(app)

# User class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    amdin = db.Column(db.Boolean)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'public_id', 'name', 'password', 'admin')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Place class
class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(50))

    def __init__(self, name, address):
        self.name = name
        self.address = address

class PlaceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address')

place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)


# Tag class
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20))
    place_id = db.Column(db.String(50), db.ForeignKey('place.id', ondelete="CASCADE"))

class TagSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'tag', 'place_id')

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)

# Add Place
@app.route('/', methods=['POST'])
def add_place():

    name = request.json['name']
    address = request.json['address']
    
    new_place = Place(name, address)

    db.session.add(new_place)
    db.session.commit()

    return place_schema.jsonify(new_place)


@app.route('/', methods=['GET'])
def get_places():
    all_places = Place.query.all()

    result = places_schema.dump(all_places)

    return jsonify(result)


if __name__ == '__main__':
    app.run()