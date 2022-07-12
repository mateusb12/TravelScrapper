from travel_analysis.flight import get_flight_example


def flight_dict_filler(flight_dict: dict) -> None:
    flight_dict["countryFrom"] = {"name": "Brazil"}
    flight_dict["countryTo"] = {"name": "Brazil"}
    flight_dict["duration"] = {"total": flight_dict["flightDurationSeconds"]}
    flight_dict["bags_price"] = 0
    flight_dict["availability"] = {"seats": flight_dict["seatsAvailable"]}
    route_ex = [{"local_arrival": '2022-10-21T15:15:00.000Z',
                 "local_departure": '2022-10-21T14:05:00.000Z',
                 "flight_no": 5056}]
    flight_dict["route"] = route_ex
    flight_dict["routes"] = route_ex
    flight_dict["local_arrival"] = '2022-10-06T11:25:00.000Z'
    flight_dict["local_departure"] = '2022-10-06T11:25:00.000Z'
    flight_dict["deep_link"] = flight_dict["link"]


def __main():
    flight = get_flight_example()


if __name__ == "__main__":
    __main()
