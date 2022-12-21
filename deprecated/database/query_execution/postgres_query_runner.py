from termcolor import colored

from apis.api_cruds.postgres_crud import postgres_list_all_queries
from deprecated.update_flight_prices import UpdateFlight


def run_all_postgres_queries():
    all_queries = postgres_list_all_queries()[0].values()
    if not all_queries:
        return "No queries found", 404
    result_pot = []
    ufd = UpdateFlight()
    for query in all_queries:
        result = run_query(ufd, query)
        result_pot.append(result)
    if new_cheapest := [item for item in result_pot if item[1] == 200]:
        return new_cheapest[0]
    else:
        return "No new cheapest flight found!", 206


def run_query(flight_updater: UpdateFlight, query: dict) -> tuple[str, int]:
    query_name = query["query_name"]
    flight_updater.set_query(query)
    print(colored(f"Updating query {query_name}", "green"))
    return flight_updater.update_flight_db()


def __main():
    run_all_postgres_queries()


if __name__ == "__main__":
    __main()
