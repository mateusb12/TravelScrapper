import json
import os
import urllib
import webbrowser

import pyrebase

from tokens.token_loader import check_env_variable, load_all_tokens
from firebase_admin import credentials, auth, initialize_app


class FirebaseApp:
    def __init__(self):
        aux = check_env_variable("FIREBASE_API_KEY")
        with open("service_account_key.json", "r") as f:
            service_account_key = json.load(f)
        config = {
            "apiKey": os.environ["FIREBASE_API_KEY"],
            "authDomain": os.environ["FIREBASE_AUTH_DOMAIN"],
            "projectId": os.environ["FIREBASE_PROJECT_ID"],
            "storageBucket": os.environ["FIREBASE_STORAGE_BUCKET"],
            "messagingSenderId": os.environ["FIREBASE_MESSAGING_SENDER_ID"],
            "appId": os.environ["FIREBASE_APP_ID"],
            "measurementId": os.environ["FIREBASE_MEASUREMENT_ID"],
            "databaseURL": os.environ["FIREBASE_DATABASE_URL"],
            "credential": service_account_key
        }
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.auth = firebase.auth()
        self.user = self.__authenticate_using_email_and_password()

    def __authenticate_using_email_and_password(self) -> dict:
        email = "user@example.com"
        password = "123456789"
        return self.auth.sign_in_with_email_and_password(email, password)

    def add_entry(self, input_dict: dict):
        token = self.user["idToken"]
        self.db.child('/random_data').set({'key': 'value'}, token=token)


def __main():
    fba = FirebaseApp()
    fba.add_entry({"key1": "value1", "key2": "value2"})
    return


if __name__ == "__main__":
    __main()
