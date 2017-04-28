from app.extensions import db


class Sentence(db.Model):

    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer)
    episode = db.Column(db.Integer)
    sentence = db.Column(db.Text)
    search = db.Column(db.Integer)

