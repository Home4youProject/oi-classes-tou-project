from datetime import datetime
from Home4u import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
    has_stayed = db.Column(db.String, default='0')
    selected_id = db.Column(db.Integer)
    
    
    def stayed(self):
        return [int(x) for x in self.has_stayed.split(';')]
    
    def stayed(self, House):
        self.has_stayed += ';%s' % House.id


    def ratings(self):
        return [float(x) for x in self.reviews.split(';')]
   
    def ratings(self, Review):
        self.reviews += ';%s' % Review.stars


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Owner(User):
    pass
    #houses = db.relationship('House', backref='owner', lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    
     