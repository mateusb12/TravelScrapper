from typing import List

from apis.api_consumer.kiwi_api_call import kiwi_call
from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_flight_crud import FirebaseFlightCrud
from firebase_data.firebase_login import FirebaseLogin
from firebase_data.firebase_query_crud import FirebaseQueryCrud
from firebase_data.firebase_run import FirebaseApp
from firebase_data.firebase_user_crud import FirebaseUserCrud
from notifications.telegram_bot.bot import telegram_bot_instance
from price_monitor.flight_processor import FlightProcessor
from price_monitor.flight_utils import get_formatted_today_date, get_earliest_date, revert_date


class FlightMonitor:
    def __init__(self, app: FirebaseApp):
        self.flight_crud = FirebaseFlightCrud(input_app=app)
        self.query_crud = FirebaseQueryCrud(input_app=app)
        self.today_date = get_formatted_today_date()
        self.flight_crud.set_folder(f"flight_data/{self.today_date}")
        self.current_query = {}
        self.existing_flight_data = [{}]
        self.new_flight_data = [{}]
        self.output = {"cheapest_firebase_flight": 0, "cheapest_kiwi_flight": 0}
        self.query_data = []

    def search_prices(self):
        self._gather_current_firebase_flight_data()
        self._read_all_queries()
        self._process_all_queries()

    def _read_all_queries(self):
        all_queries = self.query_crud.read_all_queries()
        for key, value in all_queries.items():
            value["uniqueId"] = key
            self.query_data.append(value)

    def _process_all_queries(self):
        for query in self.query_data:
            self._process_single_query(query)

    def _process_single_query(self, query_dict: dict):
        self.current_query = query_dict
        self._collect_new_kiwi_data(query_dict)
        self._analyze_new_data()

    def _clean_folder(self):
        self.flight_crud.delete_folder("flight_data")

    def _gather_current_firebase_flight_data(self):
        raw_data = self.flight_crud.read_all_flights()
        if raw_data is None:
            self.existing_flight_data = []
            return
        self.existing_flight_data = list(raw_data.values())
        return

    def _collect_new_kiwi_data(self, kiwi_info: dict):
        departure_airport = kiwi_info["departureAirport"]
        arrival_airport = kiwi_info["arrivalAirport"]
        raw_departure_date = kiwi_info["departureDate"]
        raw_arrival_date = kiwi_info.get("arrivalDate")
        raw_arrival_date = raw_departure_date if raw_arrival_date is None else raw_arrival_date
        raw_departure_date, raw_arrival_date = revert_date(raw_departure_date), revert_date(raw_arrival_date)
        kiwi_api_call = kiwi_call(fly_from=departure_airport, fly_to=arrival_airport, date_from=raw_departure_date,
                                  date_to=raw_arrival_date, limit=100)
        if 'status' in kiwi_api_call and kiwi_api_call["status"] == "Bad Request":
            raise ValueError(f"Kiwi API call failed.\nStatus → {kiwi_api_call['status']}"
                             f"\nMessage → {kiwi_api_call['error']}")
        trimmed_data = self._trim_kiwi_data(kiwi_api_call["data"])
        flight_processor_instance = FlightProcessor(trimmed_data)
        raw_flights = flight_processor_instance.flights
        self.new_flight_data = sorted(raw_flights, key=lambda x: x["duration"]["total"])

    @staticmethod
    def _trim_kiwi_data(kiwi_flights: List[dict]) -> List[dict]:
        lowest_price_value = min(flight["price"] for flight in kiwi_flights)
        return [flight for flight in kiwi_flights if flight["price"] == lowest_price_value]

    def _get_current_lowest_price(self):
        """This function retrieves the lowest price for the flights that matches the current selected query"""
        all_flights_dict = self.flight_crud.read_all_flights()
        flights = [sub_val for key, val in all_flights_dict.items() for sub_key, sub_val in val.items()]
        flights_with_query_id = [flight for flight in flights if "queryId" in flight]
        current_query_flights = [flight for flight in flights_with_query_id if flight["queryId"] ==
                                 self.current_query["uniqueId"]]
        all_flights_dates = list(all_flights_dict.keys())
        earliest_date = get_earliest_date(all_flights_dates)
        all_flights_list = all_flights_dict[earliest_date]
        unique_id_flight_pot = [flight["uniqueId"] for flight in current_query_flights]
        all_relevant_flights = [flight for flight in all_flights_list.values() if flight["uniqueId"] in
                                unique_id_flight_pot]
        cheapest_flight = min(all_relevant_flights, key=lambda x: x['price'])
        return cheapest_flight["price"]

    def _analyze_new_data(self) -> dict:
        """This function compares the new retrieved data to the existing data, updating the firebase accordingly.
        If it ends up finding a new cheapest flight, it will call the handle_new_cheapest_flight function"""
        lowest_firebase_price = self._get_current_lowest_price()
        lowest_kiwi_price = self.new_flight_data[0]["price"]
        self.output["cheapest_firebase_flight"] = lowest_firebase_price
        self.output["cheapest_kiwi_flight"] = lowest_kiwi_price
        if lowest_firebase_price == float("inf"):
            self.flight_crud.create_flight(self.new_flight_data[0])
            return {"output": "failure", "outputDetails": "There was no data in the database."
                                                          " Could not find a cheaper flight"}
        price_diff = round(100 * (lowest_kiwi_price - lowest_firebase_price) / lowest_firebase_price, 2)
        if price_diff <= -10:
            return self.handle_new_cheapest_flight(price_diff, lowest_kiwi_price)
        self._insert_new_data(self.new_flight_data)
        return {"output": "failure", "outputDetails": f"Could not find a cheaper flight than {lowest_firebase_price}"}

    def handle_new_cheapest_flight(self, price_diff, lowest_kiwi_price):
        """This function sends a telegram message to the user"""
        flight_link = self.new_flight_data[0]["link"]
        price_diff_tag = f"{price_diff}% cheaper"
        full_message = f"New flight found! {price_diff_tag} \n {flight_link}"
        print(full_message)
        telegram_bot_instance.send_message(chat_id=405202204, text=full_message)
        self._insert_new_data(self.new_flight_data)
        return {"output": "success", "outputDetails": f"New cheapest flight found for ${lowest_kiwi_price} "
                                                      f"({price_diff_tag} cheaper)"}

    def _insert_new_data(self, flight_pot: List[dict]):
        """This function inserts the new data into the firebase database"""
        for flight in flight_pot:
            flight["queryDetails"] = self.current_query
            flight["queryId"] = self.current_query["uniqueId"]
            self.flight_crud.create_flight(flight)

    def export_query_output(self):
        return self.output


def __main():
    core = FirebaseCore()
    user_crud = FirebaseUserCrud(core)
    firebase_login = FirebaseLogin(user_crud)
    email = "test@test.com"
    password = "123456"
    firebase_login.login(email, password)
    user = firebase_login.user
    app = FirebaseApp(input_user=user, input_core=core)
    fw = FlightMonitor(app)
    fw.search_prices()
    output = fw.output
    return


if __name__ == "__main__":
    __main()
