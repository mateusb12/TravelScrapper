from firebase_data.firebase_run import FirebaseApp


class FirebaseCrud:
    def __init__(self):
        self.firebase_app = FirebaseApp()

    def create_flight(self, flight_data: dict) -> dict:
        # sourcery skip: use-named-expression
        existing_flight = self.firebase_app.check_existing_flight(flight_data)
        if existing_flight:
            return {"output": "error", "outputDetails": "Flight already exists"}
        self.firebase_app.add_entry(flight_data)
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


def __main():
    fbc = FirebaseCrud()
    fbc.firebase_app.set_firebase_folder("tests")
    fbc.delete_folder(folder_name="tests")
    # fbc.update_flight(flight_unique_id="-NJjiRqwX8-qlOPRy-Iv", new_flight_data={"arrivalAirport": "GIH"})


if __name__ == '__main__':
    __main()
