"""
User authentication.
"""
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from chatbot.db import get_db

# Create a blueprint for authentication
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Associate the route with the register view
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ Registration route 
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                create_user(name, email, password)
            except db.IntegrityError:
                error = f"User with Email {email} is already registered."
            else:
                return redirect(url_for("auth.login", sign_up_success=True))
        flash(error, 'text-danger')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ Login route
    """
    if request.method == 'GET':

        # If already logged in, redirect to dashboard
        if g.user:
            return redirect(url_for("dashboard.dashboard"))

        # Show sign up success method if redirected from signup
        sign_up_success = request.args.get('sign_up_success')
        if sign_up_success:
            success_message = "Success! You can now log in."
            flash(success_message, 'text-success')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_from_db(email)
        
        error = None
        if user is None:
            error = f'No user with Email {email} found'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            user_id = user['id']
            set_logged_in_user(user_id)
            return redirect(url_for("dashboard.dashboard"))

        flash(error, 'text-danger')

    return render_template('auth/login.html')
    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    """ Require login for a view.

    Can be used as a decorator for views for which
    login is required.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def set_logged_in_user(user_id):
    """ Set the user as the current active user in this session. """
    session.clear()
    session['user_id'] = user_id

# This is executed before every request
@bp.before_app_request
def load_logged_in_user():
    """ Stores the currently active user in the g object"""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# def get_active_user() -> int:
#     """ Get the currently active user. """
#     return session.get('user_id')

def create_user(name: str, email: str, password: str):
    """ Create a user and add to database

    Throws a db.IngerityError if user already exists.
    """
    db = get_db()
    db.execute(
        "INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    db.commit()


def get_user_from_db(email: str):
    """ Load the user info from the database
    """
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE email = ?', (email,)
    ).fetchone()
    return user