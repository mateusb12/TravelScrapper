from firebase_admin.auth import UserRecord

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_flight_crud import FirebaseFlightCrud
from firebase_data.firebase_login import FirebaseLogin
from firebase_data.firebase_query_crud import FirebaseQueryCrud
from firebase_data.firebase_run import FirebaseApp
from firebase_data.firebase_user_crud import FirebaseUserCrud


class FirebaseFactory:
    def __init__(self):
        self.core, self.user_crud, self.firebase_login, self.user, self.app = None, None, None, None, None
        self.firebase_query, self.firebase_flights = None, None

    def run(self, email: str, password: str):
        self.core = FirebaseCore()
        self.user_crud = FirebaseUserCrud(self.core)
        self.firebase_login = FirebaseLogin(self.user_crud)
        self.firebase_login.login(email, password)
        self.user = self.firebase_login.user
        self.app = FirebaseApp(input_user=self.user, input_core=self.core)
        self.firebase_query = FirebaseQueryCrud(self.app)
        self.firebase_flights = FirebaseFlightCrud(self.app)
        print("Factory successfully finished!")


def get_dummy_flights():
    return {"01 January 2023": {
        "-NKihnIPT9ZNKSCpSZKn": {"Departure Airport": "FOR", "Arrival Airport": "GRU",
                                 "Departure Date": " 7th February 2023 at 01:05 PM",
                                 "Arrival Date": " 7th February 2023 at 05:05 PM",
                                 "User Email": "test@test.com",
                                 "Flight Duration": "5h40min",
                                 "Layover Durations": ["0 hours 35 min", "1 hour 55 min"],
                                 "Price": "114"},
        "-NKikQDzK0RQktfSzL7M": {"Departure Airport": "FOR", "Arrival Airport": "GRU",
                                 "Departure Date": " 7th February 2023 at 01:05 PM",
                                 "Arrival Date": " 7th February 2023 at 05:05 PM",
                                 "User Email": "test@test.com",
                                 "Flight Duration": "5h40min",
                                 "Layover Durations": ["0 hours 35 min", "1 hour 55 min"],
                                 "Price": "114"},
    }}


def __main():
    factory = FirebaseFactory()
    factory.run("test@test.com", "123456")
    queries = factory.firebase_query.read_all_queries()
    flights = factory.firebase_flights.read_all_flights()
    return


if __name__ == "__main__":
    __main()
