import random

import pandas as pd

from fillers.filler_generator import FillerGenerator


def generate_filler_df(size: int = 10) -> pd.DataFrame:
    random_cities = ['Berlin', 'London', 'Paris', 'Madrid', 'Rome', 'Vienna', 'Zurich', 'Amsterdam', 'Brussels',
                     'Copenhagen', 'Helsinki', 'Lisbon', 'Luxembourg', 'Madrid', 'Oslo', 'Stockholm', 'Warsaw',
                     'Zagreb', 'Athens', 'Bucharest', 'Cairo', 'Hamburg', 'Istanbul', 'Ljubljana', 'Moscow',
                     'Prague', 'Sofia', 'Stockholm', 'Vienna', 'Warsaw']
    df_list = []
    for _ in range(size):
        fg = FillerGenerator(random.choice(random_cities), random.choice(random_cities))
        df_list.append(fg.export_to_series())
    return pd.DataFrame(df_list)