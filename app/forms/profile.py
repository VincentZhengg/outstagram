from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

