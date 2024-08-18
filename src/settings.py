import os

from dotenv import load_dotenv

load_dotenv()

auth_settings = {
    "domain": os.environ.get("COGNITO_DOMAIN"),
    "region": os.environ.get("AWS_REGION"),
    "secret_key": os.environ.get("SECRET_KEY"),
    "client_id": os.environ.get("COGNITO_OAUTH_CLIENT_ID"),
    "client_secret": os.environ.get("COGNITO_OAUTH_CLIENT_SECRET"),
    "behind_proxy": os.environ.get("BEHIND_PROXY", False)
}

api_settings = {
    "everhour_api_key": os.environ.get("EVERHOUR_API_KEY"),
    "todoist_api_key": os.environ.get("TODOIST_API_KEY"),
    "pipedrive_api_key": os.environ.get("PIPEDRIVE_API_KEY"),
    "wordpress_user": os.environ.get("WORDPRESS_USER"),
    "wordpress_pass": os.environ.get("WORDPRESS_PASS")
}