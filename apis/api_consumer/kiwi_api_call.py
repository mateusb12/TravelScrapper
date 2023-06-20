import os
from datetime import datetime, timedelta

import requests as requests


def kiwi_call(**kwargs) -> dict:
    fly_from = kwargs.get('fly_from')
    fly_to = kwargs.get('fly_to')
    date_from = kwargs.get('date_from')
    date_to = kwargs.get('date_to')
    limit = kwargs.get('limit')
    param_tag = f"fly_from={fly_from}&fly_to={fly_to}&dateFrom={date_from}&dateTo={date_to}&limit={limit}"
    url = f"https://tequila-api.kiwi.com/v2/search?{param_tag}"
    api_key = os.environ["KIWI_TOKEN"]
    header_dict = {
        "apikey": api_key,
        "max_fly_duration": "20",
    }
    response = requests.get(url, headers=header_dict)
    return response.json()


def kiwi_call_example() -> dict:
    current_date = datetime.now()
    one_month_ago = current_date - timedelta(days=30)
    one_month_later = current_date + timedelta(days=30)

    date_from = one_month_ago.strftime("%d/%m/%Y")
    date_to = one_month_later.strftime("%d/%m/%Y")

    return kiwi_call(fly_from="FOR", fly_to="RIO", date_from=date_from, date_to=date_to, limit=500)


def kiwi_call_sp_example() -> dict:
    return kiwi_call(fly_from="FOR", fly_to="SAO", date_from="01/01/2023", date_to="01/03/2023", limit=500)


def set_kiwi_call(config: dict) -> dict:
    fly_from = config.get('fly_from')
    fly_to = config.get('fly_to')
    date_from = config.get('date_from')
    date_to = config.get('date_to')
    limit = config.get('query_limit')
    return kiwi_call(fly_from=fly_from, fly_to=fly_to, date_from=date_from, date_to=date_to, limit=limit)


def __main():
    call = kiwi_call_example()
    return


if __name__ == "__main__":
    __main()
