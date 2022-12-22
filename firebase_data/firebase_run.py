import json
import os
import re
import urllib
import webbrowser

import pyrebase

from references.paths import get_service_account_json_reference
from tokens.token_loader import check_env_variable, load_all_tokens
from firebase_admin import credentials, auth, initialize_app

from wrapper.flight_utils import get_formatted_today_date


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
        self.firebase_folder = "flight_data"
        self.db = firebase.database()
        self.auth = firebase.auth()
        self.user = self.__authenticate_using_email_and_password()
        self.token = self.user["idToken"]
        self.all_entries = self.get_all_flights().val()

    def __authenticate_using_email_and_password(self) -> dict:
        email = os.environ["FIREBASE_DUMMY_LOGIN"]
        password = os.environ["FIREBASE_DUMMY_PASSWORD"]
        return self.auth.sign_in_with_email_and_password(email, password)

    def add_entry(self, input_dict: dict):
        self.db.child(f'/{self.firebase_folder}').push(input_dict, token=self.token)

    def check_existing_flight(self, input_dict: dict) -> bool:
        # sourcery skip: use-any, use-named-expression, use-next
        if not self.all_entries:
            return False
        test_key = list(self.all_entries.keys())[0]
        if bool(re.match(r'^\d{2} \w+ \d{4}$', test_key)):
            self.refresh_all_entries()
        all_flights = list(self.all_entries.values())
        for flight in all_flights:
            same_flights = self.are_two_flights_the_same(flight, input_dict)
            if same_flights:
                return True
        return False

    @staticmethod
    def are_two_flights_the_same(flight_a: dict, flight_b: dict) -> bool:
        price_a = int(flight_a["price"])
        price_b = int(flight_b["price"])
        price_check = price_a == price_b
        departure_check = flight_a["departureFormattedDateAndTime"] == flight_b["departureFormattedDateAndTime"]
        arrival_check = flight_a["arrivalFormattedDateAndTime"] == flight_b["arrivalFormattedDateAndTime"]
        return price_check and departure_check and arrival_check

    def check_existing_unique_id(self, unique_id: str) -> bool:
        # sourcery skip: assign-if-exp, reintroduce-else
        if self.all_entries is None:
            return False
        return unique_id in self.all_entries

    def get_all_flights(self):
        return self.db.child(f'/{self.firebase_folder}').get(token=self.token)

    def get_entry_by_key(self, desired_key: str) -> dict:  # sourcery skip: use-next
        for unique_id, content in self.all_entries.items():
            for key, value in content.items():
                if key == desired_key:
                    return value
        return {}

    def get_entry_by_unique_id(self, unique_id: str) -> dict:
        return self.all_entries[unique_id]

    def get_unique_id_by_entry(self, entry: dict) -> str:
        # sourcery skip: use-next
        for unique_id, content in self.all_entries.items():
            different_values = [item for item in content.items() if item not in entry.items()]
            if not different_values:
                return unique_id
        return ""

    def delete_entry_by_unique_id(self, unique_id: str):
        self.db.child(f'/{self.firebase_folder}').child(unique_id).remove(token=self.token)

    def update_entry_by_unique_id(self, unique_id: str, new_info: dict):
        self.db.child(f'/{self.firebase_folder}').child(unique_id).update(new_info, token=self.token)

    def get_all_firebase_folders(self):
        try:
            return self.db.child("/").get(token=self.token).val().keys()
        except AttributeError:
            self.create_dummy_test_folder()
            return self.db.child("/").get(token=self.token).val().keys()

    def create_dummy_test_folder(self):
        self.db.child('/tests').push("test", token=self.token)

    def delete_all_entries(self):
        all_folders = self.get_all_firebase_folders()
        desired_folder = self.firebase_folder.replace("/", "")
        if desired_folder not in all_folders:
            return
        self.db.child(f'/{self.firebase_folder}').remove(token=self.token)

    def set_firebase_folder(self, new_location: str):
        self.firebase_folder = new_location

    def delete_firebase_folder(self, folder_name: str):
        all_folders = self.get_all_firebase_folders()
        desired_folder = folder_name.replace("/", "")
        if desired_folder not in all_folders:
            return
        self.db.child(f'/{folder_name}').remove(token=self.token)

    def refresh_all_entries(self):
        self.all_entries = self.get_all_flights().val()


def __main():
    fba = FirebaseApp()
    # fba.delete_all_entries()
    # fba.get_entry("flight_data")
    return


if __name__ == "__main__":
    __main()
