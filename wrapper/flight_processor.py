from typing import List, Tuple, Dict

from apis.api_consumer.kiwi_api_call import kiwi_call_example
from datetime import datetime, timedelta

from wrapper.flight_utils import analyze_layover_durations, beautify_date, convert_timedelta_list_to_beautiful_string, \
    convert_seconds_to_beautiful_string


class FlightProcessor:
    """This class is responsible for filtering and processing
    the most important pieces of data from a flight API call"""

    def __init__(self, flight_api_call: dict or list[dict]):
        self.raw_data = flight_api_call
        self.flight_amount: int = 5
        self.data = self.raw_data.get("data") if isinstance(self.raw_data, dict) else self.raw_data
        self.flights = []
        self.__flight_data_processing()

    def __flight_data_processing(self):
        variables = {"flyFrom": "departureAirport", "flyTo": "arrivalAirport", "local_departure": "departureTime",
                     "utc_departure": "departureTimeUtc", "local_arrival": "arrivalTime",
                     "utc_arrival": "arrivalTimeUtc", "airlines": "airlines", "duration": "duration",
                     "baglimit": "luggageLimits", "bags_price": "luggagePrice", "price": "price",
                     "availability": "remainingSeats", "quality": "quality", "deep_link": "link",
                     "route": "_route"}
        for flight in self.data:
            flight_dict = {variables[key]: flight[key] for key in variables}
            seats = flight["availability"]["seats"]
            flight_dict["remainingSeats"] = 0 if seats is None else seats
            flight_dict["numberOfStops"] = len(flight["route"])
            flight_times = []
            for item in flight["route"]:
                flight_tuple = {"type": "departure", "time": item["local_departure"]}, \
                        {"type": "arrival", "time": item["local_arrival"]}
                flight_times.append(flight_tuple)
            flight_durations = analyze_layover_durations(flight_times)
            flight_dict["layoverDurations"] = flight_durations
            flight_dict["departureFormattedDateAndTime"] = beautify_date(flight_dict["departureTime"])
            flight_dict["arrivalFormattedDateAndTime"] = beautify_date(flight_dict["arrivalTime"])
            adjusted_luggage = [
                f"{key} luggage costs {value}"
                for key, value in flight_dict["luggagePrice"].items()
            ]
            flight_dict["luggagePrice"] = adjusted_luggage
            duration_seconds = int(flight_dict["duration"]["total"])
            formatted_duration_seconds = convert_seconds_to_beautiful_string(duration_seconds)
            flight_dict["flightDuration"] = formatted_duration_seconds
            flight_dict = dict(sorted(flight_dict.items()))
            # del flight_dict["duration"]
            del flight_dict["_route"]
            self.flights.append(flight_dict)


def get_flight_data_example() -> list[dict]:
    api_data = kiwi_call_example()
    fp = FlightProcessor(api_data)
    return fp.flights


def __main():
    flight_data = kiwi_call_example()
    fp = FlightProcessor(flight_data)
    flight = fp.flights[0]
    return


if __name__ == "__main__":
    __main()
