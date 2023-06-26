import os
from flask import Flask, jsonify, request
from firebase_data.firebase_factory import FirebaseFactory, getFactoryInstance
from ariadne import make_executable_schema, graphql_sync
from apis.travel_api.schemas import type_defs, resolvers

factory: FirebaseFactory = getFactoryInstance()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
schema = make_executable_schema(type_defs, resolvers)


@app.route("/graphql", methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.route("/")
def homepage():
    # Create a hello world message.
    return "Hello world!", 200


@app.route("/get_all_queries", methods=['GET'])
def get_all_queries():
    all_queries = factory.firebase_query.read_all_queries()
    return all_queries, 200


@app.route("/get_all_flights", methods=['GET'])
def get_all_flights():
    all_flights = factory.firebase_flights.read_all_flights()
    return all_flights, 200


@app.route("/get_all_users", methods=['GET'])
def get_all_users():
    raw_query = factory.user_crud.get_all_users()
    raw_users = raw_query["outputDetails"]
    userList = []
    for user in raw_users:
        displayName = user.display_name
        email = user.email
        phoneNumber = user.phone_number
        uniqueId = user.uid
        userList.append({"displayName": displayName, "email": email, "phoneNumber": phoneNumber, "uniqueId": uniqueId})
    return jsonify(userList), 200


def __main():
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    __main()
