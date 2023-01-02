import json
import os

import firebase_admin
from firebase_admin import credentials

from references.paths import get_service_account_json_reference
from tokens.token_loader import check_env_variable
from firebase_admin import auth, db


def create_firebase_connection() -> firebase_admin.App:
    aux = check_env_variable("FIREBASE_API_KEY")
    with open(get_service_account_json_reference(), "r") as f:
        service_account_key = json.load(f)
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


class FirebaseCore:
    def __init__(self):
        self.app: firebase_admin.App = create_firebase_connection()
        self.auth = firebase_admin.auth
        self.db = firebase_admin.db


def __main():
    fc = FirebaseCore()
    return


if __name__ == "__main__":
    __main()
