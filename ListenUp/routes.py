from flask import Flask, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from .forms import SignupForm, LoginForm,PostArgument, ExpandDebate, editDebate, EditProfile, EditAccount, ChangePassword
from ListenUp import app,db
from .models import User,Arguments, load_user, singleArgument, like_dislike
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

@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    return render_template("account.html")

@app.route("/profile", methods = ['GET','POST'])
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user = user)

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
        #update values
        #db.session.query(User).filter(User.username == form.username).update({'name': str(form.username),})
        #db.session.query(User).filter(User.email == form.email).update({'bio': 'New Foobar Name!'})
        #db.session.commit()
        flash('Passwords do not match', 'no success') 
        
       
    return render_template("changepassword.html", form=form)



@app.route("/discussionhome/view/expand", methods=['GET','POST'])
@login_required
def expand_debate():
    # app.logger.info("YELLO")
    # user = User.query.filter_by(id=load_user(current_user.get_id())).first()
    curr_id = current_user.get_id()
    user = load_user(curr_id)
    # app.logger.info(curr_id)
    # app.logger.info(user.email)
    # app.logger.info(request.args.get('author_id'))
    # author_id = request.args.get('author_id')
    curr = singleArgument.query.filter_by(author_id=curr_id).first()
    # app.logger.info(curr is None)
    # app.logger.info(request.args.get('author_id'))
    # app.logger.info('YERRRRRR '+str(curr))
    form = ExpandDebate(request.form)
    if request.method == 'POST' and form.validate():
        option = request.form['aod']
        #app.logger.info("YESSSIRRRRRR "+str(option))
        #app.logger.info(str(option=='agree'))
        a_o_d = None
        if option=='agree':
            a_o_d = True
        else:
            a_o_d = False
        # app.logger.info("YERRRR "+str(a_o_d))
        use = User.query.filter_by(id=curr_id).first()
        # app.logger.info('YERRRR '+str(use.username))
        # app.logger.info("YELLOW "+use.username)
        expand = singleArgument(arguments_id=request.args.get('org_arg'), author_id=curr_id,
                                content=form.content.data, agree_or_disagree=a_o_d, username=use.username)
        db.session.add(expand)
        db.session.commit()
        right_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        left_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        left_len = 0
        right_len = 0
        for arg in left_args:
            if arg.agree_or_disagree == False:
                left_len += 1
        for arg2 in right_args:
            if arg2.agree_or_disagree == True:
                right_len += 1
        return render_template('view_debate.html', title=request.args.get('title'), curr=current_user,
                                   arguments_id=request.args.get('argument_id'),
                                   content=request.args.get('content'), org_author=request.args.get('org_author'),
                                    org_arg=request.args.get('org_arg'),
                                   author_id=request.args.get('author_id'),
                                   right_args=right_args, left_args=left_args, left_len=left_len,
                                   right_len=right_len)

    return render_template('expand_debate.html', title=request.args.get('title'),
                           arguments_id=request.args.get('argument_id'),
                           content=request.args.get('content'), org_author=request.args.get('org_author'),
                           sub_author=request.args.get('sub_author'),
                           curr=current_user)
@app.route("/discussionhome/view/edit", methods = ['GET','POST'])
@login_required
def edit_debate():
    form=editDebate(request.form)
    current_content=request.args.get('subcontent')
    #app.logger.info(singleArgument.query.filter_by(arguments_id=request.args.get('argument_id')).first().content)
    if request.method == 'POST' and form.validate():
        arg=singleArgument.query.filter_by(id=request.args.get('argument_id')).first()
        arg.content=form.content.data
        db.session.commit()
        author_id = request.args.get('author_id')
        right_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        left_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        left_len = 0
        right_len = 0
        for arg in left_args:
            if arg.agree_or_disagree == False:
                left_len += 1
        for arg2 in right_args:
            if arg2.agree_or_disagree == True:
                right_len += 1
            # app.logger.info("YERR" + left_args[0].author.username)
        return render_template('view_debate.html', title=request.args.get('title'), curr=current_user,
                               arguments_id=request.args.get('argument_id'),
                               content=request.args.get('content'), org_author=request.args.get('org_author'),
                               org_arg=request.args.get('org_arg'),
                               author_id=author_id,
                               right_args=right_args, left_args=left_args, left_len=left_len,
                               right_len=right_len)  # return render_template('view_debate.html', title = request.args.get('title'), argument = request.args.get('content'), author = author.username)

    #<a href={{ url_for( 'edit_debate', content=content,subcontent = rarg.content, author_id = author_id, author = rarg.author.username, argument_id=rarg.id)}} style="float:right;">Edit</a>
    #return render_template('edit_debate.html',content=request.args.get('content'),subcontent=request.args.get('subcontent'),author_id=request.args.get('author_id'),author=request.args.get('author'),argument_id=request.args.get('argument_id'))
    return render_template('edit_debate.html',form = form)
