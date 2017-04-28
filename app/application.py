import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from config import config
from app import views
from app.extensions import bootstrap, mail, moment, db, login_manager, photos
from app.email import SSLSMTPHandler
from flask_uploads import configure_uploads


DEFAULT_BLUEPRINTS = (
    (views.main, ""),
    (views.auth, "/auth"),
    (views.users, "/user")
)


def create_app(config_name, blueprints=None):

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(__name__)

    configure_app(app, config_name)
    configure_errorhandlers(app)
    configure_extensions(app)
    configure_blueprints(app, blueprints)
    configure_logging(app)
    configure_uploads(app, photos)

    return app


def configure_app(app, config_name):

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


def configure_errorhandlers(app):

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", error=error), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html", error=error), 403

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html", error=error), 500


def configure_extensions(app):

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def configure_blueprints(app, blueprints):

    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_logging(app):

    if app.debug or app.testing:
        return

    mail_handler = \
        SSLSMTPHandler(mailhost=app.config['MAIL_SERVER'],
                       fromaddr=app.config['FLASKY_MAIL_SENDER'],
                       toaddrs=(app.config['FLASKY_ADMIN'], ),
                       subject='application error',
                       credentials=
                       (
                            app.config['MAIL_USERNAME'],
                            app.config['MAIL_PASSWORD'],
                       ))

    mail_handler.setLevel(logging.INFO)
    app.logger.addHandler(mail_handler)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    # debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    #
    # debug_file_handler = \
    #     RotatingFileHandler(debug_log,
    #                         maxBytes=100000,
    #                         backupCount=10)
    #
    # debug_file_handler.setLevel(logging.DEBUG)
    # debug_file_handler.setFormatter(formatter)
    # app.logger.addHandler(debug_file_handler)

    info_log = os.path.join(app.root_path,
                            app.config['INFO_LOG'])

    info_file_handler = \
        RotatingFileHandler(info_log,
                            maxBytes=100000,
                            backupCount=10)

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

