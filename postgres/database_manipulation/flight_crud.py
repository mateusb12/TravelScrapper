from postgres.database_manipulation.sql_lines_generator import generate_sql_update_line, \
    get_sql_line_create
from postgres.postgres_database_runner import PostgresRunner


class PostgresFlightCrud:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name = "FlightData"

    def __post_init__(self):
        self.query_amount = len(self.list_all_flights())

    def list_all_flights(self) -> list[tuple]:
        sql = f"select * from {self.table_name}"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()

    def existing_flight(self, query_dict: dict) -> bool:
        all_flights = self.list_all_flights()
        current_link = query_dict["link"]
        all_links = [item[-2] for item in all_flights]
        return current_link in all_links

    def jsonify_results(self, result_tuple: tuple):
        keys = list(self.get_flight_example().keys())
        values = result_tuple[1:]
        return dict(zip(keys, values))

    @staticmethod
    def get_flight_example():
        return {'price': 1200, 'quality': 153, 'cityFrom': 'Fortaleza',
                'cityTo': 'Rio de Janeiro', 'departure': '14:20', 'arrival': '17:30',
                'dateDeparture': '14-10-2022', 'dateArrival': '14-10-2022', 'flightDuration': '3:10',
                'directFlight': True, 'flightDurationSeconds': 11400, 'longLayover': False,
                'seatsAvailable': 1, 'connection_1': '0:00', 'connection_2': '0:00',
                'connection_3': '0:00', 'link': 'https://www.google.com', 'flight_tag': 'fortaleza_rio'}

    def get_keys(self):
        return list(self.get_flight_example().keys())

    def get_sql_line_create(self, values: tuple):
        columns = list(self.get_flight_example().keys())
        column_str = "".join(f"{item}, " for item in columns)[:-2]
        header = f"insert into {self.table_name} ({column_str}) values ("
        for value in values:
            header += f"'{value}', " if isinstance(value, str) else f"{value}, "
        return f"{header[:-2]});"

    def flight_data_create(self, flight_dict: dict) -> bool:
        if self.existing_flight(flight_dict):
            return False
        dict_example = self.get_flight_example()
        values = tuple(flight_dict.values())
        table_name = self.table_name
        full_sql = get_sql_line_create(dict_example, values, table_name)
        self.db.run_sql_query(full_sql)
        return True

    def flight_data_read(self, input_tag: str):
        flight_dict = {'flight_tag': input_tag.lower()}
        if not self.existing_flight(flight_dict):
            return False
        # sql = f"select * from {self.table_name} where flight_tag='{input_tag}'"
        sql = f"select * from {self.table_name}"
        self.db.run_sql_query(sql)
        res = self.db.show_query_results()[0]
        return self.jsonify_results(res)

    def flight_data_update(self, flight_dict: dict) -> bool:
        if not self.existing_flight(flight_dict):
            return False
        full_sql = generate_sql_update_line(flight_dict, self.table_name)
        self.db.run_sql_query(full_sql)
        return True

    def flight_data_delete(self, input_tag: str) -> bool:
        if not self.existing_flight({'flight_tag': input_tag.lower()}):
            return False
        sql = f"delete from {self.table_name} where flight_tag='{input_tag}'"
        self.db.run_sql_query(sql)
        return True


def __main():
    db = PostgresFlightCrud(PostgresRunner())
    db.flight_data_create(db.get_flight_example())
    # print(db.list_all_flights())
    # print(db.flight_data_read('fortaleza_rio'))
    # print(db.flight_data_update(db.get_flight_example()))
    # print(db.flight_data_delete('fortaleza_rio'))


if __name__ == "__main__":
    __main()
