from firebase_data.firebase_run import FirebaseApp


class FirebaseCrud:
    def __init__(self):
        self.firebase = FirebaseApp()

    def create_flight(self, flight_data: dict):
        self.firebase.add_entry(flight_data)

    def read_flight(self, flight_unique_id: str) -> dict:
        return self.firebase.get_entry_by_unique_id(flight_unique_id)

    def update_flight(self, flight_unique_id: str, new_flight_data: dict):
        current_flight = self.firebase.get_entry_by_unique_id(flight_unique_id)
        for key, value in new_flight_data.items():
            current_flight[key] = value
        self.firebase.db.child('/flight_data').child(flight_unique_id).set(
            current_flight, token=self.firebase.token)

    def delete_flight(self, flight_unique_id: str):
        self.firebase.delete_entry_by_unique_id(flight_unique_id)


def __main():
    fbc = FirebaseCrud()
    fbc.update_flight(flight_unique_id="-NJjiRqwX8-qlOPRy-Iv", new_flight_data={"arrivalAirport": "GIH"})


if __name__ == '__main__':
    __main()
