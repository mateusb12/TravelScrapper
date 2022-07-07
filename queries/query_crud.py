import json
from pathlib import Path

from references.paths import get_queries_reference


def create_query_file(dictionary: dict, tag: str) -> tuple[str, int]:
    file_name = f"{tag}.json"
    p = Path(get_queries_reference(), file_name)
    if p.exists():
        return f"{tag} query already exist", 406
    with open(p, 'w') as f:
        json.dump(dictionary, f)
    print(f"Saved {file_name}")
    return f"{file_name} created", 201


def update_query_file(dictionary: dict, tag: str) -> tuple[str, int]:
    p = Path(get_queries_reference(), f"{tag}.json")
    if not p.exists():
        return f"{tag} query does not exist", 404
    with open(p, 'w') as f:
        json.dump(dictionary, f)
    print(f"Updated {tag}.json")
    return f"{tag}.json updated", 200


def delete_query_file(tag: str) -> tuple[str, int]:
    p = Path(get_queries_reference(), f"{tag}.json")
    if p.exists():
        p.unlink()
        return f"Deleted {tag}.json", 200
    else:
        return f"{tag}.json does not exist", 404


def get_existing_query(tag: str) -> tuple[str, int]:
    p = Path(get_queries_reference(), f"{tag}.json")
    if not p.exists():
        return f"{tag} query does not exist", 404
    with open(p, 'r') as f:
        return json.load(f), 200


def existing_queries():
    p = Path(get_queries_reference())
    return [file.stem for file in p.iterdir() if file.suffix == ".json"]


def __main():
    # dict_example = {"fly_from": "FOR", "fly_to": "RIO", "date_from": "01/10/2022", "date_to": "12/12/2022",
    #                 "limit": 500}
    # create_query_file(dict_example, "fortaleza_rio")
    # delete_query("fortaleza_rio")
    print(get_existing_query("fortaleza_rio"))


if __name__ == "__main__":
    __main()
    print("done!")
