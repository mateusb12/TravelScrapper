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


# Create update_flight_db as dataclass
@dataclass
class UpdateFlight:
    filename: str
    ratio: int
    kiwi_dict: dict

    def update_flight_db(self) -> None:
        aux = set_kiwi_call(self.kiwi_dict)
        flight_api_data = aux['data']
        shuffle(flight_api_data)
        dataset = load_df(self.filename)
        fu = FlightUpdater(df=dataset)
        size = len(flight_api_data)
        loop = int(0.01 * self.ratio * size)
        for flight_dict in flight_api_data[:loop]:
            flight = Flight(flight_dict)
            fu.set_new_flight(flight)
            fu.append_new_flight()
        fu.save_df()
        print(colored("Done!", "green"))


def __main():
    ufd = UpdateFlight(filename="fortaleza_rio.csv", ratio=100, kiwi_dict=get_rio_example())
    ufd.update_flight_db()


if __name__ == "__main__":
    __main()
