import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    CAPTCHA_DIR = os.path.join(basedir, 'app/static/captcha')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'E equals mc squared'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = "937037911@qq.com"
    FLASKY_ADMIN = "937037911@qq.com"
    INFO_LOG = "log/app.log"
    TEMPLATES_AUTO_RELOAD = True
    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'app/static/user-photo')
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'app/static/user-photo')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/app'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/app'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/app'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
