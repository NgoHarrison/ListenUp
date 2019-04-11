from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import logging
from flask_login import LoginManager


app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']='123456'
#app.config['MYSQL_DB']='ListenUpLocal'
#app.config['MYSQL_CURSORCLASS']='DictCursor'
#app.secret_key='secret123'

#mysql=MySQL(app)
app.secret_key='secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
# #adding more databases
# SQLALCHEMY_BINDS = {
#     'profiles':        'mysqldb://localhost/profiles'
#}
#app.config['SQLALCHEMY_BINDS'] = {'arguments' : 'sqlite:///Arguments.db'}


db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
login_manager = LoginManager(app)
from ListenUp import routes


if __name__== '__main__ ':
    manager.run()

