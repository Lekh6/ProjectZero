from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, first_login
from cs50 import SQL

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")


@app.route('/login', methods = ['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash("Please enter all details!")
            return redirect('/login')
        check = db.execute('select uid, username, passhash from users where username = ?', username)
        if len(check) != 1 or not check_password_hash(check[0]['passhash'], password):
            print(f'DEBUG: {len(check)}')
            return redirect('/login')            
        uid = check[0]['uid']
        session['user_id'] = uid
        return redirect('/')
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
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
        msg = db.execute('insert into users(username, passhash) values(? , ?)', username, generate_password_hash(password))
        if not msg:
            flash('Registration failed! Please try again!')
            return redirect('/register')
        uid = (db.execute('select uid from users where username = ?', username))[0]['uid']
        ch = first_login(uid)
        flash('Registration successful! Please log in!')
        return redirect('/login')
    return render_template('register.html')

 
@app.route("/", methods = ['GET', 'POST'])
@login_required
def homepage():
    uid = session['user_id']
    if request.method == 'POST':
        task = request.form.get('tasks')
        priority = request.form.get('priority')
        desc = request.form.get('description')
        due = request.form.get('due')
        if not task:
            flash('task cannot be empty!')
        else:
            db.execute(f'insert into data_{uid}(title, priority, description, due) values(?, ?, ?, ?)', task, priority, desc, due)
        return redirect('/')
    dat = db.execute(f'Select * from data_{uid}'),fetchall()
    return render_template('homepage.html', tasks = dat)


@app.route('/timeline', methods = ['GET', 'POST'])
@login_required
def timeline():
    uid = session['user_id']
    filter = request.args.get('filter', 'week')
    act = {'week': 7, 'month' : 30, 'year': 365}[filter]
    query = db.execute(f"select date(creation) as day, count(*) as total from user_{uid} where creation >= date('now', ?) group by day", f'-{act} days')
    return render_template('timeline.html', data = query, period = filter)

@app.route('/notes', methods = ['GET', 'POST'])
@login_required
def notes():
    uid = session['user_id']

    if request.method == 'POST':
        note = request.form.get('notes')
        if note:
            db.execute(f'insert into notes_{uid}(content) values(?)', note)
        return redirect('/notes')
    
    notes = db.execute(f'select * from notes_{uid} order by creation desc')
    return render_template('notes.html', notes = notes)

@app.route('/overview', methods = ['GET', 'POST'])
@login_required
def overview():
    uid = session['user_id']
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        due = request.form.get('due')

        db.execute(f"INSERT INTO data_{uid} (title, description, due) VALUES (?, ?, ?)", title, desc, due)
        return redirect('/overview')
    
    cat = {'now': [], 'later': [], 'indefinite': [], 'flexible': []}
    tasks = db.execute(f'select * from data_{uid}')

    for task in tasks:
        diff = (task['due'] - datetime.now().date()).days
        if diff <= 1:
            filt = 'now'
        elif diff <= 7:
            filt = 'later'
        elif diff <= 31:
            filt = 'flexible'
        else:
            filt = 'indefinite'
        cat[filt].append(task)
    return render_template('overview.html', cat = cat)


@app.route('/ts')
def test_flash():
    flash("Hello from Flask!")
    return redirect('/login')
