from apis.api_cruds.postgres_crud import get_flight_query
from updater.price_monitor import UpdateFlight


def __main():
    query = get_flight_query("fortaleza_rio")
    ufd = UpdateFlight(kiwi_dict=query)
    ufd.update_flight_db()
    print(query)


if __name__ == "__main__":
    __main()
