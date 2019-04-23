from flask import Flask, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from .forms import SignupForm, LoginForm,PostArgument, ExpandDebate
from ListenUp import app,db
from .models import User,Arguments, load_user, singleArgument
from flask_login import login_user, login_required, current_user, logout_user


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
    arguments = Arguments.query.all()
    #list_of_arguments = []
    #for argument in arguments:
        #arg = {'title': argument.title}
        #list_of_arguments.append(arg)
    #app.logger.info(arguments)
    return render_template("discussionhome.html", arguments = arguments)

@app.route("/logout.html", methods = ['GET','POST'])
@login_required
def logout():
    flash('You have successfully logged out!')
    return render_template("index.html")



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

@app.route("/discussionhome/view", methods = ['GET', 'POST'])
@login_required
def view_debate():
    #user = User.query.filter_by(id=load_user(current_user.get_id())).first()
    curr_id = current_user.get_id()
    user = load_user(curr_id)
    #app.logger.info(user.email)
    #app.logger.info(request.args.get('author_id'))
    #author_id = request.args.get('author_id')
    curr = singleArgument.query.filter_by(author_id=curr_id).first()
    #app.logger.info('YERRRRRR '+str(curr))
    if curr is None and request.args.get('author_id') != curr_id:
        form = ExpandDebate(request.form)
        if request.method == 'POST' and form.validate():
            #app.logger.info('LOLLLLLLLLLLL -------- ' + str(current_user.id))
            a_o_d=None
            if 'agree' in request.form:
                a_o_d=True
            else:
                a_o_d=False
            #app.logger.info("YERRRR "+str(a_o_d))
            use = User.query.filter_by(id=curr_id).first()
            app.logger.info('YERRRR '+str(use.username))
            expand = singleArgument(arguments_id=request.args.get('argument_id'),author_id=curr_id,
                                    content=form.content.data, agree_or_disagree=a_o_d,username=use.username)
            db.session.add(expand)
            db.session.commit()
            right_args = singleArgument.query.all()
            # app.logger.info("IM TIRED "+str(right_args.first().content))
            left_args = singleArgument.query.all()
            left_len=0
            right_len=0
            for arg in left_args:
                if arg.agree_or_disagree == False:
                    left_len+=1
            for arg2 in right_args:
                if arg2.agree_or_disagree==True:
                    right_len+=1
            return render_template('view_debate.html', title=request.args.get('title'),
                                   arguments_id=request.args.get('argument_id'),
                                   content=request.args.get('content'), author=request.args.get('author'),
                                   right_args=right_args, left_args=left_args, left_len=left_len,right_len=right_len)

        else:
            right_args = singleArgument.query.all()
            # app.logger.info("IM TIRED "+str(right_args.first().content))
            left_args = singleArgument.query.all()
            return render_template('expand_debate.html', title=request.args.get('title'), arguments_id=request.args.get('argument_id'),
                                    content=request.args.get('content'), author = request.args.get('author'), right_args=right_args,left_args=left_args)
        #return render_template('expand_debate.html',title = request.args.get('title'), argument = request.args.get('content'), author = author.username, author_id = author_id, arguments_id=request.args.get('argument_id'))
    else:
        author = request.args.get('author')
        #app.logger.info(author+"LOOOOOL")
        right_args = singleArgument.query.all()
        # app.logger.info("IM TIRED "+str(right_args.first().content))
        left_args = singleArgument.query.all()
        left_len = 0
        right_len = 0
        for arg in left_args:
            if arg.agree_or_disagree == False:
                left_len += 1
        for arg2 in right_args:
            if arg2.agree_or_disagree == True:
                right_len += 1
        return render_template('view_debate.html', title=request.args.get('title'),
                               arguments_id=request.args.get('argument_id'),
                               content=request.args.get('content'), author=request.args.get('author'),
                               right_args=right_args, left_args=left_args, left_len=left_len, right_len=right_len)#return render_template('view_debate.html', title = request.args.get('title'), argument = request.args.get('content'), author = author.username)


