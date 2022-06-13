from . import db
from flask_login import UserMixin

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    phonenumber = db.Column(db.Integer)
    note = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    firstname = db.Column(db.String(25))
    entries = db.relationship('Entry')
