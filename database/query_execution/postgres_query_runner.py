from apis.cruds.postgres_crud import get_flight_query
from travel_analysis.price_monitor import UpdateFlight


def __main():
    query = get_flight_query("fortaleza_rio")
    ufd = UpdateFlight(kiwi_dict=query)
    ufd.update_flight_db()
    print(query)


if __name__ == "__main__":
    __main()
