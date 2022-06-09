import random

import pandas as pd

from fillers.filler_generator import FillerGenerator


def create_random_flight() -> pd.Series:
    random_cities = ['Berlin', 'London', 'Paris', 'Madrid', 'Rome', 'Vienna', 'Zurich', 'Amsterdam', 'Brussels',
                     'Copenhagen', 'Helsinki', 'Lisbon', 'Luxembourg', 'Madrid', 'Oslo', 'Stockholm', 'Warsaw',
                     'Zagreb', 'Athens', 'Bucharest', 'Cairo', 'Hamburg', 'Istanbul', 'Ljubljana', 'Moscow',
                     'Prague', 'Sofia', 'Stockholm', 'Vienna', 'Warsaw']
    fg = FillerGenerator(random.choice(random_cities), random.choice(random_cities))
    return fg.export_to_series()


def generate_filler_df(size: int = 10) -> pd.DataFrame:
    df_list = [create_random_flight() for _ in range(size)]
    return pd.DataFrame(df_list)


def dataset_updater(input_df: pd.DataFrame):
    """ Get an existing dataframe and add new flights to it"""
    df = input_df.copy()
    df = df.append(create_random_flight(), ignore_index=True)
    return df
