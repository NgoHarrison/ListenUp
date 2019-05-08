from flask import Flask, render_template, request, flash, redirect, url_for, session, Session
from .forms import SignupForm, LoginForm, EditAccount, EditProfile, ChangePassword, PostArgument
from passlib.hash import sha256_crypt
from .models import User, Arguments, app, db
from flask_login import login_user, current_user, LoginManager, login_required,
from sqlalchemy import update, literal_column
from .models import User,Arguments
from flask_login import login_user, login_required, current_user, logout_user
login_manager = LoginManager()


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
@login_required
def discussionhome():
    arguments = Arguments.query.all()
    #list_of_arguments = []
    #for argument in arguments:
        #arg = {'title': argument.title}
        #list_of_arguments.append(arg)
    #app.logger.info(arguments)
    return render_template("discussionhome.html", arguments = arguments)


@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    return render_template("account.html")

@app.route("/profile", methods = ['GET','POST'])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user = user)

@app.route("/logout.html", methods = ['GET','POST'])
def logout():
    flash('You have successfully logged out!')
    return render_template("index.html")

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    form = EditProfile(request.form)

    if request.method == 'POST' and form.validate():
        #update profile values
        a_user = current_user
        a_user.name = str(form.name.data)
        a_user.bio = str(form.bio.data)
        a_user.location = str(form.location.data)
        db.session.commit()


        flash('You have successfully edited profile!', 'success')
        return redirect(url_for('profile'))
    return render_template("editprofile.html", form=form)


@app.route("/edit_account", methods=['GET', 'POST'])
def edit_account():
    form = EditAccount(request.form)

    if request.method == 'POST' and form.validate():
        # update account values
        a_user = current_user
        a_user.username = str(form.username.data)
        a_user.email = str(form.email.data)
        db.session.commit()
        #update values
        #db.session.query(User).filter(User.username == form.username).update({'name': str(form.username),})
        #db.session.query(User).filter(User.email == form.email).update({'bio': 'New Foobar Name!'})
        #db.session.commit()

        flash('You have successfully edited account!', 'success')
        return redirect(url_for('account'))
    flash('Passwords do not much')
    return render_template("editaccount.html", form=form)

@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    form = ChangePassword(request.form)

    if request.method == 'POST' and form.validate():

        # update account values
        a_user = current_user
        pass1 = str(form.password.data)
        pass2 = str(form.confirmpassword.data)
        if pass1 == pass2:
            encPass=sha256_crypt.encrypt(str(form.confirmpassword.data))
            a_user.password = encPass
            db.session.commit()
            flash('You have successfully changed your password!', 'success') 
            return redirect(url_for('account'))
        flash('Passwords do not match', 'no success') 
    return render_template("changepassword.html", form=form)



@app.route("/discussionhome/new",methods = ['GET','POST'])
@login_required
def new_debate():
    form = PostArgument(request.form)
    if request.method == 'POST' and form.validate():
        argument = Arguments(title=form.title.data,content=form.content.data,author = current_user)
        db.session.add(argument)
        db.session.commit()
        flash('You have succesfully posted!')
        return redirect(url_for('discussionhome'))
    return render_template('create_debate.html', title = 'New debate', form = form)

@app.route("/discussionhome/expand", methods = ['GET', 'POST'])
@login_required
def expand_debate():
    return render_template('expand_debate.html')



@app.route("/profile", methods = ['GET','POST'])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user = user)
