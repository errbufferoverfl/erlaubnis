import http.client

import flask
import werkzeug
from flask import jsonify

blueprint = flask.Blueprint('error_handlers', __name__)


class HTTPError(Exception):
    status_code = http.client.INTERNAL_SERVER_ERROR
    description = "Internal Server Error"
    debug_msg = ""

    def __init__(self, debug_msg: str = None, description: str = None, status_code: int = None):
        Exception.__init__(self)
        if flask.app.get_debug_flag():
            self.debug_msg = debug_msg

        if description is not None:
            self.description = description

        if status_code is not None:
            self.status_code = status_code

    def to_json(self):
        if self.debug_msg:
            response_body = {
                "code": self.status_code,
                "description": self.description,
                "debug": self.debug_msg,
            }
        else:
            response_body = {
                "code": self.status_code,
                "description": self.description,
            }
        return jsonify(response_body)


class UserLookupUnauthorized(HTTPError):
    """
    The client request has not been completed because it lacks valid authentication credentials for the requested
    resource.

    Similar to 403 Forbidden, except Unauthorized implies user authentication can allow access to the resource.
    """
    status_code = http.client.UNAUTHORIZED
    description = "Unauthorized user lookup."


class UserInputError(HTTPError):
    """
    The server understands the content type of the request entity, and the syntax of the request entity is correct,
    but it was unable to process the contained instructions.
    """
    status_code = http.client.UNPROCESSABLE_ENTITY
    description = "Unable to process provided user supplied information."


class UserAlreadyExists(HTTPError):
    """
    Conflict with the current state of the target resource.
    """
    status_code = http.client.CONFLICT
    description = "Username already exists. Select another and try again."


class UnauthorizedAction(HTTPError):
    status_code = http.client.UNAUTHORIZED
    description = "Unauthorized"


class InvalidURI(HTTPError):
    """
    The HyperText Transfer Protocol (HTTP) 422 Unprocessable Content response status code indicates that the server
    understands the content type of the request entity, and the syntax of the request entity is correct, but it was
    unable to process the contained instructions.
    """
    status_code = http.client.UNPROCESSABLE_ENTITY
    description = "Invalid URI as defined by RFC 3986#Section 4.3."


@blueprint.app_errorhandler(HTTPError)
def internal_server_error(error: HTTPError) -> werkzeug.Response:
    response = error.to_json()
    response.status_code = error.status_code
    response.content_type = "application/json"

    return response
