from typing import List

from api_consumer.kiwi_api_call import kiwi_call_example
from travel_analysis.flight import Flight


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


if __name__ == "__main__":
    ta = TravelAnalyser(kiwi_call_example())
    ta.filter_long_layover_flights(threshold=5)
    pass
