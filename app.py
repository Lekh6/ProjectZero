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


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please enter all details!", "warn")
            return redirect('/login')

        check = db.execute('SELECT uid, username, passhash FROM users WHERE username = ?', username)
        if len(check) != 1 or not check_password_hash(check[0]['passhash'], password):
            flash("Invalid username or password!", "error")
            return redirect('/login')

        session['user_id'] = check[0]['uid']
        flash(f"Welcome back, {username}!", "success")
        return redirect('/')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repass = request.form.get('repass')

        if not username or not password or not repass:
            flash('Please enter all details!', 'warn')
            return redirect('/register')
        elif password != repass:
            flash('Passwords do not match!', 'error')
            return redirect('/register')

        try:
            db.execute('INSERT INTO users(username, passhash) VALUES(?, ?)', username, generate_password_hash(password))
            uid = db.execute('SELECT uid FROM users WHERE username = ?', username)[0]['uid']
            first_login(uid)
            flash('Registration successful! Please log in.', 'success')
        except Exception:
            flash('Registration failed! Try again.', 'error')

        return redirect('/login')

    return render_template('register.html')


@app.route("/", methods=['GET', 'POST'])
@login_required
def homepage():
    uid = session['user_id']

    if request.method == 'POST':
        task = request.form.get('tasks')
        priority = request.form.get('priority')
        desc = request.form.get('description')
        due = request.form.get('finby')
        notes = request.form.get('notes')

        if not task:
            flash('Task cannot be empty!', 'warn')
        else:
            try:
                db.execute(f'INSERT INTO data_{uid}(title, priority, description, finby) VALUES(?, ?, ?, ?)',
                           task, priority, desc, due)
                if notes:
                    db.execute(f'INSERT INTO notes_{uid}(content) VALUES(?)', notes)
                flash('Task added successfully!', 'success')
            except Exception as e:
                flash('Error saving task. Please try again.', 'error')

        return redirect('/')


    high = db.execute(f"SELECT COUNT(*) as c FROM data_{uid} WHERE priority='high'")[0]['c']
    medium = db.execute(f"SELECT COUNT(*) as c FROM data_{uid} WHERE priority='medium'")[0]['c']
    low = db.execute(f"SELECT COUNT(*) as c FROM data_{uid} WHERE priority='low'")[0]['c']
    dat = db.execute(f'SELECT * FROM data_{uid} WHERE status = 0 ORDER BY date(finby) ASC')
    return render_template('homepage.html', tasks=dat, counts=[high, medium, low])

    


@app.route('/update', methods=['POST'])
@login_required
def update():
    uid = session['user_id']
    tid = request.form.get('task_id')
    done = 1 if request.form.get('done') else 0
    cdate = date.today().isoformat() if done else None
    db.execute(f"UPDATE data_{uid} SET status = ?, donedate = ? WHERE id = ?", done, cdate, tid)
    flash("Task updated successfully!", "success")
    return redirect('/')


@app.route('/timeline')
@login_required
def timeline():
    uid = session['user_id']
    filter = request.args.get('filter', 'week')
    act = {'week': 7, 'month': 30, 'year': 365}[filter]

    data_created = db.execute(
        f"SELECT date(creation) AS day, COUNT(*) AS total FROM data_{uid} "
        "WHERE creation >= date('now', ?) GROUP BY day",
        f'-{act} days'
    )
    data_completed = db.execute(
        f"SELECT date(donedate) AS day, COUNT(*) AS total FROM data_{uid} "
        "WHERE status = 1 AND donedate >= date('now', ?) GROUP BY day",
        f'-{act} days'
    )

    return render_template('timeline.html',
                           data_created=data_created,
                           data_completed=data_completed,
                           period=filter)


@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    uid = session['user_id']

    if request.method == 'POST':
        note = request.form.get('notes')
        if note and note.strip():
            db.execute(f'INSERT INTO notes_{uid}(content) VALUES(?)', (note,))
            flash("Note saved successfully!", "success")
        else:
            flash("Cannot save empty note!", "warn")
        return redirect('/notes')

    notes = db.execute(f'SELECT * FROM notes_{uid} ORDER BY creation DESC')
    return render_template('notes.html', notes=notes)


@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    uid = session['user_id']

    if request.method == 'POST' and request.is_json:
        try:
            data = request.get_json()
            tid = data.get('id')
            done = data.get('done')
            db.execute(f'UPDATE data_{uid} SET status=? WHERE id=?', done, tid)
            flash("Task updated!", "success")
        except Exception:
            flash("Failed to update task.", "error")
        return ('', 204)

    cat = {'now': [], 'later': [], 'flexible': [], 'indefinite': []}
    tasks = db.execute(f'SELECT * FROM data_{uid} WHERE status = 0')
    for task in tasks:
        finby = task['finby']
        if not finby:
            diff = None
        else:
            try:
                findate = datetime.strptime(finby, "%Y-%m-%d").date()
                diff = (findate - date.today()).days
            except:
                diff = None

        if diff is not None and diff <= 1:
            filt = 'now'
        elif diff is not None and diff <= 7:
            filt = 'later'
        elif diff is not None and diff <= 31:
            filt = 'flexible'
        else:
            filt = 'indefinite'

        cat[filt].append(task)

    return render_template('overview.html',
                           now=cat['now'],
                           later=cat['later'],
                           flexible=cat['flexible'],
                           indefinite=cat['indefinite'])


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect('/login')
