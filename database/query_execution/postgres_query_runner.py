from termcolor import colored

from apis.api_cruds.postgres_crud import postgres_list_all_queries
from update_flight_prices.price_monitor import UpdateFlight


def run_all_postgres_queries():
    all_queries = postgres_list_all_queries()[0].values()
    result_pot = []
    for query in all_queries:
        result = run_query(query)
        result_pot.append(result)
    if new_cheapest := [item for item in result_pot if item[1] == 200]:
        return new_cheapest[0]
    else:
        return "No new cheapest flight found!", 206


def run_query(query: dict) -> tuple[str, int]:
    query_name = query["query_name"]
    ufd = UpdateFlight(kiwi_dict=query)
    print(colored(f"Updating query {query_name}", "green"))
    return ufd.update_flight_db()


def __main():
    run_all_postgres_queries()


if __name__ == "__main__":
    __main()
