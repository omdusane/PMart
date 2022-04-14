from . import db
from flask_login import UserMixin
from datetime import date

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    company = db.Column(db.String(150), nullable=False)
    created_date = db.Column(db.Date, default= date.today())
    last_modified_date = db.Column(db.Date, default = date.today())
    manufactured_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    description = db.Column(db.String(500), nullable=True)
    rack_no = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(20))
    items = db.relationship('Item', backref='user', cascade='all, delete')