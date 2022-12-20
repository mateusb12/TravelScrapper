from deprecated.database.fillers.time_manipulations import timedelta_format, get_today_date
from travel_analysis.flight import Flight


def get_rio_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "RIO", "date_from": "01/10/2022", "date_to": "12/12/2022",
            "query_limit": 5, "less_than": 120,
            "query_name": "fortaleza_rio"}


def get_sp_example() -> dict:
    return {"fly_from": "FOR", "fly_to": "SAO", "date_from": "01/07/2022", "date_to": "30/07/2022",
            "query_limit": 5, "less_than": 120,
            "query_name": "fortaleza_sp"}


def get_flight_dict_example():
    return {'id': 0,
            'price': 1200, 'quality': 153,
            'queryDate': '01-07-2022',
            'cityFrom': 'Fortaleza', 'cityTo': 'Rio de Janeiro',
            'departure': '14:20', 'arrival': '17:30',
            'dateDeparture': '14-10-2022', 'dateArrival': '14-10-2022',
            'flightDuration': '3:10', 'directFlight': True,
            'flightDurationSeconds': 11400,
            'longLayover': False,
            'seatsAvailable': 1,
            'connection_1': '00:00',
            'connection_2': '00:00',
            'connection_3': '00:00',
            'link': 'https://www.google.com',
            'less_than': 120,
            'flight_tag': 'fortaleza_rio'}


def get_flight_table_format():
    return {'id': 'serial primary key',
            'price': 'INT', 'quality': 'INT',
            'queryDate': 'varchar(20)',
            'cityFrom': 'varchar(20)', 'cityTo': 'varchar(20)',
            'departure': 'varchar(20)', 'arrival': 'varchar(20)',
            'dateDeparture': 'varchar(20)', 'dateArrival': 'varchar(20)',
            'flightDuration': 'varchar(20)', 'directFlight': 'boolean',
            'flightDurationSeconds': 'INT',
            'longLayover': 'BOOL',
            'seatsAvailable': 'INT',
            'connection_1': 'varchar(20)',
            'connection_2': 'varchar(20)',
            'connection_3': 'varchar(20)',
            'link': 'varchar(1000)',
            'less_than': 'INT',
            'flight_tag': 'varchar(20)',
            }


def convert_flight_to_dict(input_flight: Flight) -> dict:
    return {"price": input_flight.price, "quality": int(input_flight.quality),
            "queryDate": get_today_date(),
            "cityFrom": input_flight.flight_from, "cityTo": input_flight.flight_to,
            "departure": input_flight.time_departure, "arrival": input_flight.time_arrival,
            "dateDeparture": input_flight.date_departure, "dateArrival": input_flight.date_arrival,
            "flightDuration": input_flight.duration, "directFlight": input_flight.is_direct_flight(),
            "flightDurationSeconds": input_flight.duration_seconds,
            "longLayover": input_flight.long_layover,
            "seatsAvailable": input_flight.seats_available if input_flight.seats_available is not None else 0,
            "connection_1": timedelta_format(input_flight.connection_times[0]),
            "connection_2": timedelta_format(input_flight.connection_times[1]),
            "connection_3": timedelta_format(input_flight.connection_times[2]),
            "link": input_flight.link,
            "less_than": input_flight.less_than}


def jsonify_flight_data(input_tuple: tuple) -> dict:
    return {"id": input_tuple[0],
            "price": input_tuple[1], "quality": input_tuple[2],
            "queryDate": input_tuple[3],
            "city_from": input_tuple[4], "city_to": input_tuple[5], "departure": input_tuple[6],
            "arrival": input_tuple[7], "dateDeparture": input_tuple[8], "dateArrival": input_tuple[9],
            "flightDuration": input_tuple[10], "directFlight": input_tuple[11], "flightDurationSeconds": input_tuple[12],
            "longLayover": input_tuple[13], "seatsAvailable": input_tuple[14], "connection_1": input_tuple[15],
            "connection_2": input_tuple[16], "connection_3": input_tuple[17], "link": input_tuple[18],
            "less_than": input_tuple[19], "flight_tag": input_tuple[20]}


def get_flight_query_format():
    return {'id': 'serial primary key', 'fly_from': 'varchar(20)', 'fly_to': 'varchar(20)',
            'date_from': 'varchar(20)', 'date_to': 'varchar(20)', 'query_limit': 'INT',
            'less_than': 'INT', 'query_name': 'varchar(20)'}
