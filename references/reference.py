from pathlib import Path


def get_main_folder_reference():
    return Path(__file__).parent.parent


def get_airports_reference():
    return get_main_folder_reference() / "airports"


def get_datasets_reference():
    return get_main_folder_reference() / "datasets"


if __name__ == "__main__":
    print(get_airports_reference())
