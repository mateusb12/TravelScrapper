from typing import List
from datetime import datetime, timedelta

from api_consumer.kiwi_api_call import kiwi_call_example


class TravelAnalyser:
    def __init__(self, data: dict):
        self.raw_data = data
        self.flight_data: List[Flight] = [Flight(item) for item in data['data']]
        self.flight_data.sort(key=lambda x: x.price)


class Flight:
    def __init__(self, input_flight_data: dict):
        self.data = input_flight_data
        self.long_layover = False
        self.flight_from = input_flight_data['cityFrom']
        self.flight_to = input_flight_data['cityTo']
        self.country_from = input_flight_data['countryFrom']["name"]
        self.country_to = input_flight_data['countryTo']["name"]
        self.quality = input_flight_data['quality']
        self.duration_seconds = input_flight_data['duration']['total']
        self.duration = datetime.fromtimestamp(self.duration_seconds).strftime('%H:%M')
        self.price = input_flight_data['price']
        self.bag_price = input_flight_data['bags_price']
        self.seats_available = input_flight_data['availability']['seats']
        self.connections = input_flight_data['routes']
        self.routes = input_flight_data['route']
        self.link = input_flight_data['deep_link']
        self.time_departure = input_flight_data['local_departure']
        self.time_arrival = input_flight_data['local_arrival']
        self.connection_times = self.calculate_connection_time(layover_threshold=5)

    def calculate_connection_time(self, **kwargs) -> list[timedelta]:
        # sourcery skip: for-append-to-extend, inline-immediately-returned-variable, list-comprehension
        layover_threshold = timedelta(hours=kwargs.get('layover_threshold', 5))
        connection_time_list = []
        for i in range(len(self.routes) - 1):
            current_flight = datetime.strptime(self.routes[i]['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ')
            next_flight = datetime.strptime(self.routes[i + 1]['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ')
            difference = next_flight - current_flight
            connection_time_list.append(difference)
        for item in connection_time_list:
            if item > layover_threshold:
                self.long_layover = True
        return connection_time_list


if __name__ == "__main__":
    ta = TravelAnalyser(kiwi_call_example())
    print(ta.flight_data[0].duration)
    pass
