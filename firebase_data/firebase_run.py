import json
import os
import urllib
import webbrowser

import pyrebase

from references.paths import get_service_account_json_reference
from tokens.token_loader import check_env_variable, load_all_tokens
from firebase_admin import credentials, auth, initialize_app


class FirebaseApp:
    def __init__(self):
        aux = check_env_variable("FIREBASE_API_KEY")
        with open(get_service_account_json_reference(), "r") as f:
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
        self.token = self.user["idToken"]
        self.all_entries = self.get_all_flights().val()

    def __authenticate_using_email_and_password(self) -> dict:
        email = "user@example.com"
        password = "123456789"
        return self.auth.sign_in_with_email_and_password(email, password)

    def add_entry(self, input_dict: dict):
        self.db.child('/flight_data').push(input_dict, token=self.token)

    def check_existing_flight(self, input_dict: dict) -> bool:  # sourcery skip: use-any, use-next
        for unique_id, content in self.all_entries.items():
            if content == input_dict:
                return True
        return False

    def check_existing_unique_id(self, unique_id: str) -> bool:
        return unique_id in self.all_entries

    def get_all_flights(self):
        return self.db.child('/flight_data').get(token=self.token)

    def get_entry_by_key(self, desired_key: str) -> dict:  # sourcery skip: use-next
        for unique_id, content in self.all_entries.items():
            for key, value in content.items():
                if key == desired_key:
                    return value
        return {}

    def get_entry_by_unique_id(self, unique_id: str) -> dict:
        return self.all_entries[unique_id]

    def delete_entry_by_unique_id(self, unique_id: str):
        self.db.child('/flight_data').child(unique_id).remove(token=self.token)


def __main():
    fba = FirebaseApp()
    data = get_flight_data_example()
    single_data = data[0]
    fba.add_entry(single_data)
    # fba.get_entry("flight_data")
    return


if __name__ == "__main__":
    __main()
