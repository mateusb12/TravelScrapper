from time_manipulations import *
import pandas as pd


class FillerGenerator:
    def __init__(self, city_from: str = "London", city_to: str = "Madrid"):
        self.price = random_normal_number(126.78, 21.63)
        self.quality = random_normal_number(299.40, 102.42)
        self.departure = random_time(8, 18)
        self.flight_duration = random_time(2, 10)
        self.arrival = sum_time(self.departure, self.flight_duration)
        self.flight_duration_seconds = time_to_seconds(self.flight_duration)
        self.seats_available = random_normal_number(3.008333, 2.027110)
        self.departure_date = random_date()
        self.arrival_date = sum_days(self.departure_date, random.randint(0, 1))
        self.city_from = city_from
        self.city_to = city_to

    def export_to_series(self):
        series_format = {"price": self.price, "quality": self.quality,
                         "cityFrom": self.city_from, "cityTo": self.city_to,
                         "departure": self.departure, "arrival": self.arrival, "date_departure": self.departure_date,
                         "date_arrival": self.arrival_date, "flightDuration": self.flight_duration,
                         "direct_flight": True, "flightDurationSeconds": self.flight_duration_seconds,
                         "longLayover": False, "seatsAvailable": self.seats_available, "connection_1": 0,
                         "connection_2": 0, "connection_3": 0, "link": "https://www.google.com"}
        return pd.Series(series_format)


if __name__ == "__main__":
    fg = FillerGenerator()
    print(fg.export_to_series())
