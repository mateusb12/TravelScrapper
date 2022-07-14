from database.fillers.time_manipulations import timedelta_format
from travel_analysis.flight import Flight


def get_rio_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "RIO", "date_from": "01/10/2022", "date_to": "12/12/2022", "query_limit": 5,
            "query_name": "fortaleza_rio"}


def get_sp_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "SAO", "date_from": "01/07/2022", "date_to": "30/07/2022", "query_limit": 5,
            "query_name": "fortaleza_sp"}


def get_flight_dict_example():
    return {'price': 1200, 'quality': 153, 'cityFrom': 'Fortaleza',
            'cityTo': 'Rio de Janeiro', 'departure': '14:20', 'arrival': '17:30',
            'dateDeparture': '14-10-2022', 'dateArrival': '14-10-2022', 'flightDuration': '3:10',
            'directFlight': True, 'flightDurationSeconds': 11400, 'longLayover': False,
            'seatsAvailable': 1, 'connection_1': '00:00', 'connection_2': '00:00',
            'connection_3': '00:00', 'link': 'https://www.google.com', 'flight_tag': 'fortaleza_rio'}


def get_flight_table_format():
    return {'id': 'serial primary key', 'price': 'INT', 'quality': 'INT', 'cityFrom': 'varchar(20)',
            'cityTo': 'varchar(20)', 'departure': 'varchar(20)', 'arrival': 'varchar(20)',
            'dateDeparture': 'varchar(20)', 'dateArrival': 'varchar(20)', 'flightDuration': 'varchar(20)',
            'directFlight': 'boolean', 'flightDurationSeconds': 'INT', 'longLayover': 'BOOL',
            'seatsAvailable': 'INT', 'connection_1': 'varchar(20)', 'connection_2': 'varchar(20)',
            'connection_3': 'varchar(20)', 'link': 'varchar(1000)', 'flight_tag': 'varchar(20)'}


def convert_flight_to_dict(input_flight: Flight) -> dict:
    return {"price": input_flight.price, "quality": int(input_flight.quality), "cityFrom": input_flight.flight_from,
            "cityTo": input_flight.flight_to, "departure": input_flight.time_departure, "arrival": input_flight.time_arrival,
            "dateDeparture": input_flight.date_departure, "dateArrival": input_flight.date_arrival,
            "flightDuration": input_flight.duration, "directFlight": input_flight.is_direct_flight(),
            "flightDurationSeconds": input_flight.duration_seconds,
            "longLayover": input_flight.long_layover,
            "seatsAvailable": input_flight.seats_available if input_flight.seats_available is not None else 0,
            "connection_1": timedelta_format(input_flight.connection_times[0]),
            "connection_2": timedelta_format(input_flight.connection_times[1]),
            "connection_3": timedelta_format(input_flight.connection_times[2]),
            "link": input_flight.link}


def get_flight_query_format():
    return {'id': 'serial primary key', 'fly_from': 'varchar(20)', 'fly_to': 'varchar(20)',
            'date_from': 'varchar(20)', 'date_to': 'varchar(20)', 'query_limit': 'INT',
            'query_name': 'varchar(20)'}
