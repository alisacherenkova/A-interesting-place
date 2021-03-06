from init import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    xCoor = db.Column(db.Float, nullable=False)
    yCoor = db.Column(db.Float, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    popup = db.Column(db.String(100), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)