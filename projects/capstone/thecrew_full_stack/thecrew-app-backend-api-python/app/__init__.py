"""TheCrew API Backend.

The TheCrew is a Casting Agency company that is responsible for creating movies 
and managing and assigning actors to those movies.

So TheCrew API is the backend application that serves and accepts JSON data for 
our applications and third-party applications.

The code follows [PEP 8 style guide](https://pep8.org/).
"""

__author__ = "Filipe Bezerra de Sousa"

import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from flask_bootstrap import Bootstrap
from flask_compress import Compress
from flask_caching import Cache
from dynaconf import FlaskDynaconf
from flasgger import Swagger
from werkzeug.exceptions import default_exceptions

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
bootstrap = Bootstrap()
compress = Compress()
cache = Cache()
swagger = Swagger()


def create_app(**config):
    """Create and initialize the Flask application.

    :param config: Additional kwargs configurations.
    :return An instance of Flask.
    """
    app = Flask(__name__)
    FlaskDynaconf(
        app,
        settings_files=['settings.toml', '.secrets.toml'],
        load_dotenv=False,
        **config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r'/api/*': {'origins': '*'}})
    bootstrap.init_app(app)
    compress.init_app(app)
    cache.init_app(app)
    swagger.init_app(app)

    from app.main import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import bp as api_blueprint
    app.register_blueprint(
        api_blueprint, url_prefix=f'/api/{app.config["THECREW_API_VERSION"]}')

    for code in default_exceptions:
        app.register_error_handler(code, handle_http_exception)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (
                    app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=f'no-reply@{app.config["MAIL_SERVER"]}',
                toaddrs=app.config['THECREW_ADMINS'],
                subject='[TheCrew API] Failure',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config['THECREW_LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/thecrew_api.log', maxBytes=10240, backupCount=10)
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('TheCrew API startup')

    return app


from app import models  # noqa: E402
from app.api.errors import handle_http_exception  # noqa: E402
