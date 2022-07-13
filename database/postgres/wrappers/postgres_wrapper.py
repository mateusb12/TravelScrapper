from database.postgres.database_manipulation.flight_crud import PostgresFlightCrud
from database.postgres.database_manipulation.query_crud import PostgresQueryCrud
from database.postgres.database_manipulation.table_creation import PostgresTableCreation
from database.postgres.runners.postgres_database_runner import PostgresRunner


class PostgresWrapper:
    def __init__(self):
        self.runner = PostgresRunner()
        self.table_names = ["FlightData", "FlightQuery"]
        self.table_handler: PostgresTableCreation = PostgresTableCreation(self.runner)
        self.flight_handler = PostgresFlightCrud(self.runner)
        self.query_handler = PostgresQueryCrud(self.runner)

    def refresh_db(self):
        self.delete_all_tables()
        self.create_all_tables()
        self.register_first_filler()

    def create_all_tables(self):
        for table in self.table_names:
            self.table_handler.set_table_name(table)
            self.table_handler.create_table()

    def delete_all_tables(self):
        for table in self.table_names:
            self.table_handler.set_table_name(table)
            self.table_handler.delete_table()

    def register_first_filler(self):
        flight_example = self.flight_handler.get_flight_example()
        self.flight_handler.flight_data_create(flight_example)


def __main():
    db = PostgresWrapper()
    db.refresh_db()


if __name__ == "__main__":
    __main()
