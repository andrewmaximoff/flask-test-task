import functools

from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from core import db
from core.forms import LoginForm, RegistrationForm
from core.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


def redirect_if_logged(view):
    """If a user id is stored in the session,
    redirect user from login and registration page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('records.index'))

        return view(**kwargs)

    return wrapped_view


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()


@bp.route('/register', methods=('GET', 'POST'))
@redirect_if_logged
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
@redirect_if_logged
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('records.index'))
        else:
            error = 'Incorrect email or password.'
    return render_template('auth/login.html', form=form, error=error)


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('records.index'))
