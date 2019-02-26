from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, flash, redirect, url_for, session
import logging
from .forms import SignupForm
from methods import login_worked, create_user
import sys


app=Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def home():
    return render_template("index.html")

# Make this actually work
@app.route("/login_page" ,methods = ['GET','POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_worked(username, password):
            flash('You have logged in!', 'success')
            app.logger.info('You have successfully logged in')
        else:
            app.logger.info('Invalid username or password')
            flash('Invalid username or password', 'failure')
    return render_template("Login_Page.html")

@app.route("/signup_page", methods = ['GET','POST'])
def signup_page():
    form = SignupForm(request.form)
    if request.method =='POST' and form.validate():
        username=form.username.data
        email=form.email.data
        create_user(username, email, password)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('home'))

    return render_template("Signup_Page.html", form=form)


if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, host="127.0.0.1")
