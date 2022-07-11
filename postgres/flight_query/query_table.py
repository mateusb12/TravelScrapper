from postgres.postgres_database_runner import PostgresRunner


class PostgresFlightTables:
    def __init__(self, db: PostgresRunner):
        self.db = db

    def list_all_tables(self):
        sql = "SELECT * FROM information_schema.tables WHERE table_schema='public';"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()

    def existing_table(self, input_table_name: str):
        all_tables = self.list_all_tables()
        return any(input_table_name.lower() in table for table in all_tables)

    def create_flight_query_table(self):
        if self.existing_table(self.db.table_name):
            print(f"Could not create {self.db.table_name} because that table already exists")
            return
        sql = 'create table FlightQuery (id serial primary key, fly_from varchar(20), fly_to varchar(20), ' \
              'date_from varchar(20), date_to varchar(20), query_limit INT, query_name varchar(20))'
        self.db.run_sql_query(sql)

    def delete_flight_query_table(self):
        sql = f"drop table {self.db.table_name}"
        self.db.run_sql_query(sql)


def __main():
    db = PostgresRunner()
    db.create_flight_query_table()
    # db.delete_flight_query_table()


if __name__ == "__main__":
    __main()
