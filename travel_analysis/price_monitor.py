import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from termcolor import colored
from random import shuffle

from api_consumer.kiwi_api_call import kiwi_call_example, set_kiwi_call
from datasets.empy_df_creator import create_empty_df
from references.paths import get_datasets_reference
from travel_analysis.flight import Flight
from updater.flight_updater import FlightUpdater
from notifications.telegram_bot.bot import telegram_bot_instance

from datetime import datetime


def load_df(df_filename: str) -> pd.DataFrame:
    dataset_ref = get_datasets_reference()
    df_ref = Path(dataset_ref / df_filename)
    if not df_ref.exists():
        create_empty_df(df_ref)
    output_df = pd.read_csv(df_ref)
    output_df.filename = df_filename
    return output_df


def get_rio_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "RIO", "date_from": "01/10/2022", "date_to": "12/12/2022", "limit": 500}


def get_sp_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "RIO", "date_from": "30/07/2022", "date_to": "12/12/2022", "limit": 500}


@dataclass
class UpdateFlight:
    filename: str
    kiwi_dict: dict
    dataset: pd.DataFrame = None

    def update_flight_db(self) -> None:
        aux = set_kiwi_call(self.kiwi_dict)
        flight_api_data = aux['data']
        shuffle(flight_api_data)
        self.dataset = load_df(self.filename)
        fu = FlightUpdater(df=self.dataset)
        for flight_dict in flight_api_data:
            flight = Flight(flight_dict)
            fu.set_new_flight(flight)
            fu.append_new_flight()
        cheapest = fu.get_new_cheapest()
        if cheapest is not None:
            full_msg = self.setup_bot_msg(cheapest)
            self.handle_telegram(user_id=405202204, message=full_msg)
        fu.save_df()
        if cheapest is not None:
            print(colored("Done!", "green"))
        else:
            print(colored("No new cheapest flights found!", "red"))

    @staticmethod
    def handle_telegram(user_id: int, message: str):
        telegram_bot_instance.send_message(chat_id=user_id, text=message)

    def get_avg_price(self) -> float:
        return self.dataset.price.mean()

    def get_price_diff(self, input_price: float) -> float:
        return 100 * (input_price - self.get_avg_price()) / input_price

    def setup_bot_msg(self, cheapest_flight: Flight) -> str:
        body = f"New cheapest flight found in {self.filename}!\n"
        date = f"Date: {cheapest_flight.date_departure.replace('-', '/')}\n"
        departure = f"Departure: {cheapest_flight.time_departure}\n"
        arrival = f"Arrival: {cheapest_flight.time_arrival}\n"
        flight_duration = f"Duration: {cheapest_flight.duration}\n"
        avg_price = f"Avg price: £{self.get_avg_price():.0f}\n"
        price_diff = round(self.get_price_diff(cheapest_flight.price))
        price = f"New price: £{cheapest_flight.price} ({price_diff}%)\n"
        link = f"Link: {cheapest_flight.link}\n"
        return body + date + departure + arrival + flight_duration + avg_price + price + link


def __main():
    ufd = UpdateFlight(filename="fortaleza_rio.csv", kiwi_dict=get_rio_example())
    ufd.update_flight_db()


if __name__ == "__main__":
    __main()
