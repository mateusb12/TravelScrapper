from typing import List

from api_consumer.kiwi_api_call import kiwi_call_example
from travel_analysis.flight import Flight

import pandas as pd


class TravelAnalyser:
    def __init__(self, data: dict, threshold: int = 5):
        self.raw_data = data
        self.flight_data = None
        self.create_flights(threshold=5)

    def create_flights(self, **kwargs):
        threshold = kwargs.get('threshold', 5)
        self.flight_data: List[Flight] = [Flight(item, layover_threshold=threshold) for item in self.raw_data['data']]
        self.flight_data.sort(key=lambda x: x.price)

    def filter_long_layover_flights(self, **kwargs):
        threshold = kwargs.get('threshold', 5)
        self.create_flights(threshold=threshold)
        self.flight_data = [item for item in self.flight_data if item.long_layover is False]

    def df_generator(self) -> pd.DataFrame:  # sourcery skip: merge-dict-assign
        pre_df = []
        for item in self.flight_data:
            aux = {"price": item.price, "quality": round(item.quality), "cityFrom": item.flight_from,
                   "cityTo": item.flight_to, "departure": item.time_departure, "arrival": item.time_arrival,
                   "flightDuration": item.duration, "flightDurationSeconds": item.duration_seconds,
                   "longLayover": item.long_layover,
                   "seats_available": int(item.seats_available) if item.seats_available is not None else 0,
                   "connection_1": 0, "connection_2": 0, "connection_3": 0}
            for index, connection in enumerate(item.connection_times, 1):
                aux[f'connection_{str(index)}'] = int(connection.seconds)
            aux["link"] = item.link
            pre_df.append(aux)
        df = pd.DataFrame(pre_df)
        df["directFlight"] = df.apply(lambda row: row["connection_1"] == 0 and row["connection_2"] == 0 and
                                                  row["connection_3"] == 0, axis=1)
        direct_flight = df.pop("directFlight")
        df.insert(8, "directFlight", direct_flight)
        return df


if __name__ == "__main__":
    ta = TravelAnalyser(kiwi_call_example())
    ta.df_generator()
    # ta.filter_long_layover_flights(threshold=5)
    # pass
