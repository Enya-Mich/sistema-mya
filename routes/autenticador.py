from functools import wraps
from flask import request, redirect, url_for, session

# Decorador personalizado para verificar la autenticación
def login_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/')
        return view_func(*args, **kwargs)
    return decorated_view
