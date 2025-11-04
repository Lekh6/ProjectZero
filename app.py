from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, first_login
from cs50 import SQL
from datetime import datetime, date


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
            print("Please enter all details!")
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
            print('Please enter all details!')
            return redirect('/register')
        elif password != repass:
            print('Passwords do not match!')
            return redirect('/register')
        msg = db.execute('insert into users(username, passhash) values(? , ?)', username, generate_password_hash(password))
        if not msg:
            print('Registration failed! Please try again!')
            return redirect('/register')
        uid = (db.execute('select uid from users where username = ?', username))[0]['uid']
        first_login(uid)
        print('Registration successful! Please log in!')
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
        due = request.form.get('finby')
        print("DUE IS: ", due)
        if not task:
            print('task cannot be empty!')
        else:
            try:
                db.execute(f'insert into data_{uid}(title, priority, description, finby) values(?, ?, ?, ?)', task, priority, desc, due)
            except Exception as e:
                print(task, priority, desc, due)
                print('SQL ERROR: ', e)
        return redirect('/')
    dat = db.execute(f'Select * from data_{uid} where status = 0 order by date(finby) asc')
    print(dat, uid)
    return render_template('homepage.html', tasks = dat)

@app.route('/update', methods = ["POST"])
@login_required
def update():
    uid = session['user_id']
    tid = request.form.get('task_id')
    done = 1 if request.form.get('done') else 0
    db.execute(f"update data_{uid} set status = ? where id = ?", done, tid)
    return redirect('/')

@app.route('/timeline', methods = ['GET', 'POST'])
@login_required
def timeline():
    uid = session['user_id']
    filter = request.args.get('filter', 'week')
    act = {'week': 7, 'month' : 30, 'year': 365}[filter]
    query = db.execute(f"select date(creation) as day, count(*) as total from data_{uid} where creation >= date('now', ?) group by day", f'-{act} days')
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
        due = request.form.get('finby')

        db.execute(f"INSERT INTO data_{uid} (title, description, finby) VALUES (?, ?, ?)", title, desc, due)
        return redirect('/overview')
    
    cat = {'now': [], 'later': [], 'indefinite': [], 'flexible': []}
    tasks = db.execute(f'select * from data_{uid}')
    findate = 0
    for task in tasks:  
        finby = task['finby']
        print("FINBY IS", finby)
        if not finby:
            diff = None
        else:
            try:
                findate = datetime.strptime(task['finby'], "%Y-%m-%d").date()

            except ValueError:
                print("VALUERROR")
                findate = None
            diff = (findate - date.today()).days if findate else None
        print('FINDATE IS :',findate,'|DIFF IS:', diff,'AND ', tasks[1]['finby'])
        if diff is not None and diff <= 1:
            filt = 'now'
        elif diff is not None and diff <= 7:
            filt = 'later'
        elif diff is not None and diff <= 31:
            filt = 'flexible'
        else:
            filt = 'indefinite'
        cat[filt].append(task)
    return render_template('overview.html', cat = cat)



@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/login')
