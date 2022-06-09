import os
from pathlib import Path


def get_main_folder_path() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def get_api_consumer_path() -> Path:
    return get_main_folder_path() / 'api_consumer'


def get_travel_analysis_path() -> Path:
    return get_main_folder_path() / 'travel_analysis'


def get_fillers_path() -> Path:
    return get_main_folder_path() / 'fillers'


if __name__ == "__main__":
    aux = get_travel_analysis_path()
    print(aux)