@app.route("/discussionhome/new",methods = ['GET','POST'])
@login_required
def new_debate():
    form = PostArgument(request.form)
    if request.method == 'POST' and form.validate():
        argument = Arguments(title=form.title.data,content=form.content.data,author = current_user)
        db.session.add(argument)
        db.session.commit()
        return redirect(url_for('discussionhome'))
    return render_template('create_debate.html', title = 'New debate', form = form, org_arg=request.args.get('org_arg'),author=request.args.get('author'))



@app.route("/discussionhome/view", methods = ['GET', 'POST'])
@login_required
def view_debate():
    if request.args.get('likes')== "pressed" or request.args.get('dislikes') == "pressed":
        #app.logger.info("YESSIR")
        # app.logger.info("YERRRR "+str(a_o_d))
        curr_id = current_user.get_id()
        #app.logger.info("WE IN THIS " + str(request.args.get('argument_id')))
        user = load_user(curr_id)
        # app.logger.info(user.email)
        # app.logger.info(request.args.get('author_id'))
        # author_id = request.args.get('author_id')
        curr = singleArgument.query.filter_by(author_id=curr_id).first()
        use = User.query.filter_by(id=curr_id).first()
        # app.logger.info('YERRRR '+str(use.username))
        #expand = singleArgument(arguments_id=request.args.get('argument_id'), author_id=curr_id,
                                #content=request.args.get('content'), agree_or_disagree=a_o_d, username=use.username)
        arg=singleArgument.query.filter_by(content=request.args.get('subcontent')).first()
        #app.logger.info("WE IN THIS "+str(curr_id))
        ld = like_dislike.query.filter_by(author_id=curr_id,single_arg_id=request.args.get('argument_id')).first()
        if request.args.get('likes') =="pressed":
            if ld is None:
                arg.likes=arg.likes+1
                #app.logger.info("OOOOOH")
                lod= like_dislike(single_arg_id=request.args.get('argument_id'),author_id=curr_id)
                db.session.add(lod)
                db.session.commit()
        else:
            if ld is None:
                arg.dislikes=arg.dislikes+1
                lod = like_dislike(single_arg_id=request.args.get('argument_id'), author_id=curr_id)
                db.session.add(lod)
                db.session.commit()
        #app.logger.info("LOLOL "+request.args.get('argument_id'))
        right_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        left_args = singleArgument.query.filter_by(arguments_id=request.args.get('org_arg')).order_by(
            singleArgument.likes.desc())
        #for a in right_args:
            #app.logger.info("INFO "+str(a.content))
        left_len = 0
        right_len = 0
        for arg in left_args:
            if arg.agree_or_disagree == False:
                left_len += 1
        for arg2 in right_args:
            if arg2.agree_or_disagree == True:
                right_len += 1
        app.logger.info("YOLO ")
        return render_template('view_debate.html', title=request.args.get('title'),left_args=left_args,right_args=right_args,
                               argument_id=request.args.get('argument_id'), content=request.args.get('content'), curr=current_user,left_len=left_len,right_len=right_len,
                               subcontent=request.args.get('subcontent'), org_author=request.args.get('org_author'),author_id=curr_id, org_arg=request.args.get('org_arg'))

    else:

        author_id = request.args.get('author_id')
        right_args = singleArgument.query.filter_by(arguments_id=request.args.get('argument_id')).order_by(
        singleArgument.likes.desc())
        left_args = singleArgument.query.filter_by(arguments_id=request.args.get('argument_id')).order_by(
        singleArgument.likes.desc())
        left_len = 0
        right_len = 0
        for arg in left_args:
            if arg.agree_or_disagree == False:
                left_len += 1
        for arg2 in right_args:
            if arg2.agree_or_disagree == True:
                right_len += 1
            # app.logger.info("YERR" + left_args[0].author.username)

        return render_template('view_debate.html', title=request.args.get('title'), curr=current_user,
                                   arguments_id=request.args.get('argument_id'),
                                   content=request.args.get('content'), org_author=request.args.get('org_author'), org_arg=request.args.get('org_arg'),
                                   author_id=author_id,
                                   right_args=right_args, left_args=left_args, left_len=left_len,
                                   right_len=right_len)  # return render_template('view_debate.html', title = request.args.get('title'), argument = request.args.get('content'), author = author.username)
