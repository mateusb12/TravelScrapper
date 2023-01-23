from typing import List

from firebase_data.firebase_run import FirebaseApp, are_two_flights_the_same
from price_monitor.flight_processor import get_flight_data_example
from price_monitor.flight_utils import get_formatted_today_date


class FirebaseFlightCrud:
    def __init__(self, input_app: FirebaseApp):
        self.folder = "flight_data"
        self.firebase_app = input_app
        self.firebase_app.query_date = get_formatted_today_date()
        self.existing_flights = self.__get_existing_flights()

    def create_flight(self, flight_data: dict) -> dict:
        # sourcery skip: use-named-expression
        existing_flight = self.__check_existing_flight(flight_data)
        if existing_flight:
            return {"output": "error", "outputDetails": "Flight already exists"}
        query_date = get_formatted_today_date()
        flight_data["queryDate"] = query_date
        flight_data["userEmail"] = self.firebase_app.user.email
        del flight_data["duration"]
        base_folder = self.firebase_app.main_firebase_folder
        new_firebase_folder = f"{self.firebase_app.firebase_folder}/{self.firebase_app.query_date}"
        self.firebase_app.set_firebase_folder(new_firebase_folder)
        self.firebase_app.add_entry(flight_data)
        self.firebase_app.set_firebase_folder(base_folder)
        self.refresh_entries()
        return {"output": "success", "outputDetails": "Flight created"}

    def read_flight(self, flight_unique_id: str) -> dict:
        # sourcery skip: use-named-expression
        existing_flight = self.firebase_app.check_existing_unique_id(flight_unique_id)
        return (
            (self.firebase_app.get_entry_by_unique_id(flight_unique_id))
            if existing_flight
            else {"output": "error", "outputDetails": "Flight already exists"}
        )

    def update_flight(self, flight_unique_id: str, new_flight_data: dict) -> dict:
        if not self.firebase_app.check_existing_unique_id(flight_unique_id):
            return {"output": "error", "outputDetails": f"Could not update [{flight_unique_id}]. Flight not found"}
        current_flight = self.firebase_app.get_entry_by_unique_id(flight_unique_id)
        for key, value in new_flight_data.items():
            current_flight[key] = value
        self.firebase_app.update_entry_by_unique_id(flight_unique_id, current_flight)
        self.refresh_entries()
        return {"output": "success", "outputDetails": "Flight updated"}

    def delete_flight(self, flight_unique_id: str) -> dict:
        if not self.firebase_app.check_existing_unique_id(flight_unique_id):
            return {"output": "error", "outputDetails": f"Could not delete [{flight_unique_id}]. Flight not found"}
        self.firebase_app.delete_entry_by_unique_id(flight_unique_id)
        self.refresh_entries()
        return {"output": "success", "outputDetails": "Flight deleted"}

    def delete_folder(self, folder_name: str):
        self.firebase_app.delete_firebase_folder(folder_name)

    def refresh_entries(self):
        self.firebase_app.refresh_all_entries()

    def set_folder(self, folder_name: str):
        self.firebase_app.set_firebase_folder(folder_name)

    def read_all_flights(self):
        self.firebase_app.firebase_folder = self.folder
        raw_flights = self.firebase_app.get_all_entries()
        for key, value in raw_flights.items():
            for key2, value2 in value.items():
                value2["uniqueId"] = key2
        return raw_flights

    def trim_non_existing_flights(self, flight_pot: List[dict]):
        return [item for item in flight_pot if not self.firebase_app.check_existing_flight(item)]

    def get_flights_by_user_email(self, user_email: str):
        return self.firebase_app.get_entries_by_user_email(user_email)

    def __get_existing_flights(self):
        nested_flights = list(self.firebase_app.all_entries.values())
        return [x for sublist in nested_flights for x in sublist.values()]

    def __check_existing_flight(self, new_flight: dict):
        # sourcery skip: use-any, use-next
        for flight in self.existing_flights:
            if are_two_flights_the_same(flight, new_flight):
                return True
        return False


def __main():
    firebase_app = FirebaseApp()
    fbc = FirebaseFlightCrud(firebase_app)
    fbc.firebase_app.set_firebase_folder("flight_data")
    aux = fbc.read_all_flights()
    return
    # flight_data = get_flight_data_example()
    # single_flight = flight_data[0]
    # fbc.create_flight(single_flight)
    # fbc.update_flight(flight_unique_id="-NJjiRqwX8-qlOPRy-Iv", new_flight_data={"arrivalAirport": "GIH"})


if __name__ == '__main__':
    __main()
