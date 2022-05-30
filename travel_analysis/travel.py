from typing import List

from api_consumer.kiwi_api_call import kiwi_call_example
from travel_analysis.flight import Flight


class TravelAnalyser:
    def __init__(self, data: dict):
        self.raw_data = data
        threshold = 5
        self.flight_data: List[Flight] = [Flight(item, layover_threshold=threshold) for item in data['data']]
        self.flight_data.sort(key=lambda x: x.price)

    def filter_long_layover_flights(self):
        self.flight_data = [item for item in self.flight_data if item.long_layover is False]


if __name__ == "__main__":
    ta = TravelAnalyser(kiwi_call_example())
    ta.filter_long_layover_flights()
    pass
