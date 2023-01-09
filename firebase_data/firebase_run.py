import os
import re

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_login import FirebaseLogin

from firebase_data.firebase_user_crud import FirebaseUserCrud
from price_monitor.flight_utils import get_formatted_today_date, reorder_flight_data_node_by_date


class FirebaseApp:
    def __init__(self):
        connection_class = FirebaseCore()
        self.app = connection_class.app
        self.firebase_folder = "flight_data"
        self.db = connection_class.db
        self.auth = connection_class.auth
        user_crud = FirebaseUserCrud(connection_class)
        user_login = FirebaseLogin(user_crud)
        self.user = user_login.user
        self.all_entries: dict = self.get_all_entries()
        self.query_date = get_formatted_today_date()

    def __set_env_credentials(self):
        self.credential_email = os.environ["FIREBASE_DUMMY_LOGIN"]
        self.credential_password = os.environ["FIREBASE_DUMMY_PASSWORD"]

    def add_entry(self, input_dict: dict):
        ref = self.db.reference(self.firebase_folder)
        return ref.push(input_dict)

    def check_existing_flight(self, input_dict: dict) -> bool:
        # sourcery skip: use-any, use-named-expression, use-next
        if not self.all_entries:
            return False
        test_key = list(self.all_entries.keys())[0]
        if bool(re.match(r'^\d{2} \w+ \d{4}$', test_key)):
            self.refresh_all_entries()
        if self.all_entries is None:
            return False
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

    def get_all_entries(self) -> dict:
        ref = self.db.reference(self.firebase_folder)
        return ref.get()

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
        ref = self.db.reference(f'{self.firebase_folder}/{unique_id}')
        ref.delete()
        # self.db.child(f'/{self.firebase_folder}').child(unique_id).remove(token=self.token)

    def update_entry_by_unique_id(self, unique_id: str, new_info: dict):
        ref = self.db.reference(f'{self.firebase_folder}/{unique_id}')
        ref.update(new_info)
        # self.db.child(f'/{self.firebase_folder}').child(unique_id).update(new_info, token=self.token)

    def get_all_firebase_folders(self):
        ref = self.db.reference("/").get()
        collections = dict(ref)
        return list(collections.keys())

    def create_dummy_test_folder(self):
        ref = self.db.reference('tests')
        ref.set({"test_field": "test"})
        # self.db.child('/tests').push("test", token=self.token)

    def delete_all_entries(self):
        all_folders = self.get_all_firebase_folders()
        desired_folder = self.firebase_folder.replace("/", "")
        if desired_folder not in all_folders:
            return
        ref = self.db.reference(self.firebase_folder)
        ref.delete()
        # self.db.child(f'/{self.firebase_folder}').remove(token=self.token)

    def set_firebase_folder(self, new_location: str):
        self.firebase_folder = new_location

    def delete_firebase_folder(self, folder_name: str):
        all_folders = self.get_all_firebase_folders()
        desired_folder = folder_name.replace("/", "")
        if desired_folder not in all_folders:
            return
        ref = self.db.reference(folder_name)
        ref.delete()

    def refresh_all_entries(self):
        self.all_entries = self.get_all_entries()
        return

    def get_entries_by_user_email(self, user_email: str) -> list[dict]:
        all_data = self.db.reference(self.firebase_folder).get()
        user_pot = []
        for date, flights in all_data.items():
            user_pot.extend(
                flight_content
                for unique_id, flight_content in flights.items()
                if flight_content["userEmail"] == user_email
            )
        return user_pot

    def reorder_flight_node_by_query_date_order(self):
        flight_node = self.db.reference("flight_data")
        flight_node_dict = dict(flight_node.get())
        reordered_dict = reorder_flight_data_node_by_date(flight_node_dict)
        flight_node.update(reordered_dict)


def __main():
    fba = FirebaseApp()
    return
    # all_folders = fba.get_all_firebase_folders()
    # example = get_flight_data_example()[0]
    # existing = fba.check_existing_flight(example)
    # # fba.delete_all_entries()
    # # fba.get_entry("flight_data")
    # return


if __name__ == "__main__":
    __main()
