from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_login import LoginManager


app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

app.secret_key='secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
# #adding more databases
# SQLALCHEMY_BINDS = {
#     'profiles':        'mysqldb://localhost/profiles'
#}
#app.config['SQLALCHEMY_BINDS'] = {'arguments' : 'sqlite:///Arguments.db'}


db = SQLAlchemy(app)
login_manager = LoginManager(app)
from ListenUp import routes

