from datetime import datetime
from app.extensions import db


class Collection(db.Model):

    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    word_id = db.Column(db.Integer)
    collect_date = db.Column(db.DateTime, default=datetime.utcnow)


