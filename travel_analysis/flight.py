from datetime import datetime, timedelta


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
        self.duration = datetime.fromtimestamp(self.duration_seconds).strftime('%H:%M')
        self.price = input_flight_data['price']
        self.bag_price = input_flight_data['bags_price']
        self.seats_available = input_flight_data['availability']['seats']
        self.connections = input_flight_data['routes']
        self.routes = input_flight_data['route']
        self.link = input_flight_data['deep_link']
        self.time_departure = datetime.strptime(input_flight_data['local_departure'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%H:%M")
        self.time_arrival = datetime.strptime(input_flight_data['local_arrival'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%H:%M")
        self.connection_times = self.calculate_connection_time()

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
