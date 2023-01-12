import ast

from flask import Flask, request, render_template, redirect, url_for

from firebase_data.firebase_factory import login_pipeline, get_all_queries

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login_page.html")
    username = request.form['username']
    password = request.form['password']
    print(f"Username: {username}, Password: {password}")
    firebase_app = login_pipeline(email=username, password=password)
    all_queries = get_all_queries(firebase_app)
    return render_template("flight_query_viewer.html", query_dict=all_queries)


@app.route('/query_creator', methods=['GET', 'POST'])
def forms():
    if request.method == 'GET':
        return render_template('query_form.html')
    print("You have clicked on the submit button!")
    flight_results = {
        'folder_name': request.form['folder-name'],
        'departure_airport': request.form['departure-airport'],
        'arrival_airport': request.form['arrival-airport'],
        'price': request.form['price'],
        'duration': request.form['duration']
    }
    # return render_template('flight_results.html', results=flight_results)
    return redirect(url_for('results', results=flight_results))


@app.route("/flight_results", methods=['GET', 'POST'])
def results():
    results_string = request.args.get('results')
    flight_results = ast.literal_eval(results_string)
    return render_template('flight_results.html', results=flight_results)


if __name__ == '__main__':
    app.run()
