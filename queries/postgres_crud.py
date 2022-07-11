from postgres.postgres_runner import PostgresRunner

runner = PostgresRunner()


def insert_tag(input_dict: dict, input_tag: str):
    input_dict["query_name"] = input_tag


def create_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.flight_query_create(dictionary)
    if not result:
        return f"Query {tag} already exists", 406
    return f"Query {tag} created successfully", 200


def read_query(tag: str) -> tuple[str, int]:
    aux = {"query_name": tag}
    result = runner.flight_query_read(aux)
    if not result:
        return f"Query {tag} does not exist", 404
    return result, 200


def update_query(dictionary: dict, tag: str) -> tuple[str, int]:
    insert_tag(dictionary, tag)
    result = runner.flight_query_update(dictionary)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} updated successfully", 200


def delete_query(tag: str) -> tuple[str, int]:
    aux = {"query_name": tag}
    result = runner.flight_query_delete(aux)
    if not result:
        return f"Query {tag} does not exist", 404
    return f"Query {tag} deleted successfully", 200
