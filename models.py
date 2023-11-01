from . import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    my_orders = db.relationship('Orders')


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    counter_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, default='0')
    counter_id = db.Column(db.Integer, db.ForeignKey('counter.id'))
    counter = db.relationship('Counter', back_populates='foods')

class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    foods = db.relationship('Food', back_populates='counter')

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(10), nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)
    counter_name = db.Column(db.String(500), nullable=False)
    ord_id = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

