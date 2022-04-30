from flask import session, url_for
from functools import wraps
from flask import render_template, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('user', None)
        if user:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function
