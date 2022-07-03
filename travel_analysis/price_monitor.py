import time
from pathlib import Path

import pandas as pd
from termcolor import colored
from random import shuffle

from api_consumer.kiwi_api_call import kiwi_call_example
from datasets.empy_df_creator import create_empty_df
from references.reference import get_datasets_reference
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


def update_flight_db(filename: str, ratio: int = 100) -> None:
    aux = kiwi_call_example()
    flight_api_data = aux['data']
    shuffle(flight_api_data)
    dataset = load_df(filename)
    fu = FlightUpdater(df=dataset)
    size = len(flight_api_data)
    loop = int(0.01 * ratio * size)
    for flight_dict in flight_api_data[:loop]:
        flight = Flight(flight_dict)
        fu.set_new_flight(flight)
        fu.append_new_flight()
    fu.save_df()


def __main():
    update_flight_db("fortaleza_rio.csv")


if __name__ == "__main__":
    __main()
