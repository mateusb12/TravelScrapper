import pandas as pd

from apis.api_cruds.postgres_crud import postgres_get_all_flights_df


def __get_flights() -> pd.DataFrame:
    flights = postgres_get_all_flights_df()
    flights.sort_values(by=["queryDate", "price"], inplace=True, ascending=True)
    return flights


def __main():
    all_flights = __get_flights()
    print("nice")


if __name__ == "__main__":
    __main()
