from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_run import FirebaseApp
from price_monitor.flight_utils import get_formatted_today_date


class FirebaseQueryCrud:
    def __init__(self, input_app: FirebaseApp):
        self.app = input_app
        self.app.firebase_folder = "query_data"
        self.user = input_app.user
        self.query_date = get_formatted_today_date()

    def create_query(self, query_params: dict):
        base_dict = {"userEmail": self.user.email, "queryDate": self.query_date, **query_params}
        self.app.add_entry(base_dict)
        return {"output": "success", "outputDetails": "Query created"}


def __get_query_example():
    return {"departureAirport": "FOR", "arrivalAirport": "CDG", "departureDate": "02 March 2022", "returnDate": None}


def __main():
    firebase_app = FirebaseApp()
    fqc = FirebaseQueryCrud(firebase_app)
    fqc.create_query(__get_query_example())
    return


if __name__ == "__main__":
    __main()
