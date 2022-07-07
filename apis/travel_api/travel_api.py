import os

from flask import Flask, jsonify, request, Response

from queries.query_saver import create_query_file, delete_query_file, existing_queries, get_existing_query
from travel_analysis.price_monitor import UpdateFlight

app = Flask(__name__)


@app.route("/")
def homepage():
    raw_dict = {"a": "b", "b": "c"}
    return jsonify(raw_dict)


@app.route("/get_example/<tag>", methods=["GET"])
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


@app.route("/create_query/<tag>", methods=["POST"])
def create_query(tag: str):
    query_dict = request.json
    return create_query_file(query_dict, tag)


@app.route("/delete_query/<tag>", methods=["DELETE"])
def delete_query(tag: str):
    return delete_query_file(tag)

    # ufd = UpdateFlight(filename=f"{tag}.csv", kiwi_dict=query_dict)
    # ufd.update_flight_db()
    # return Response(status=201)


@app.route("/list_query", methods=["GET"])
def list_all_query():
    return jsonify(existing_queries())


@app.route("/get_query/<tag>", methods=["GET"])
def get_query(tag: str):
    return get_existing_query(tag)


# @app.route('/get_round_impact/<input_match_id>', methods=["GET"])
# def get_round_impact(input_match_id):
#     """
#     Json format
#     {
#         "match_id": 44795,
#         "round": 1,
#         "side": "atk"
#     }
#     """
#     match_id = input_match_id
#     rr_instance = RoundReplay(vv.model)
#     rr_instance.set_match(match_id)
#     total_rounds = rr_instance.analyser.round_amount
#     proba_plot = []
#     for i in range(1, total_rounds):
#         rr_instance.choose_round(i)
#         proba_plot.append(rr_instance.get_round_probability(side="atk"))
#     round_impact_df = pd.concat(proba_plot, axis=0)
#     dict_to_return = round_impact_df.to_dict('list')
#     return jsonify(dict_to_return)

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
