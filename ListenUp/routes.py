from flask import Flask, render_template, request, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from .forms import SignupForm, LoginForm,PostArgument, ExpandDebate, editDebate
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
        a_o_d = None
        if 'agree' in request.form:
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
        return render_template('view_debate.html', title=request.args.get('title'),
                               arguments_id=request.args.get('argument_id'),
                               content=request.args.get('content'), org_author=request.args.get('org_author'),
                               sub_author=request.args.get('sub_author'),
                               curr=current_user,
                               right_args=right_args, left_args=left_args, left_len=left_len, right_len=right_len)

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
    return render_template('create_debate.html', title = 'New debate', form = form)



@app.route("/discussionhome/view", methods = ['GET', 'POST'])
@login_required
def view_debate():
    if request.args.get('likes')== "pressed" or request.args.get('dislikes') == "pressed":
        #app.logger.info("YESSIR")
        # app.logger.info("YERRRR "+str(a_o_d))
        curr_id = current_user.get_id()
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


        if request.args.get('likes') =="pressed":
            arg.likes=arg.likes+1
            #app.logger.info("OOOOOH")
            db.session.commit()
        else:
            arg.dislikes=arg.dislikes+1
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
            a_o_d = None
            if 'agree' in request.form:
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
            return render_template('view_debate.html', title=request.args.get('title'),
                                   arguments_id=request.args.get('argument_id'),
                                   content=request.args.get('content'), org_author=request.args.get('org_author'),
                                   sub_author=request.args.get('sub_author'),
                                   curr=current_user,
                                   right_args=right_args, left_args=left_args, left_len=left_len, right_len=right_len)

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
