from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route("/")
def homepage():
    return redirect('/login')