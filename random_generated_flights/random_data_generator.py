import random

from airports.airport_exporter import export_codes
from references.paths import get_airports_reference


class FlightDataGenerator:
    def __init__(self):
        self.airport_codes_dict = export_codes('BR')
        self.airport_codes = list(self.airport_codes_dict.values())

    def generate_random_airport_codes(self) -> dict:
        departure_airport, arrival_airport = random.sample(self.airport_codes, 2)
        return {"arrivalAirport": arrival_airport, "departureAirport": departure_airport}


def __main():
    fdg = FlightDataGenerator()
    aux = fdg.generate_random_airport_codes()
    return


if __name__ == '__main__':
    __main()
