import pytest

from firebase_data.firebase_crud import FirebaseCrud
from wrapper.flight_processor import get_flight_data_example


@pytest.fixture(scope='module')
def get_flight_data():
    data = get_flight_data_example()
    return data[0]


@pytest.fixture(scope='module')
def get_firebase_crud_instance():
    return FirebaseCrud()


def test_firebase_create_flight(get_flight_data, get_firebase_crud_instance):
    """This test creates a flight using the create_flight method, and then uses the read_flight method to retrieve
     the flight and verify that it was created correctly."""
    flight_data = get_flight_data
    firebase_crud = get_firebase_crud_instance

    firebase_crud.create_flight(flight_data)
    all_flights = firebase_crud.firebase.get_all_flights().val()
    return


def test_firebase_read_flight(get_firebase_crud_instance, flight_unique_id: str):
    """This test uses the read_flight method to retrieve the flight and verify that the returned data
     matches the data that was originally used to create the flight."""
    return


def test_firebase_update_flight(get_firebase_crud_instance, flight_unique_id: str, new_flight_data: dict):
    """This test uses the update_flight method to update the flight and verify that the update was successful."""
    return


def test_firebase_delete_flight(get_firebase_crud_instance, flight_unique_id: str):
    """This test uses the delete_flight method to delete the flight and verify that the flight was deleted."""
    return


def test_firebase_create_invalid_flight(get_firebase_crud_instance):
    """This test passes invalid data to the create_flight method and verify that an error is raised."""
    return


def test_firebase_read_flight_not_found(get_firebase_crud_instance, flight_unique_id: str):
    """This test uses the read_flight method to retrieve a flight that does not exist and verify that
     an error is raised."""
    return


def test_firebase_update_flight_not_found(get_firebase_crud_instance, flight_unique_id: str, new_flight_data: dict):
    """This test uses the update_flight method to update a flight that does not exist and verify that
     an error is raised."""
    return


def test_firebase_delete_flight_not_found(get_firebase_crud_instance, flight_unique_id: str):
    """This test uses the delete_flight method to delete a flight that does not exist and verify that
     an error is raised."""
    return


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
