from dataclasses import dataclass

import pandas as pd

from termcolor import colored

from apis.api_consumer.kiwi_api_call import set_kiwi_call
from database.fillers.query_examples import get_rio_example, get_sp_example
from travel_analysis.flight import Flight
from updater.flight_updater import FlightUpdater
from notifications.telegram_bot.bot import telegram_bot_instance


@dataclass
class UpdateFlight:
    kiwi_dict: dict
    tag: str = None
    df: pd.DataFrame = None

    def update_flight_db(self) -> tuple[str, int]:
        self.tag = self.kiwi_dict["query_name"]
        api_data = set_kiwi_call(self.kiwi_dict)
        flight_api_data = api_data['data']
        fu = FlightUpdater(query_tag=self.tag)
        for index, flight_dict in enumerate(flight_api_data, 1):
            current = index
            last = len(flight_api_data)
            ratio = f"{round(100 * current / last, 2)}%"
            log = f"{current}/{last} ({ratio})"
            print(colored(log, "yellow"))
            flight = Flight(flight_dict)
            fu.set_new_flight(flight)
        cheapest = fu.export_new_cheapest()
        if cheapest is not None:
            self.df = fu.df
            full_msg = self.setup_bot_msg(cheapest)
            self.handle_telegram(user_id=405202204, message=full_msg)
        if cheapest is not None:
            return "New cheapest flight found!", 200
        else:
            return "No new cheapest flight found!", 206

    @staticmethod
    def handle_telegram(user_id: int, message: str):
        telegram_bot_instance.send_message(chat_id=user_id, text=message)

    @staticmethod
    def get_avg_price(input_dataset: pd.DataFrame) -> float:
        return input_dataset.price.mean()

    def get_price_diff(self, input_price: float) -> float:
        return 100 * (input_price - self.get_avg_price(self.df)) / input_price

    def setup_bot_msg(self, cheapest_flight: Flight) -> str:
        body = f"New cheapest flight found in {self.tag}!\n"
        date = f"Date: {cheapest_flight.date_departure.replace('-', '/')}\n"
        departure = f"Departure: {cheapest_flight.time_departure}\n"
        arrival = f"Arrival: {cheapest_flight.time_arrival}\n"
        flight_duration = f"Duration: {cheapest_flight.duration}\n"
        avg_price = f"Avg price: £{self.get_avg_price(self.df):.0f}\n"
        price_diff = round(self.get_price_diff(cheapest_flight.price))
        price = f"New price: £{cheapest_flight.price} ({price_diff}%)\n"
        link = f"Link: {cheapest_flight.link}\n"
        return body + date + departure + arrival + flight_duration + avg_price + price + link


def __main():
    ufd = UpdateFlight(kiwi_dict=get_sp_example())
    ufd.update_flight_db()


if __name__ == "__main__":
    __main()
