from deprecated.database.postgres.runners.postgres_database_runner import PostgresRunner


class PostgresFlightTables:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name = "FlightQuery"

    def list_all_tables(self):
        sql = "SELECT * FROM information_schema.tables WHERE table_schema='public';"
        self.db.run_sql_query(sql)
        query_res = self.db.show_query_results()[0]
        query_res = [x if x is not None else '' for x in query_res]
        return [table.lower() for table in query_res if table]

    def existing_table(self, input_table_name: str):
        all_tables = self.list_all_tables()
        return input_table_name in all_tables

    def create_flight_query_table(self):
        if self.existing_table(self.table_name):
            print(f"Could not create {self.table_name} because that table already exists")
            return
        sql = f'create table {self.table_name} (id serial primary key, fly_from varchar(20), fly_to varchar(20), ' \
              'date_from varchar(20), date_to varchar(20), query_limit INT, query_name varchar(20))'
        self.db.run_sql_query(sql)

    def delete_flight_query_table(self):
        sql = f"drop table {self.db.table_name}"
        self.db.run_sql_query(sql)


def __main():
    db = PostgresRunner()
    pgt = PostgresFlightTables(db)
    pgt.create_flight_query_table()


if __name__ == "__main__":
    __main()
