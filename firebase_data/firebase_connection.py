import json
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

from references.paths import get_service_account_json_reference
from utils.singleton_pattern import singleton
from firebase_admin import auth, db

load_dotenv()
def load_service_account_key_from_dot_env():
    rawDict = {"type": os.environ["FIREBASE_JSON_TYPE"],
                "project_id": os.environ["FIREBASE_JSON_PROJECT_ID"],
                "private_key_id": os.environ["FIREBASE_JSON_PRIVATE_KEY_ID"],
                "private_key": os.environ["FIREBASE_JSON_PRIVATE_KEY"].replace("\\n", "\n"),
                "client_email": os.environ["FIREBASE_JSON_CLIENT_EMAIL"],
                "client_id": os.environ["FIREBASE_JSON_CLIENT_ID"],
                "auth_uri": os.environ["FIREBASE_JSON_AUTH_URL"],
                "token_uri": os.environ["FIREBASE_JSON_TOKEN_URL"],
                "auth_provider_x509_cert_url": os.environ["FIREBASE_JSON_AUTH_PROVIDER_X509_CERT_URL"],
                "client_x509_cert_url": os.environ["FIREBASE_JSON_CLIENT_X509_CERT_URL"]}
    return rawDict

def load_service_account_key_from_json():
    with open(get_service_account_json_reference(), "r") as f:
        return json.load(f)


def create_firebase_connection() -> firebase_admin.App:
    service_account_key = load_service_account_key_from_dot_env()
    credential = credentials.Certificate(service_account_key)
    config = {
        "apiKey": os.environ["FIREBASE_API_KEY"],
        "authDomain": os.environ["FIREBASE_AUTH_DOMAIN"],
        "projectId": os.environ["FIREBASE_PROJECT_ID"],
        "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
        "messagingSenderId": os.environ["FIREBASE_MESSAGING_SENDER_ID"],
        "appId": os.environ["FIREBASE_APP_ID"],
        "measurementId": os.environ["FIREBASE_MEASUREMENT_ID"],
        "databaseURL": os.environ["FIREBASE_DATABASE_URL"],
        "credential": credential
    }
    return firebase_admin.initialize_app(credential, config)


@singleton
class FirebaseCore:
    def __init__(self):
        self.app: firebase_admin.App = create_firebase_connection()
        self.auth = firebase_admin.auth
        self.db = firebase_admin.db


def __main():
    load_dotenv()
    os_keys = list(os.environ.keys())
    fc = FirebaseCore()
    return


if __name__ == "__main__":
    __main()
