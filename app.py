from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, flash, redirect, url_for, session
from flaskmysqldb import MySQL
import logging
from passlib.hash import sha256_crypt
from .forms import SignupForm


import sys


app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='ListenUpLocal'
app.config['MYSQL_CURSORCLASS']='DictCursor'
app.secret_key='secret123'

mysql=MySQL(app)



@app.route("/")
def home():
    return render_template("index.html")

# Make this actually work
@app.route("/login_page" ,methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        if result >0:
            data = cur.fetchone()
            real_password = data['password']

            if sha256_crypt.verify(password, real_password):
                app.logger.info('You have successfully logged in')
            else:
                app.logger.info('You have entered an incorrect password')

        else:
            app.logger.info('No users with that username found')
    return render_template("Login_Page.html")

@app.route("/signup_page", methods = ['GET','POST'])
def signup_page():
    form = SignupForm(request.form)
    if request.method =='POST' and form.validate():
        username=form.username.data
        email=form.email.data
        password=sha256_crypt.encrypt(str(form.password.data))
        cur = mysql.connection.cursor()


        cur.execute("INSERT INTO users(username,email,password) VALUES (%s, %s,%s)" , (username,email,password))

        mysql.connection.commit()
        cur.close()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('home'))


    return render_template("Signup_Page.html", form=form)


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host="127.0.0.1")
