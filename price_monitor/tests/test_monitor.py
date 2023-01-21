import pytest

from apis.api_consumer.kiwi_api_call import kiwi_call
from price_monitor.flight_monitor import FlightMonitor


@pytest.fixture(scope="module")
def get_flight_monitor_instance():
    fm = FlightMonitor()
    today = fm.today_date
    fm.flight_crud.set_folder(f"test/{today}")
    return fm


@pytest.mark.search_prices(order=1)
def test_gather_current_data_handles_empty_firebase_response(get_flight_monitor_instance):
    fm = get_flight_monitor_instance
    fm.flight_crud.delete_folder("test")
    fm.search_prices()
    current_firebase_structure = fm.flight_crud.firebase_app.db.reference("/").get()
    today_flights = current_firebase_structure["test"][fm.today_date]
    assert fm.existing_flight_data == []
    assert len(today_flights) == 1


@pytest.mark.search_prices(order=2)
def test_run_creates_new_node_when_no_stored_flights(get_flight_monitor_instance):
    fm = get_flight_monitor_instance
    fm.search_prices()
    current_firebase_structure = fm.flight_crud.firebase_app.db.reference("/").get()
    assert len(current_firebase_structure["test"].keys()) == 1
    assert len(fm.existing_flight_data) == 1
    assert len(fm.new_flight_data) >= 1


@pytest.mark.search_prices(order=3)
def test_trim_kiwi_data_removes_expensive_flights(get_flight_monitor_instance):
    fm = get_flight_monitor_instance
    kiwi_api_call = kiwi_call(fly_from="FOR", fly_to="RIO", date_from="01/01/2023",
                              date_to="01/03/2023", limit=500)["data"]
    trimmed_data = fm._trim_kiwi_data(kiwi_api_call)
    assert len(trimmed_data) < len(kiwi_api_call)


@pytest.mark.search_prices(order=4)
def test_analyze_new_data_notifies_when_cheaper_flight_found(get_flight_monitor_instance):
    fm = get_flight_monitor_instance
    fm._gather_current_firebase_flight_data()
    fm._collect_new_kiwi_data()
    fm.new_flight_data[0]["price"] = 5
    result = fm._analyze_new_data()
    assert result["output"] == "success"


@pytest.mark.search_prices(order=5)
def test_analyze_new_data_not_notify_when_no_cheaper_flight_found(get_flight_monitor_instance):
    fm = get_flight_monitor_instance
    fm._gather_current_firebase_flight_data()
    fm._collect_new_kiwi_data()
    fm.new_flight_data[0]["price"] = 100000
    result = fm._analyze_new_data()
    fm.flight_crud.delete_folder("test")
    assert result["output"] == "failure"


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
