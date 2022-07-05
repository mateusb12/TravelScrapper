from pathlib import Path

import requests as requests

from references.paths import get_api_consumer_path


def kiwi_call(**kwargs) -> dict:
    fly_from = kwargs.get('fly_from')
    fly_to = kwargs.get('fly_to')
    date_from = kwargs.get('date_from')
    date_to = kwargs.get('date_to')
    limit = kwargs.get('limit')
    param_tag = f"fly_from={fly_from}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&limit={limit}"
    url = f"https://tequila-api.kiwi.com/v2/search?{param_tag}"
    p = Path(get_api_consumer_path(), "api.txt")
    api_key = open(p, "r").read()
    header_dict = {
        "apikey": api_key,
        "max_fly_duration": "20",
    }
    response = requests.get(url, headers=header_dict)
    return response.json()


def kiwi_call_example():
    return kiwi_call(fly_from="FOR", fly_to="RIO", date_from="01/10/2022", date_to="12/12/2022", limit=500)


if __name__ == "__main__":
    call = kiwi_call_example()
    print("done!")
    # p = Path("api_consumer/api.txt")
    # print("oi")
