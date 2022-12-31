import pytest

from firebase_data.firebase_flight_crud import FirebaseFlightCrud
from price_monitor.flight_processor import get_flight_data_example


@pytest.fixture(scope="module")
def get_flight_data():
    data = get_flight_data_example()
    return data[0]


@pytest.fixture(scope="module")
def get_firebase_crud_instance():
    instance = FirebaseFlightCrud()
    instance.firebase_app.set_firebase_folder("tests")
    instance.delete_folder(folder_name="/tests")
    return instance


@pytest.mark.run(order=1)
def test_firebase_create_flight(get_flight_data, get_firebase_crud_instance):
    # sourcery skip: use-next
    """This test creates a flight using the create_flight method, and then uses the read_flight method to retrieve
     the flight and verify that it was created correctly."""
    flight_data = get_flight_data
    firebase_crud = get_firebase_crud_instance

    creation_result = firebase_crud.create_flight(flight_data)
    all_flights = firebase_crud.firebase_app.get_all_flights()
    created_flight = list(all_flights.values())[0]
    different_values = [item for item in created_flight.values() if item not in flight_data.values()]
    assert creation_result["output"] == "success"
    assert not different_values


@pytest.mark.run(order=2)
def test_firebase_read_flight(get_flight_data, get_firebase_crud_instance):
    """This test uses the read_flight method to retrieve the flight and verify that the returned data
     matches the data that was originally used to create the flight."""
    flight_data = get_flight_data
    firebase_crud = get_firebase_crud_instance

    all_flights = firebase_crud.firebase_app.get_all_flights()
    flight_unique_id = list(all_flights.keys())[0]
    read_flight = firebase_crud.read_flight(flight_unique_id)
    assert read_flight == flight_data


@pytest.mark.run(order=3)
def test_firebase_update_flight(get_flight_data, get_firebase_crud_instance):
    """This test uses the update_flight method to update the flight and verify that the update was successful."""
    flight_data = get_flight_data
    firebase_crud = get_firebase_crud_instance

    new_flight_data = {"arrivalAirport": "BER", "departureAirport": "LHR"}
    expected_flight_data = flight_data.copy()
    expected_flight_data.update(new_flight_data)
    all_flights = firebase_crud.firebase_app.get_all_flights()
    flight_unique_id = list(all_flights.keys())[0]
    update_result = firebase_crud.update_flight(flight_unique_id, new_flight_data)
    assert update_result["output"] == "success"

    updated_flight = firebase_crud.read_flight(flight_unique_id)
    different_values = [item for item in updated_flight.values() if item not in expected_flight_data.values()]
    assert not different_values


@pytest.mark.run(order=4)
def test_firebase_delete_flight(get_firebase_crud_instance):
    """This test uses the delete_flight method to delete the flight and verify that the flight was deleted."""
    firebase_crud = get_firebase_crud_instance

    all_flights = firebase_crud.firebase_app.get_all_flights()
    flight_unique_id = list(all_flights.keys())[0]

    delete_result = firebase_crud.delete_flight(flight_unique_id)
    assert delete_result["output"] == "success"

    all_flights = firebase_crud.firebase_app.get_all_flights()
    if all_flights is None:
        all_flights = {"key": "value"}
    assert flight_unique_id not in all_flights.keys()


def test_firebase_read_flight_not_found(get_firebase_crud_instance):
    """This test uses the read_flight method to retrieve a flight that does not exist and verify that
     an error is raised."""
    firebase_crud = get_firebase_crud_instance
    result = firebase_crud.read_flight("abc")
    assert result["output"] == "error"


def test_firebase_update_flight_not_found(get_firebase_crud_instance):
    """This test uses the update_flight method to update a flight that does not exist and verify that
     an error is raised."""
    firebase_crud = get_firebase_crud_instance
    update_result = firebase_crud.update_flight("abc", {"flight": "data"})
    assert update_result["output"] == "error"


def test_firebase_delete_flight_not_found(get_firebase_crud_instance):
    """This test uses the delete_flight method to delete a flight that does not exist and verify that
     an error is raised."""
    firebase_crud = get_firebase_crud_instance
    delete_result = firebase_crud.delete_flight("abc")
    assert delete_result["output"] == "error"


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
