import os
from pathlib import Path

import pandas as pd


def create_empty_df(reference: Path) -> None:
    base_dict = {"id": 0, "price": 5000, "quality": 0, "cityFrom": "", "cityTo": "", "departure": "", "arrival": "",
                 "date_departure": "", "date_arrival": "", "flightDuration": "", "direct_flight": False,
                 "flightDurationSeconds": 0, "longLayover": False, "seatsAvailable": 0, "connection_1": "00:00",
                 "connection_2": "00:00", "connection_3": "00:00", "link": ""}
    base_dict = {k: [v] for k, v in base_dict.items()}
    df = pd.DataFrame(base_dict)
    df.to_csv(reference, index=False)
