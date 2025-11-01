from functools import wraps 
from flask import redirect, session


def login_required(f):
    @wraps(f)
        def check(*args, **kwargs):
            if session.get('user_id') is None:
                return redirect('login.html')
            return(*args, **kwargs)
    return check

def first_login(user_id):
    try:
        db = SQL("sqlite:///users.db")
        db.execute(f'create table if not exists data_{user_id}(' \
        'id integer primary key autoincrement,' \
        'title text not null,' \
        'description text,' \
        'priority text check(priority in ('low', 'medium', 'high'))),'
        'due date,'
        'creation default current timestamp')

        db.execute(f'create table if not exists notes_{user_id}(
                   id primary key autoincrement,
                   content text not null,
                   creation timestamp default current_timestamp)')
        db.commit()
        db.close()
        return True
    except Exception as e:
        print('Error: ', e)
        return False

