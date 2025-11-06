from functools import wraps 
from flask import redirect, session
from cs50 import SQL

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def first_login(user_id):
    try:
        db = SQL("sqlite:///users.db")
        print('DEBUG: creation has started')
        db.execute(f"""
        CREATE TABLE IF NOT EXISTS data_{user_id} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT CHECK(priority IN ('low', 'medium', 'high')),
            finby DATE,
            status integer default 0,
            donedate date,
            creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute(f"""
            CREATE TABLE IF NOT EXISTS notes_{user_id} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print('created successfully')
        return True
    except Exception as e:
        print('Error creating tables: ', e)
        return False

