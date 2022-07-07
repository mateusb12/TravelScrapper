import os
from pathlib import Path


def get_main_folder_path() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def get_api_consumer_path() -> Path:
    return Path(get_main_folder_path(), "apis", "api_consumer")


def get_travel_analysis_path() -> Path:
    return get_main_folder_path() / 'travel_analysis'


def get_fillers_path() -> Path:
    return get_main_folder_path() / 'fillers'


def get_main_folder_reference():
    return Path(__file__).parent.parent


def get_airports_reference():
    return get_main_folder_reference() / "airports"


def get_datasets_reference():
    return get_main_folder_reference() / "datasets"


def get_notifications_reference():
    return get_main_folder_reference() / "notifications"


def get_telegram_bot_reference():
    return get_notifications_reference() / "telegram_bot"


def get_queries_reference():
    return get_main_folder_reference() / "queries"


if __name__ == "__main__":
    aux = get_travel_analysis_path()
    print(aux)
