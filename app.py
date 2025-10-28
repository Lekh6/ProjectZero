from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('layout.html')

@login_required
@app.route("/")
def homepage():
    