import random
from datetime import datetime, timedelta

from airports.airport_exporter import export_codes
from references.paths import get_airports_reference


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
        duration = timedelta(minutes=random.randint(40, 1080))
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

    def generate_single_flight(self):
        airport_codes = self.__generate_random_airport_codes()
        airline_codes = self.__generate_airline_codes()
        dates = self.__generate_random_dates()
        price = self.__generate_random_prices()
        query_date = self.__generate_query_date()
        flight_dict = {**airport_codes, **dates, "airlines": airline_codes, "price": price, "queryDate": query_date}
        return 0


def __main():
    fdg = FlightDataGenerator()
    aux = fdg.generate_single_flight()
    return


if __name__ == '__main__':
    __main()
