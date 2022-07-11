from postgres.database_creation.query_crud import PostgresQueryCrud
from postgres.postgres_database_runner import PostgresRunner
from postgres.flight_query.query_table import PostgresFlightTables


class PostgresWrapper:
    def __init__(self):
        self.runner = PostgresRunner()
        self.table_handler: PostgresFlightTables = PostgresFlightTables(self.runner)
        self.table_handler.create_flight_query_table()
        self.entry_handler: PostgresQueryCrud = PostgresQueryCrud(self.runner)


def __main():
    db = PostgresWrapper()


if __name__ == "__main__":
    __main()
