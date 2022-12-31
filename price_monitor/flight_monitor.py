from apis.api_consumer.kiwi_api_call import kiwi_call
from firebase_data.firebase_crud import FirebaseCrud
from notifications.telegram_bot.bot import telegram_bot_instance
from random_generated_flights.random_data_generator import get_10_random_flights
from price_monitor.flight_processor import FlightProcessor
from price_monitor.flight_utils import get_formatted_today_date


class FlightMonitor:
    def __init__(self):
        self.crud = FirebaseCrud()
        today_date = get_formatted_today_date()
        self.crud.set_folder(f"flight_data/{today_date}")
        self.existing_flight_data = [{}]
        self.new_flight_data = [{}]
        self.__run()

    def __run(self):
        self.__gather_current_data()
        self.__collect_new_data()
        self.__analyze_new_data()

    def __clean_folder(self):
        self.crud.delete_folder("flight_data")

    def __gather_current_data(self):
        raw_data = self.crud.firebase_app.get_all_flights()
        if raw_data is None:
            self.existing_flight_data = []
            return
        self.existing_flight_data = list(raw_data.values())
        return

    def __collect_new_data(self):
        kiwi_api_call = kiwi_call(fly_from="FOR", fly_to="RIO", date_from="01/01/2023",
                                  date_to="01/03/2023", limit=500)
        trimmed_data = self.__trim_kiwi_data(kiwi_api_call["data"])
        flight_processor_instance = FlightProcessor(trimmed_data)
        raw_flights = flight_processor_instance.flights
        self.new_flight_data = sorted(raw_flights, key=lambda x: x["duration"]["total"])

    @staticmethod
    def __trim_kiwi_data(kiwi_flights: list[dict]) -> list[dict]:
        lowest_price_value = min(flight["price"] for flight in kiwi_flights)
        return [flight for flight in kiwi_flights if flight["price"] == lowest_price_value]

    def __get_current_lowest_price(self):
        all_flights_call = self.crud.read_all_flights()
        if all_flights_call is None:
            return float("inf")
        all_flights_dict = all_flights_call
        all_flights_list = list(all_flights_dict.values())
        all_flights_ordered_list = sorted(all_flights_list, key=lambda flight: flight["price"])
        return all_flights_ordered_list[0]["price"]

    def __analyze_new_data(self):
        lowest_firebase_price = self.__get_current_lowest_price()
        lowest_kiwi_price = self.new_flight_data[0]["price"]
        if lowest_firebase_price == float("inf"):
            self.crud.create_flight(self.new_flight_data[0])
            return
        price_diff = round(100 * (lowest_kiwi_price - lowest_firebase_price) / lowest_firebase_price, 2)
        if price_diff <= -10:
            flight_link = self.new_flight_data[0]["link"]
            price_diff_tag = f"{price_diff}% cheaper"
            full_message = f"New flight found! {price_diff_tag} \n {flight_link}"
            telegram_bot_instance.send_message(chat_id=405202204, text=full_message)
        self.__insert_new_data(self.new_flight_data)

    def __insert_new_data(self, flight_pot: list[dict]):
        # available_flights = self.crud.trim_non_existing_flights(flight_pot)
        for flight in flight_pot:
            self.crud.create_flight(flight)


def __main():
    fw = FlightMonitor()
    return


if __name__ == "__main__":
    __main()
