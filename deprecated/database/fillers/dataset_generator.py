import random

import pandas as pd

from deprecated.database.fillers.filler_generator import FillerGenerator


def create_random_flight() -> pd.Series:
    random_cities = ['Berlin', 'London', 'Paris', 'Madrid', 'Rome', 'Vienna', 'Zurich', 'Amsterdam', 'Brussels',
                     'Copenhagen', 'Helsinki', 'Lisbon', 'Luxembourg', 'Madrid', 'Oslo', 'Stockholm', 'Warsaw',
                     'Zagreb', 'Athens', 'Bucharest', 'Cairo', 'Hamburg', 'Istanbul', 'Ljubljana', 'Moscow',
                     'Prague', 'Sofia', 'Stockholm', 'Vienna', 'Warsaw']
    fg = FillerGenerator(random.choice(random_cities), random.choice(random_cities))
    return fg.export_to_series()


def generate_filler_df(size: int = 10) -> pd.DataFrame:
    df_list = [create_random_flight() for _ in range(size)]
    df = pd.DataFrame(df_list)
    df.drop(df.columns[0], axis=1)
    df = df.assign(id=(df['cityFrom'] + '_' + df['cityTo']).astype('category').cat.codes)
    df.insert(0, "id", df.pop("id"))
    df = df.sort_values(by='id', inplace=False)
    return df


def filler_dataset_updater(input_df: pd.DataFrame):
    """ Get an existing dataframe and add new flights to it"""
    df = input_df.copy()
    df = df.append(create_random_flight(), ignore_index=True)
    return df


def generate_filler_csv(size: int = 10):
    d = generate_filler_df(size)
    d.to_csv(f'{size}.csv', index=False)


def __main():
    generate_filler_csv(1)


if __name__ == "__main__":
    __main()
