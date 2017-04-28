from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
