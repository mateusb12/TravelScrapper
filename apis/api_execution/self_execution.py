import requests


def run_travel_loop():
    url = "http://travelscrapper.herokuapp.com/run_all_queries"
    return requests.post(url)


def __main():
    aux = run_travel_loop()
    print(run_travel_loop())


if __name__ == "__main__":
    __main()
