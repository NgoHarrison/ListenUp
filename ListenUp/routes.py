from flask import Flask, render_template, request, flash, redirect, url_for, session
from .forms import SignupForm
from passlib.hash import sha256_crypt
from .forms import SignupForm, LoginForm, PostArgument
from ListenUp import app,db
from .models import User,Arguments
from flask_login import login_user, login_required, current_user


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login_page" ,methods = ['GET','POST'])
def login_page():
    form = LoginForm(request.form)
    if request.method == 'POST':
        #app.logger.info('Hereeeee')
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
@login_required
def discussionhome():
    arguments = Arguments.query.filter_by(root_arg=True)
    return render_template("discussionhome.html", arguments = arguments)

@app.route("/logout.html", methods = ['GET','POST'])
@login_required
def logout():
    flash('You have successfully logged out!')
    return render_template("index.html")

@app.route("topics/<topic_id>")
def topic(topic_id):
    argument =  Argument.query.filter_by(id=topic_id)
    
    argument_children = list(map(lambda child: Argument.query.filter_by(id=int(child)), argument.children.split(',')))
    
    return render_template("topics.html", main_argument = argument, children=argument_children)

@app.route("/topics/<topic_id>/new", methods = ["GET", "POST")
@login_required
def new_arg(topic_id):
    form = PostArgument(request.form)
    if request.method == 'POST' and form.validate():
         argument = Arguments(title=form.title.data,content=form.content.data,author = current_user,root_arg=False,children="")
         db.session.add(argument)
         db.session.commit()
         Argument.query.filter_by(id=topic_id).children=Argument.query.filter_by(id=topic_id).children+argument.id+","
         flash('You have succesfully posted!')
         return redirect(url_for('discussionhome'))


@app.route("/discussionhome/new",methods = ['GET','POST'])
@login_required
def new_debate():
    form = PostArgument(request.form)
    if request.method == 'POST' and form.validate():
        argument = Arguments(title=form.title.data,content=form.content.data,author = current_user,root_arg=True,children="")
        db.session.add(argument)
        db.session.commit()
        flash('You have succesfully posted!')
        return redirect(url_for('discussionhome'))
    return render_template('create_debate.html', title = 'New debate', form = form)
