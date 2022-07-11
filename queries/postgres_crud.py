from typing import Union, Tuple, Dict, Any

from postgres.postgres_database_runner import PostgresRunner
from postgres.postgres_wrapper import PostgresWrapper

runner = PostgresWrapper()


def insert_tag(input_dict: dict, input_tag: str):
    input_dict["query_name"] = input_tag


def jsonify_flight_query(input_tuple: tuple) -> dict:
    return {"fly_from": input_tuple[1], "fly_to": input_tuple[2], "date_from": input_tuple[3],
            "date_to": input_tuple[4], "query_limit": input_tuple[5], "query_name": input_tuple[6]}


def get_flight_query(tag: str) -> Union[bool, dict]:
    aux = {"query_name": tag}
    result = runner.entry_handler.flight_query_read(aux)
    if not result:
        return False
    return jsonify_flight_query(result[0])


def postgres_create_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.entry_handler.flight_query_create(dictionary)
    if not result:
        return f"Query {tag} already exists", 406
    return f"Query {tag} created successfully", 200


def postgres_read_query(tag: str) -> Union[tuple[str, int], tuple[dict[str, Any], int]]:
    result = get_flight_query(tag)
    if not result:
        return f"Query {tag} does not exist", 404
    # res_dict = jsonify_flight_query(result[0])
    return result, 200


def postgres_update_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.entry_handler.flight_query_update(dictionary)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} updated successfully", 200


def postgres_delete_query(tag: str) -> tuple[str, int]:
    aux = {"query_name": tag}
    result = runner.entry_handler.flight_query_delete(aux)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} deleted successfully", 200


def postgres_list_all_queries():
    result = runner.entry_handler.list_all_queries()
    result_dict = {item[-1]: jsonify_flight_query(item) for item in result}
    return result_dict, 200
