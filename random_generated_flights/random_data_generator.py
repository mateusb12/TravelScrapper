import random
from datetime import datetime, timedelta

from airports.airport_exporter import export_codes
from references.paths import get_airports_reference
from wrapper.flight_utils import beautify_date, analyze_layover_durations


class FlightDataGenerator:
    def __init__(self):
        self.airport_codes_dict = export_codes('BR')
        self.airport_codes = list(self.airport_codes_dict.values())
        self.number_of_stops = random.randint(1, 2)
        self.flight_pot = []

    def __generate_random_airport_codes(self) -> dict:
        departure_airport, arrival_airport = random.sample(self.airport_codes, 2)
        return {"arrivalAirport": arrival_airport, "departureAirport": departure_airport}

    def __generate_airline_codes(self):
        airline_pot = ["AD", "G3", "JJ", "O6", "WJ"]
        return [random.choice(airline_pot) for _ in range(self.number_of_stops)]

    @staticmethod
    def __generate_random_departure_date():
        # Choose a random day in the year 2023
        start = datetime(2023, 1, 1)
        end = datetime(2024, 1, 1)
        num_days = (end - start).days
        random_day = start + timedelta(days=random.uniform(0, num_days))
        return random_day.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    @staticmethod
    def __generate_random_arrival_date(departure_time: str):
        date = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S.000Z')
        duration = timedelta(minutes=random.randint(40, 1000))
        arrival_time = date + duration
        return arrival_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    def __generate_random_dates(self):
        departure_date = self.__generate_random_departure_date()
        arrival_date = self.__generate_random_arrival_date(departure_date)
        return {"departureTime": departure_date, "arrivalTime": arrival_date}

    @staticmethod
    def __generate_random_prices():
        return round(random.uniform(50, 600), 2)

    def __generate_query_date(self):
        if len(self.flight_pot) == 0:
            return datetime.now().strftime('%d-%b-%Y')
        last_date = self.flight_pot[-1]["queryDate"]
        date = datetime.strptime(last_date, '%d-%b-%Y')
        new_date = date + timedelta(days=1)
        return new_date.strftime('%d-%b-%Y')

    def __generate_single_complete_flight(self):
        airport_codes = self.__generate_random_airport_codes()
        airline_codes = self.__generate_airline_codes()
        dates = self.__generate_random_dates()
        price = self.__generate_random_prices()
        query_date = self.__generate_query_date()
        flight_dict = {**airport_codes, **dates, "airlines": airline_codes, "price": price, "queryDate": query_date}
        self.flight_pot.append(flight_dict)

    def generate_multiple_complete_flights(self, flight_amount: int) -> list[dict]:
        for _ in range(flight_amount):
            self.__generate_single_complete_flight()
        return self.flight_pot

    @staticmethod
    def __beautify_time_delta(input_time_delta: timedelta) -> str:
        hours = input_time_delta.seconds // 3600
        minutes = (input_time_delta.seconds // 60) % 60
        return f"{hours}h{minutes}m"

    def __generate_simple_flight(self, departure_airport: str = "FOR", arrival_airport: str = "RIO") -> dict:
        dates = self.__generate_random_dates()
        datetime_dates = {key: datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000Z') for key, value in dates.items()}
        delta_time_duration = datetime_dates["arrivalTime"] - datetime_dates["departureTime"]
        delta_time_str = self.__beautify_time_delta(delta_time_duration)
        stop_flights = None
        if stop_flights := self.__add_stop_flight(dates):
            layover_durations = analyze_layover_durations(stop_flights)
        else:
            layover_durations = [None]
        beautify_dates = [beautify_date(dates["departureTime"]), beautify_date(dates["arrivalTime"])]
        beautify_dates_dict = {"departureFormattedDateAndTime": beautify_dates[0],
                               "arrivalFormattedDateAndTime": beautify_dates[1]}
        price = self.__generate_random_prices()
        query_date = self.__generate_query_date()
        return {"departureAirport": departure_airport, "arrivalAirport": arrival_airport,
                **dates, **beautify_dates_dict, "flightDuration": delta_time_str,
                "layoverDurations": layover_durations, "queryDate": query_date, "_route": stop_flights,
                "price": price}

    @staticmethod
    def __add_stop_flight(dates: dict):
        date_pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
        departure_time = datetime.strptime(dates['departureTime'], date_pattern)
        arrival_time = datetime.strptime(dates['arrivalTime'], date_pattern)
        flight_duration = arrival_time - departure_time
        if flight_duration <= timedelta(hours=7):
            return
        layover_duration = timedelta(minutes=random.randint(40, 150))
        first_arrival_placement = flight_duration * random.uniform(0.3, 0.7)
        first_flight_arrival_timedelta = timedelta(seconds=round(first_arrival_placement.total_seconds()))
        first_arrival_time = departure_time + first_flight_arrival_timedelta
        second_departure_time = first_arrival_time + layover_duration
        first_flight = ({"type": "departure", "time": departure_time.strftime(date_pattern)},
                        {"type": "arrival", "time": first_arrival_time.strftime(date_pattern)})
        second_flight = ({"type": "departure", "time": second_departure_time.strftime(date_pattern)},
                         {"type": "arrival", "time": arrival_time.strftime(date_pattern)})
        return [first_flight, second_flight]

    def generate_multiple_simple_flights(self, flight_amount: int) -> list[dict]:
        for _ in range(flight_amount):
            flight = self.__generate_simple_flight()
            self.flight_pot.append(flight)
        return self.flight_pot


def __main():
    fdg = FlightDataGenerator()
    aux = fdg.generate_multiple_simple_flights(10)
    return


if __name__ == '__main__':
    __main()
