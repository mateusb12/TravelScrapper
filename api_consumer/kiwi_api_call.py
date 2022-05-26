import requests as requests


def kiwi_call(**kwargs) -> dict:
    fly_from = kwargs.get('fly_from')
    fly_to = kwargs.get('fly_to')
    date_from = kwargs.get('date_from')
    date_to = kwargs.get('date_to')
    url = f"https://tequila-api.kiwi.com/v2/search?fly_from={fly_from}&fly_to={fly_to}"
    api_key = open("api.txt", "r").read()
    header_dict = {
        "apikey": api_key,
        "dateFrom": f"{date_from}",
        "dateTo": f"{date_to}",
        "max_fly_duration": "20",
    }
    response = requests.get(url, headers=header_dict)
    return response.json()


def kiwi_call_example():
    return kiwi_call(fly_from="LHR", fly_to="MAD", date_from="2020-06-01", date_to="2020-06-10")


if __name__ == "__main__":
    call = kiwi_call_example()
    print("oi")
