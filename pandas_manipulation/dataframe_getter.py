from apis.api_cruds.postgres_crud import postgres_get_all_flights_df


def __main():
    all_flights = postgres_get_all_flights_df()
    print("nice")


if __name__ == "__main__":
    __main()
