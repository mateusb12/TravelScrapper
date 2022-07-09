import os

from flask import Flask, jsonify, request, Response

from queries.query_crud import create_query_file, delete_query_file, existing_queries, get_existing_query, \
    update_query_file
from queries.query_runner import run_all_queries

application = Flask(__name__)


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
    return create_query_file(query_dict, tag)


@application.route("/update_query/<tag>", methods=["PATCH"])
def update_query(tag: str):
    query_dict = request.json
    return update_query_file(query_dict, tag)


@application.route("/delete_query/<tag>", methods=["DELETE"])
def delete_query(tag: str):
    return delete_query_file(tag)


@application.route("/list_query", methods=["GET"])
def list_all_query():
    return jsonify(existing_queries())


@application.route("/get_query/<tag>", methods=["GET"])
def get_query(tag: str):
    return get_existing_query(tag)


@application.route("/run_all_queries", methods=["POST"])
def run_all():
    return run_all_queries()


# port = int(os.environ.get('PORT', 8080))
# app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    application.run(port=port, debug=True)
