from datetime import datetime
from Home4u import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


stayed = db.Table('stayed',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('house_id', db.Integer, db.ForeignKey('house.id'), primary_key=True)
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.Integer(), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    firstname = db.Column(db.String(20), nullable=True)
    surname = db.Column(db.String(20), nullable=True)
    sex = db.Column(db.String(8), nullable=True)
    reviews = db.Column(db.String, default='0.0')
    selected_id = db.Column(db.Integer)
    houses = db.relationship('House', secondary=stayed , lazy='subquery', backref=db.backref('has_stayed', lazy=True))
   
   

class Owner(User):
    pass
    #houses = db.relationship('House', backref='owner', lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.Integer(), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(200))



class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    house_name = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    square_meters = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    house_type = db.Column(db.String(20), nullable=True)
    visitors = db.Column(db.Integer(), nullable=True)
    user_id = db.Column(db.Integer())
    image_file = db.Column(db.String(20), nullable=False, default='default_house.png')

class HouseSelector(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     house_id = db.Column(db.Integer())


class SearchInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(60), nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=True)
    guests = db.Column(db.Integer())

    
     