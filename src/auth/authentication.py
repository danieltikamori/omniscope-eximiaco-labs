import globals

from dash_cognito_auth import CognitoOAuth
from settings import auth_settings
from werkzeug.middleware.proxy_fix import ProxyFix


def run():

    if auth_settings["behind_proxy"]:
        globals.app.server.wsgi_app = ProxyFix(
            globals.app.server.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
        )

    globals.app.server.config["COGNITO_OAUTH_CLIENT_ID"] = auth_settings["client_id"]
    globals.app.server.config["COGNITO_OAUTH_CLIENT_SECRET"] = auth_settings["client_secret"]
    globals.app.server.secret_key = auth_settings["client_secret"]

    CognitoOAuth(
        globals.app,
        domain=auth_settings["domain"],
        region=auth_settings["region"],
        logout_url="logout",
        user_info_to_session_attr_mapping={
            "email": "email",
            "name": "name"
        }
    )
