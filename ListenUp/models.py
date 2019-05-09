from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from ListenUp import db,login_manager
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    arguments = db.relationship('Arguments', backref='author', lazy=True)
    single_arguments = db.relationship('singleArgument', backref='author', lazy=True)


    def __repr__(self):
        return ""


    #member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    #last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    #working on this
    #def ping(self):
     #   self.last_seen = datetime.utcnow()
      #  db.session.add(self)



#New Profile model for Profile Database, to be linked with foreign_keys


class Arguments(db.Model):
    __tablename__ = 'arguments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    single_args = relationship('singleArgument', backref='arguments')

    def __repr__(self):
        return ""

class singleArgument(db.Model):
    __tablename__='singlearguments'
    id = db.Column(db.Integer, primary_key=True)
    arguments_id = db.Column(db.Integer,ForeignKey('arguments.id'), nullable=False)
    author_id=db.Column(db.Integer,ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    agree_or_disagree = db.Column(db.Boolean, default = None)
    likes=db.Column(db.Integer, default=0)
    dislikes=db.Column(db.Integer, default=0)

    def __repr__(self):
        return ""



    def __repr__(self):
        return ""


#Instad of having a agree,disagree in the arguments table, have them in the single argument
#and also make an empty post. 