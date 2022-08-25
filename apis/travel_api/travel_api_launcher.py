import collections
import json
import os

from flask import Flask, jsonify, request
from apis.api_cruds.postgres_crud import postgres_create_query, postgres_read_query, postgres_update_query, \
    postgres_delete_query, postgres_list_all_queries, postgres_create_flight, postgres_list_all_flights, \
    postgres_read_flight, postgres_refresh_db
from database.query_execution.postgres_query_runner import run_all_postgres_queries

application = Flask(__name__)
application.config['JSON_SORT_KEYS'] = False


@application.route("/")
def homepage():
    raw_dict = {"a": "b", "b": "c"}
    return jsonify(raw_dict)


@application.route("/get_example/<tag>", methods=["GET"])
def get_example(tag: str):
    if tag == "rio":
        return jsonify({"fly_from": "FOR", "fly_to": "RIO",
                        "date_from": "01/10/2022", "date_to": "12/12/2022", "limit": 500})

    elif tag == "sp":
        example_dict = {"fly_from": "FOR", "fly_to": "SP", "date_from": "01/07/2022",
                        "date_to": "30/07/2022", "limit": 500}
    else:
        example_dict = {}
    return jsonify(example_dict)


@application.route("/create_query/<tag>", methods=["POST"])
def create_query(tag: str):
    query_dict = request.json
    return postgres_create_query(query_dict, tag)


@application.route("/get_query/<tag>", methods=["GET"])
def get_query(tag: str):
    return postgres_read_query(tag)


@application.route("/update_query/<tag>", methods=["PATCH"])
def update_query(tag: str):
    query_dict = request.json
    return postgres_update_query(query_dict, tag)


@application.route("/delete_query/<tag>", methods=["DELETE"])
def delete_query(tag: str):
    return postgres_delete_query(tag)


@application.route("/list_query", methods=["GET"])
def list_all_query():
    res = postgres_list_all_queries()
    content = res[0]
    http_result = res[1]
    return content, http_result


@application.route("/create_flight", methods=["POST"])
def create_flight():
    flight_dict = request.json
    return postgres_create_flight(flight_dict)


@application.route("/read_flight/<tag>", methods=["GET"])
def read_flight(tag: str):
    return postgres_read_flight(tag)


@application.route("/read_all_flights", methods=["GET"])
def read_all_flights():
    return postgres_list_all_flights()


@application.route("/run_all_queries", methods=["POST"])
def run_all():
    print(os.environ.keys())
    return run_all_postgres_queries()


@application.route("/refresh_db", methods=["DELETE"])
def refresh_db():
    return postgres_refresh_db()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    application.run(port=port, debug=True)
