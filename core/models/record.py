from datetime import datetime

from core import db


class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<id {self.id}>'

    def __str__(self):
        return f'<Record {self.description}>'
