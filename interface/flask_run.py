from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def forms():
    if request.method == 'GET':
        return render_template('flight_form.html')
    print("You have clicked on the submit button!")
    flight_results = {
        'folder_name': request.form['folder-name'],
        'departure_airport': request.form['departure-airport'],
        'arrival_airport': request.form['arrival-airport'],
        'price': request.form['price'],
        'duration': request.form['duration']
    }
    return render_template('flight_results.html', results=flight_results)


@app.route("/flight_results", methods=['GET', 'POST'])
def results():
    return render_template('../templates/flight_results.html')


if __name__ == '__main__':
    app.run()
