from ListenUp.models import User
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField
from wtforms.validators import ValidationError

class SignupForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25),validators.DataRequired()],render_kw={"placeholder": "Enter your name..."})
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.DataRequired()],render_kw={"placeholder": "Enter your email..."})
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirmpassword',message='Your passwords do not match')
    ],render_kw={"placeholder": "Enter your password..."})
    confirmpassword = PasswordField('Confirm password',[validators.DataRequired()],render_kw={"placeholder": "Re-enter your password..."})

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=25)],
                           render_kw={"placeholder": "Enter your name..."})
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()],
                        render_kw={"placeholder": "Enter your email..."})
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmpassword', message='Your passwords do not match')
    ], render_kw={"placeholder": "Enter your password..."})

class PostArgument(Form):
    title = StringField('Title', [validators.Length(min=3, max=25)],
                           render_kw={"placeholder": "Enter title..."})
    content = TextAreaField('content', [validators.Length(min=1, max=300), validators.DataRequired()],
                        render_kw={"placeholder": "Enter content..."})
