from flask import Flask
from firebase import firebase

app=Flask(__name__)
firebase = firebase.FirebaseApplication('change this', None)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
