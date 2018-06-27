import os
from flask import Flask

from config import config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

#mail = Mail()
db = SQLAlchemy()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'connexion'


def create_app(config_name="dev"):
    """ Create the application """
    app = Flask(
        __name__,
        template_folder=config[config_name].template_folder,
        static_folder=config[config_name].static_folder,
        static_url_path="/erasmus/statics",
    )
    if not isinstance(config_name, str):
        app.config.from_object(config)
    else:
        app.config.from_object(config[config_name])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import main_bp
    main_bp.template_folder = config[config_name].template_folder
    main_bp.static_folder = config[config_name].static_folder
    app.register_blueprint(main_bp, url_prefix='/erasmus')

    return app