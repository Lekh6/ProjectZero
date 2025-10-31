from functools import wraps 
from flask import redirect, session


def login_required(f):
    @wraps(f)
        def check(*args, **kwargs):
            if session.get('user_id') is None:
                return redirect('login.html')
            return(*args, **kwargs)
    return check