import json
from pathlib import Path

import pytest

from price_monitor.flight_processor import FlightProcessor
from references.paths import get_price_monitor_reference


@pytest.fixture(scope="module")
def get_flight_data():
    flight_json_path = Path(get_price_monitor_reference(), "tests", "flight_data.json")
    with open(flight_json_path, "r") as flight_json_file:
        flight_data = json.load(flight_json_file)
    return flight_data


def test_flight_processor_initializes_raw_data_attribute(get_flight_data):
    flight_data = get_flight_data
    flight_processor_instance = FlightProcessor(flight_data)
    assert flight_processor_instance.raw_data == flight_data


def test_flight_processor_initializes_flight_amount_attribute(get_flight_data):
    flight_data = get_flight_data
    flight_processor_instance = FlightProcessor(flight_data)
    assert flight_processor_instance.flight_amount == 5


def test_flight_processor_sets_data_attribute_correctly(get_flight_data):
    # Test when raw_data is a dictionary
    flight_data = get_flight_data
    flight_processor_instance = FlightProcessor(flight_data)
    assert flight_processor_instance.data == flight_data["data"]

    # Test when raw_data is a list
    flight_data_list = flight_data["data"]
    flight_processor_instance = FlightProcessor(flight_data_list)
    assert flight_processor_instance.data == flight_data_list


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
