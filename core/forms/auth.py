from wtforms import BooleanField, Form, PasswordField, StringField, validators

from core import db
from core.models import User


class RegistrationForm(Form):
    first_name = StringField('First name', [
        validators.DataRequired(),
        validators.Length(min=4, max=32),
    ])
    last_name = StringField('Last name', [
        validators.DataRequired(),
        validators.Length(min=4, max=32),
    ])
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Length(min=4, max=256),
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
    ])
    confirm = PasswordField('Repeat Password', [
        validators.DataRequired(),
    ])

    def validate_email(form, field):
        if db.session.query(db.exists().where(
                User.email == field.data)
        ).scalar():
            raise validators.ValidationError(f'{field.data} is already taken.')


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=4, max=256)])
    password = PasswordField('Password', [
        validators.DataRequired(),
    ])
