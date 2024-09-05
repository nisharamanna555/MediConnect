from flask import session
from functools import wraps

def protected_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if session.get('logged_in'):
            return route(*args, **kwargs)
        else:
            return 'unauthorized for this url'
    return wrapper

def patient_protected_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'usertype' in session:
            if session['usertype'] == 'patient':
                return route(*args, **kwargs)
            else:
                return 'unauthorized for this url'
    return wrapper

def physician_protected_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'usertype' in session:
            if session['usertype'] == 'physician':
                return route(*args, **kwargs)
            else:
                return 'unauthorized for this url'
    return wrapper

def pharmacy_protected_route(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        if 'usertype' in session:
            if session['usertype'] == 'pharmacy':
                return route(*args, **kwargs)
            else:
                return 'unauthorized for this url'
    return wrapper

