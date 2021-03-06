import uuid

from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from core import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(), primary_key=True, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120))
    records = db.relationship('Record', backref='user', lazy=True)

    def __init__(self, *args, **kwargs):
        self.id = uuid.uuid4().urn
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'<id {self.id}>'

    def __str__(self):
        return f'<User {self.first_name} {self.last_name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
