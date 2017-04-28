from datetime import datetime
from app.extensions import db


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)
    comment = db.Column(db.UnicodeText)
    post_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.Column(db.Integer)


