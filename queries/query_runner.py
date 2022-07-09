import json
from pathlib import Path

from references.paths import get_queries_reference
from travel_analysis.price_monitor import UpdateFlight


def get_query(tag: str):
    json_ref = Path(get_queries_reference(), f"{tag}.json")
    if json_ref.exists():
        with open(json_ref, "r") as json_file:
            return json.load(json_file), 200
    else:
        return "Query does not exist", 404


def run_query(tag: str):
    query, status = get_query(tag)
    ufd = UpdateFlight(filename=f"{tag}.csv", kiwi_dict=query)
    return ufd.update_flight_db()


def run_all_queries():
    queries = [file.stem for file in Path(get_queries_reference()).iterdir() if file.suffix == ".json"]
    results = [run_query(query) for query in queries]
    if cheapest := [item for item in results if item[1] == 200]:
        return "New cheapest flight found!", 200
    else:
        return "No new cheapest flight found!", 206


def __main():
    run_all_queries()


if __name__ == "__main__":
    __main()
