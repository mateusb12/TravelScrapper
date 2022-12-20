import random
from datetime import datetime, timedelta

from apis.api_consumer.kiwi_api_call import kiwi_call_example
from deprecated.database import seconds_to_hours_and_minutes


class Flight:
    def __init__(self, input_flight_data: dict, **kwargs):
        self.threshold = kwargs.get('layover_threshold', 5)
        self.default_layover_threshold = timedelta(hours=self.threshold)
        self.data = input_flight_data
        self.long_layover = False
        self.flight_from = input_flight_data['cityFrom']
        self.flight_to = input_flight_data['cityTo']
        self.country_from = input_flight_data['countryFrom']["name"]
        self.country_to = input_flight_data['countryTo']["name"]
        self.quality = input_flight_data['quality']
        self.duration_seconds = input_flight_data['duration']['total']
        self.duration = seconds_to_hours_and_minutes(self.duration_seconds)
        self.price = input_flight_data['price']
        self.bag_price = input_flight_data['bags_price']
        self.seats_available = input_flight_data['availability']['seats']
        self.connections = input_flight_data['route']
        self.routes = input_flight_data['route']
        self.link = input_flight_data['deep_link']
        self.time_departure = datetime.strptime(input_flight_data['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .strftime("%H:%M")
        self.time_arrival = datetime.strptime(input_flight_data['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .strftime("%H:%M")
        self.connection_times = self.calculate_connection_time()
        self.date_departure = datetime.strptime(input_flight_data['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .strftime("%d-%m-%Y")  # .replace(":", "-")
        self.date_arrival = datetime.strptime(input_flight_data['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .strftime("%d-%m-%Y")  # .replace(":", "-")
        self.flight_numbers = [route['flight_no'] for route in self.routes]
        self.identifier = f"{self.flight_from}_{self.flight_to}"
        self.fill_connection_times()
        self.less_than = input_flight_data['less_than']

    def calculate_connection_time(self) -> list[timedelta]:
        # sourcery skip: for-append-to-extend, inline-immediately-returned-variable, list-comprehension
        connection_time_list = []
        for i in range(len(self.routes) - 1):
            current_flight = datetime.strptime(self.routes[i]['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ')
            next_flight = datetime.strptime(self.routes[i + 1]['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ')
            difference = next_flight - current_flight
            connection_time_list.append(difference)
        for item in connection_time_list:
            if item > self.default_layover_threshold:
                self.long_layover = True
        return connection_time_list

    def is_direct_flight(self) -> bool:
        return self.connection_times[0] == "00:00"

    def fill_connection_times(self):
        if len(self.connection_times) == 2:
            self.connection_times.append(timedelta(0))
        elif len(self.connection_times) == 1:
            self.connection_times.append(timedelta(0))
            self.connection_times.append(timedelta(0))
        elif len(self.connection_times) == 0:
            self.connection_times.append(timedelta(0))
            self.connection_times.append(timedelta(0))
            self.connection_times.append(timedelta(0))

    # def convert_to_dict(self) -> dict:
    #     return {"price": self.price, "quality": int(self.quality), "cityFrom": self.flight_from,
    #             "cityTo": self.flight_to, "departure": self.time_departure, "arrival": self.time_arrival,
    #             "dateDeparture": self.date_departure, "dateArrival": self.date_arrival,
    #             "flightDuration": self.duration, "directFlight": self.is_direct_flight(),
    #             "flightDurationSeconds": self.duration_seconds,
    #             "longLayover": self.long_layover,
    #             "seatsAvailable": self.seats_available if self.seats_available is not None else 0,
    #             "connection_1": timedelta_format(self.connection_times[0]),
    #             "connection_2": timedelta_format(self.connection_times[1]),
    #             "connection_3": timedelta_format(self.connection_times[2]),
    #             "link": self.link}


def get_flight_object_example() -> Flight:
    flight_data = kiwi_call_example()
    example = random.choice(flight_data["data"])
    return Flight(example)


if __name__ == "__main__":
    flight = get_flight_object_example()
