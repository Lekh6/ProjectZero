from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = db = SQL("sqlite:///users.db")

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        pass = request.form.get('password')
        if not username or pass:
            flash("Please enter all details!")
            return redirect('/login')
        check = db.execute('select username from users where username = ?', username)
        if len(check) != 1 or not check_password_hash(check[0]['hash'], pass):
            flash('User does not exist, Please Register')
            return redirect('/register')
        
        session['user_id'] = check[0]['id']

        return redirect{'/'}
    return render_template('login.html')

@app.route('/', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repass = request.form.get('repass')
        if not username or not password or not repass:
            flash('Please enter all details!')
            return redirect('/register')
        elif password != repass:
            flash('Passwords do not match!')
            return redirect('/register')
        msg = db.execute('insert into users(username, hash) values(? , ?)', username, generate_password_hash(password))
        if not msg:
            flash('Registration failed! Please try again!')
            return redirect('/register')
        db.commit()
        flash('Registration successful! Please log in!')
        return redirect('/login')
    return render_template('register.html')

@login_required
@app.route("/", methods = ['GET', 'POST'])
def homepage():
    