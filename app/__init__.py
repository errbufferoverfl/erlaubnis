import flask_security  # noqa
from flask import Flask
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_principal import Principal, Identity, AnonymousIdentity, RoleNeed, Permission, identity_loaded, UserNeed
from flask_security import Security
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

"""
Install the extensions
"""
api = Api()
db = SQLAlchemy()
marshmallow = Marshmallow()
migrate = Migrate()

security = Security()
principals = Principal()


@principals.identity_loader
def read_identity_from_flask_login():
    if flask_security.current_user.is_authenticated:
        return Identity(flask_security.current_user.id)
    return AnonymousIdentity()


login_manager = LoginManager()

"""
Define the principals
"""
user_role = Permission(RoleNeed("User"))


def create_app(config_object) -> Flask:
    """
    A Flask application factory -- it’s preferable to create your extensions and app factories so that the
    extension object do not initially get bound to the application.

    See Also:
        - https://flask.pocoo.org/docs/patterns/appfactories/

    Args:
        config_object (Config): the configuration object to use to configure the Flask application

    Returns:
        a Flask application
    """
    app = Flask(__name__.split('.')[0], template_folder="../templates/", static_folder="../static/")
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    with app.app_context():
        register_extensions(app)
        register_blueprints(app)

        db.create_all()
        db.session.commit()

        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            if not isinstance(identity, AnonymousIdentity) and identity.id is not None:
                identity.provides.add(UserNeed(identity.id))

                if identity.user.roles:
                    for role in identity.user.roles:
                        identity.provides.add(RoleNeed(role._name))

        return app


def register_extensions(app: Flask) -> None:
    """
    An extension registration factory.

    Args:
        app (Flask): The Flask application your wish to register the extensions to

    Returns:
        None
    """
    db.init_app(app)
    # Setup Flask-Security for handling login and user management
    from app.models import User, Role

    user_datastore = flask_security.SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_blueprint=True)
    login_manager.init_app(app)

    principals.init_app(app)

    marshmallow.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)


def register_blueprints(app: Flask) -> None:
    """
    A blueprint registration factory, that also configures cross-origin resource sharing rules

    Args:
        app (Flask): The Flask application your wish to register the extensions to

    Returns:
        None
    """
    # front end blueprints

    # API blueprints
    from app import auth
    api.register_blueprint(auth.apis.blueprint)

    from app import user
    api.register_blueprint(user.apis.blueprint)

    from app import core
    app.register_blueprint(core.exceptions.blueprint)


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(user_id)
