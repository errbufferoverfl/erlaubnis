import http

import flask_security
from flask.views import MethodView
from flask_login import current_user
from flask_smorest import Blueprint

from app.core.exceptions import UnauthorizedAction
from app.user import serialisers, models, controller

blueprint = Blueprint("user", "user", url_prefix="/api/users", description="User operations")


@blueprint.route("/session")
class Session(MethodView):

    @blueprint.arguments(serialisers.UserSessionSchema, as_kwargs=True)
    @blueprint.response(http.HTTPStatus.CREATED, serialisers.UserSchema)
    @blueprint.alt_response(http.HTTPStatus.NO_CONTENT, http.HTTPStatus.NO_CONTENT.name)
    @blueprint.alt_response(http.HTTPStatus.FOUND, http.HTTPStatus.FOUND.name, schema=serialisers.UserSchema)
    def put(self, **kwargs):
        """
        Create new user session

        Creates a new user session and returns the authenticated users details,
        otherwise returns the logged-in users details.
        ---
        Args:
            **kwargs (dict): {
                username: the user attempting to authenticate,
                password: the password of the user attempting to authenticate
            }

        Returns:
            model.User: the details of the authenticated user
            int: the corresponding HTTP Status code

        """
        if current_user.is_authenticated:
            return current_user, http.HTTPStatus.FOUND
        else:
            user = controller.login(kwargs.get("username"), kwargs.get("password"))
            if user is not None:
                return user, http.HTTPStatus.CREATED
            else:
                return http.HTTPStatus.NO_CONTENT


@blueprint.route("/session/me")
class UserSession(MethodView):
    @blueprint.response(http.HTTPStatus.FOUND, serialisers.UserSchema)
    @blueprint.alt_response(http.HTTPStatus.UNAUTHORIZED, http.HTTPStatus.UNAUTHORIZED.name)
    def get(self):
        if current_user.is_authenticated:
            return controller.get(**{"user_id": current_user.user_id}), http.HTTPStatus.FOUND
        else:
            raise UnauthorizedAction()

    @blueprint.response(http.HTTPStatus.NO_CONTENT)
    @blueprint.alt_response(http.HTTPStatus.UNAUTHORIZED, http.HTTPStatus.UNAUTHORIZED.name)
    def delete(self):
        if current_user.is_authenticated:
            flask_security.logout_user()
        else:
            raise UnauthorizedAction()


@blueprint.route("/")
class User(MethodView):

    @blueprint.arguments(serialisers.UserSessionSchema, as_kwargs=True)
    @blueprint.response(http.HTTPStatus.CREATED, serialisers.UserSchema)
    @blueprint.alt_response(http.HTTPStatus.FOUND, http.HTTPStatus.FOUND.name, schema=serialisers.UserSchema)
    @blueprint.alt_response(http.HTTPStatus.CONFLICT, http.HTTPStatus.CONFLICT.name)
    def put(self, **kwargs):
        if current_user.is_authenticated:
            return controller.get(**{"user_id": current_user.user_id}), http.HTTPStatus.FOUND
        else:
            if controller.get(**{"username": kwargs.get("username")}):
                return User(), http.HTTPStatus.CONFLICT
            else:
                user = controller.create(kwargs.get("username"), kwargs.get("password"))
                return user, http.HTTPStatus.CREATED

    @blueprint.response(http.HTTPStatus.NO_CONTENT)
    @blueprint.alt_response(http.HTTPStatus.UNAUTHORIZED, http.HTTPStatus.UNAUTHORIZED.name)
    def delete(self) -> (models.User, int):
        if current_user.is_authenticated:
            controller.delete(current_user.user_id)
            return http.HTTPStatus.NO_CONTENT
        else:
            raise UnauthorizedAction()
