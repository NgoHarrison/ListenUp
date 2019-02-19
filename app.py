from flask import Flask
from firebase import firebase
from Flask-Login import LoginForm, LoginManager

app=Flask(__name__)
firebase = firebase.FirebaseApplication('change this', None)

@app.route("/")
def home():
    return render_template("index.html")

# Make this actually work
@app.route("/loginpage", methods=["POST", "GET"])
def login_page():
    return render_template('Login_Page.html', form=LoginForm())

LoginManager().init_app(app)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
