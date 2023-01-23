from fix_flask_imports import fix_path
fix_path()
import ast
from typing import Optional

from flask import Flask, request, render_template, redirect, url_for, session

from firebase_data.firebase_factory import FirebaseFactory, get_dummy_flights
from global_monitor import GlobalFlightMonitor
from price_monitor.flight_utils import convert_html_date

factory: FirebaseFactory = FirebaseFactory()
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/login', methods=['GET', 'POST'])
def login():
    global factory
    if request.method == 'GET':
        return render_template("login_page.html")
    username = request.form['username']
    password = request.form['password']
    print(f"Username: {username}, Password: {password}")
    factory.run(username, password)
    session['username'] = username
    return redirect('/user_details')


@app.route('/user_details', methods=['GET', 'POST'])
def user_details():
    user_name = session.get('username', "email not found")
    return render_template("flight_user_details.html", username=user_name)


@app.route('/flight_query_viewer')
def flight_query_viewer():
    global factory
    all_queries = factory.firebase_query.read_all_queries()
    return render_template("flight_query_viewer.html", query_dict=all_queries)


@app.route('/dummy')
def dummy():
    return render_template("dummy.html")


@app.route('/delete_query/<query_id>', methods=['DELETE'])
def delete_query(query_id):
    global factory
    print("Delete query")
    factory.firebase_query.delete_query_by_unique_id(query_id)
    return 'Query successfully deleted', 204


@app.route('/flight_data_viewer')
def flight_data_viewer():
    global factory
    all_flights = factory.firebase_flights.read_all_flights()
    return render_template("flight_data_viewer.html", flight_data=all_flights)


@app.route('/query_creator', methods=['GET', 'POST'])
def forms():
    if request.method == 'GET':
        return render_template('query_form.html')
    print("You have clicked on the submit button!")
    res = dict(request.form)
    desired_query = {
        "departureAirport": request.form['departure-airport'],
        "arrivalAirport": request.form['arrival-airport'],
        "departureDate": convert_html_date(request.form['departure-date'])
    }
    result = factory.firebase_query.create_query(desired_query)
    return redirect('/user_details')


@app.route("/flight_results", methods=['GET', 'POST'])
def results():
    results_string = request.args.get('results')
    flight_results = ast.literal_eval(results_string)
    return render_template('flight_results.html', results=flight_results)


@app.route("/run_query", methods=['GET', 'POST'])
def run_query():
    global factory
    factory.firebase_monitor.search_prices()
    print("Finished searching prices!")
    query_results = factory.firebase_monitor.output
    return render_template('flight_monitor_results.html', output=query_results)


@app.route("/start_pipeline", methods=['GET', 'POST'])
def start_pipeline():
    gfm = GlobalFlightMonitor()
    monitor = gfm.factory.firebase_monitor
    monitor.search_prices()
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
