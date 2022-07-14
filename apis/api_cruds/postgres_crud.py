from typing import Union, Any

import pandas as pd

from database.fillers.data_skeleton import jsonify_flight_data
from database.postgres.wrappers.postgres_wrapper import PostgresWrapper

runner = PostgresWrapper()


def insert_tag(input_dict: dict, input_tag: str):
    input_dict["query_name"] = input_tag


def jsonify_flight_query(input_tuple: tuple) -> dict:
    return {"fly_from": input_tuple[1], "fly_to": input_tuple[2], "date_from": input_tuple[3],
            "date_to": input_tuple[4], "query_limit": input_tuple[5], "query_name": input_tuple[6]}


def get_flight_query(tag: str) -> Union[bool, dict]:
    result = runner.query_handler.flight_query_read(tag)
    if not result:
        return False
    return jsonify_flight_query(result[0])


def postgres_create_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.query_handler.flight_query_create(dictionary)
    if not result:
        return f"Query {tag} already exists", 406
    return f"Query {tag} created successfully", 200


def postgres_read_query(tag: str) -> Union[tuple[str, int], tuple[dict[str, Any], int]]:
    result = get_flight_query(tag)
    if not result:
        return f"Query {tag} does not exist", 404
    return result, 200


def postgres_update_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.query_handler.flight_query_update(dictionary)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} updated successfully", 200


def postgres_delete_query(tag: str) -> tuple[str, int]:
    result = runner.query_handler.flight_query_delete(tag)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} deleted successfully", 200


def postgres_list_all_queries() -> tuple[dict, int]:
    result = runner.query_handler.list_all_queries()
    result_dict = {item["query_name"]: item for item in result}
    return result_dict, 200


def postgres_list_all_flights() -> dict:
    postgres_output = runner.flight_handler.list_all_flights()
    return {int(item[0]): jsonify_flight_data(item) for item in postgres_output}


def postgres_get_flight_keys() -> list[str]:
    keys = runner.flight_handler.get_keys()
    if "id" not in keys:
        keys.insert(0, "id")
    return keys


def postgres_get_all_flights_df() -> pd.DataFrame:
    flight_data = postgres_list_all_flights()
    flight_tuples = [list(value.values()) for value in flight_data.values()]
    flight_keys = postgres_get_flight_keys()
    return pd.DataFrame(flight_tuples, columns=flight_keys)


def postgres_create_flight(flight_dict: dict):
    return runner.flight_handler.flight_data_create(flight_dict)


def postgres_read_flight(flight_tag: str):
    return runner.flight_handler.flight_data_read(flight_tag)


def postgres_update_flight(flight_dict: dict):
    return runner.flight_handler.flight_data_update(flight_dict)


def postgres_delete_flight(flight_tag: str):
    return runner.flight_handler.flight_data_delete(flight_tag)


def postgres_refresh_db() -> tuple[str, int]:
    runner.refresh_db()
    return "Database refreshed successfully", 200


def __main():
    all_flights = postgres_get_all_flights_df()
    print(all_flights)


if __name__ == "__main__":
    __main()
