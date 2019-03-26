from flask import Flask, render_template, request, flash, redirect, url_for, session
from .forms import SignupForm, EditProfile
from passlib.hash import sha256_crypt
from .forms import SignupForm, LoginForm
from ListenUp import app,db
from .models import User,Arguments
from flask_login import login_user

@app.route("/")
def home():
    return render_template("index.html")

# Make this actually work
@app.route("/login_page" ,methods = ['GET','POST'])
def login_page():
    form = LoginForm(request.form)
    if request.method == 'POST':
        app.logger.info('Hereeeee')
        user = User.query.filter_by(email = form.email.data).first()
        if user and sha256_crypt.verify(form.password.data,user.password):
            login_user(user)
            return redirect(url_for('discussionhome'))
        app.logger.info('Error')
        flash('You have entered an incorrect email/password!')
    return render_template("Login_Page.html")

@app.route("/signup_page", methods = ['GET','POST'])
def signup_page():
    form = SignupForm(request.form)
    if request.method =='POST' and form.validate():
        encPass=sha256_crypt.encrypt(str(form.password.data))
        user = User(username=form.username.data, email = form.email.data,password=encPass)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!', 'success')
        return redirect(url_for('home'))
    return render_template("Signup_Page.html", form=form)


@app.route("/discussionhome", methods = ['GET','POST'])
def discussionhome():
    return render_template("discussionhome.html")

@app.route("/logout.html", methods = ['GET','POST'])
def logout():
    flash('You have successfully logged out!')
    return render_template("index.html")


#Route to edit profile form
@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfile(request.form)
    if request.method == 'POST' and form.validate():
        if request.method == 'POST' and form.validate():

            profile = Profile(name=form.name.data, bio=form.bio.data, title=form.title.data)
            db.session.add(profile)
            db.session.commit()
            flash('You have successfully edited profile!', 'success')
            return redirect(url_for('discussionhome'))
        return render_template("", form=form)
    return render_template("editprofile.html", form=form)



@app.route("/profile.html", methods = ['GET','POST'])
def profile():
    return render_template("profile.html")