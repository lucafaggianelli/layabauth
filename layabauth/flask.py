import logging
import functools
import json

import flask
import werkzeug
from jose import exceptions, jws

from layabauth._http import _get_token, validate, keys


def requires_authentication(jwks_uri: str):
    """
    Ensure that a valid JWT is received before entering the annotated endpoint.

    :param jwks_uri: The JWKs URI as defined in .well-known.
    For more information on JWK, refer to https://tools.ietf.org/html/rfc7517
        * Azure Active Directory: https://sts.windows.net/common/discovery/keys
        * Microsoft Identity Platform: https://sts.windows.net/common/discovery/keys
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*func_args, **func_kwargs):
            try:
                flask.g.token = _get_token(flask.request.headers)
                if not flask.g.token:
                    raise werkzeug.exceptions.Unauthorized()
                key = keys(jwks_uri)
                flask.g.token_body = validate(flask.g.token, key)
            except exceptions.JOSEError as e:
                raise werkzeug.exceptions.Unauthorized(description=str(e)) from e
            return func(*func_args, **func_kwargs)

        return wrapper

    return decorator


def _extract_token_body() -> dict:
    if getattr(flask.g, "token_body", None):
        return flask.g.token_body

    token = _get_token(flask.request.headers)
    if not token:
        return {}

    try:
        return json.loads(jws.get_unverified_claims(token=token))
    except exceptions.JOSEError:
        return {}


class UserIdFilter(logging.Filter):
    """
    This is a logging filter that makes the user identifier available for use in the logging format.
    Note that we are checking if we are in a request context, as we may want to log things before Flask is fully loaded.
    """

    def __init__(self, token_field_name: str, name: str = ""):
        logging.Filter.__init__(self, name=name)
        self.token_field_name = token_field_name

    def filter(self, record):
        record.user_id = (
            _extract_token_body().get(self.token_field_name, "")
            if flask.has_request_context()
            else ""
        )
        return True
