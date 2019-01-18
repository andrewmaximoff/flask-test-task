from wtforms import Form, TextAreaField, validators

from core import db
from core.models import User


class RecordCreateForm(Form):
    description = TextAreaField('Description', [
        validators.DataRequired(),
        validators.Length(min=1, max=140),
    ])
