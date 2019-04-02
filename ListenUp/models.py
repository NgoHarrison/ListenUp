from flask_login import UserMixin

from ListenUp import db,login_manager
from fstring import fstring
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
        return fstring("User({self.username},{self.email})")


class Arguments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    root_arg= db.Column(db.Boolean, nullable=False) # True if root argument, false if it has a parent
    children = db.Column(db.Text, nullable=True) # comma separated list of child arguments
    def __repr__(self):
        return fstring("Post('{self.title}','{self.date_posted}')")



