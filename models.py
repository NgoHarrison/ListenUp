from flask_login import UserMixin

from ListenUp import db,login_manager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    arguments = db.relationship('Arguments', backref='author', lazy=True)

    def __repr__(self):
        return ("")

#New Profile model for Profile Database, to be linked with foreign_keys
class Profile(db.Model):
    name = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    bio = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(20), unique=True, nullable=False)

class Arguments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ("")



