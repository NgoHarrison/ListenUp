from flask_login import UserMixin
from wtforms import FileField
from sqlalchemy import create_engine, LargeBinary
from ListenUp import db,login_manager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.file import FileRequired
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base







@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    arguments = db.relationship('Arguments', backref='author', lazy=True)
    name = db.Column(db.String(64), nullable=True)
    location = db.Column(db.String(64), nullable=True)
    bio = db.Column(db.String(250), nullable=True)

    #image in progress
    #image = Column(LargeBinary, nullable=True)

    def __repr__(self):
        return ("")


    #member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    #last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    #working on this
    #def ping(self):
     #   self.last_seen = datetime.utcnow()
      #  db.session.add(self)



#New Profile model for Profile Database, to be linked with foreign_keys


class Arguments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return ("")



