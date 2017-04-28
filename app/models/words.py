from app.extensions import db


class Word(db.Model):

    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    img = db.Column(db.String(256))
    voice = db.Column(db.String(256))
    sentence = db.Column(db.Text)





