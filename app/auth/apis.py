import http.client

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from app.auth.enum import ResponseType
from app.core.exceptions import HTTPError

blueprint = Blueprint("auth", "auth", url_prefix="/api", description="OAuth2 authorization endpoints")


@blueprint.route("/authorize")
class Authorization(MethodView):

    @blueprint.response(http.HTTPStatus.OK)
    @blueprint.alt_response(http.HTTPStatus.UNPROCESSABLE_ENTITY, http.HTTPStatus.UNPROCESSABLE_ENTITY.name)
    def get(self):
        """
        3.1.  Authorization Endpoint

        The authorization endpoint is used to interact with the resource
        owner and obtain an authorization grant.  The authorization server
        MUST first verify the identity of the resource owner.  The way in
        which the authorization server authenticates the resource owner
        (e.g., username and password login, session cookies) is beyond the
        scope of this specification.

        The means through which the client obtains the location of the
        authorization endpoint are beyond the scope of this specification,
        but the location is typically provided in the service documentation.

        The endpoint URI MAY include an "application/x-www-form-urlencoded"
        formatted (per Appendix B) query component ([RFC3986] Section 3.4),
        which MUST be retained when adding additional query parameters.  The
        endpoint URI MUST NOT include a fragment component.

        Since requests to the authorization endpoint result in user
        authentication and the transmission of clear-text credentials (in the
        HTTP response), the authorization server MUST require the use of TLS
        as described in Section 1.6 when sending requests to the
        authorization endpoint.

        The authorization server MUST support the use of the HTTP "GET"
        method [RFC2616] for the authorization endpoint and MAY support the
        use of the "POST" method as well.

        Parameters sent without a value MUST be treated as if they were
        omitted from the request.  The authorization server MUST ignore
        unrecognized request parameters.  Request and response parameters
        MUST NOT be included more than once.
        """

        # here we will check how the request has been sent, let's assume though it's in the URL
        response_type = request.args.get("response_type")
        client_id = request.args.get("client_id")
        redirect_url = request.args.get("redirect_url")

        if len(response_type) > 1:
            raise HTTPError(f"Request parameter 'response_type' included multiple times",
                            "too_many_parameters",
                            http.client.UNPROCESSABLE_ENTITY)

        if not response_type:
            raise HTTPError(f"Request parameter 'response_type' not provided",
                            "mandatory_parameter_missing",
                            http.client.UNPROCESSABLE_ENTITY)

        """
        If an authorization request is missing the "response_type" parameter,
        or if the response type is not understood, the authorization server
        MUST return an error response as described in Section 4.1.2.1.
        """
        if response_type.lower() == ResponseType.TOKEN:
            pass
        elif response_type.lower() == ResponseType.CODE:
            pass
        else:
            raise HTTPError(f"unsupported_response_type: '{response_type}'",
                            "unsupported_response_type",
                            http.client.UNPROCESSABLE_ENTITY)

        if len(client_id) > 1:
            raise HTTPError(f"Request parameter 'client_id' included multiple times",
                            "too_many_parameters",
                            http.client.UNPROCESSABLE_ENTITY)

        if not client_id:
            raise HTTPError(f"Request parameter 'client_id' not provided",
                            "mandatory_parameter_missing",
                            http.client.UNPROCESSABLE_ENTITY)

        if len(redirect_url) > 1:
            raise HTTPError(f"Request parameter 'redirect_url' included multiple times",
                            "too_many_parameters",
                            http.client.UNPROCESSABLE_ENTITY)

        if not redirect_url:
            raise HTTPError(f"Request parameter 'redirect_url' not provided",
                            "mandatory_parameter_missing",
                            http.client.UNPROCESSABLE_ENTITY)
