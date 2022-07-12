from postgres.postgres_database_runner import PostgresRunner


class PostgresTableCreation:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name, self.table_format = None, None

    def set_table_name(self, table_name: str):
        self.table_name: str = table_name
        self.table_format: dict = self.get_table_format(table_name)

    def list_all_tables(self):
        sql = "SELECT * FROM information_schema.tables WHERE table_schema='public';"
        self.db.run_sql_query(sql)
        query_res = self.db.show_query_results()
        if not query_res:
            return []
        query_res = [x if x is not None else '' for x in query_res][0]
        return [table.lower() for table in query_res if table]

    def existing_table(self, input_table_name: str):
        all_tables = self.list_all_tables()
        return input_table_name.lower() in all_tables

    @staticmethod
    def get_flight_table_format():
        return {'id': 'serial primary key', 'price': 'INT', 'quality': 'INT', 'cityFrom': 'varchar(20)',
                'cityTo': 'varchar(20)', 'departure': 'varchar(20)', 'arrival': 'varchar(20)',
                'dateDeparture': 'varchar(20)', 'dateArrival': 'varchar(20)', 'flightDuration': 'varchar(20)',
                'directFlight': 'boolean', 'flightDurationSeconds': 'INT', 'longLayover': 'BOOL',
                'seatsAvailable': 'INT', 'connection_1': 'varchar(20)', 'connection_2': 'varchar(20)',
                'connection_3': 'varchar(20)', 'link': 'varchar(1000)', 'flight_tag': 'varchar(20)'}

    @staticmethod
    def get_flight_query_format():
        return {'id': 'serial primary key', 'fly_from': 'varchar(20)', 'fly_to': 'varchar(20)',
                'date_from': 'varchar(20)', 'date_to': 'varchar(20)', 'query_limit': 'INT',
                'query_name': 'varchar(20)'}

    def get_table_format(self, table_tag: str):
        if table_tag.lower() == "flightdata":
            return self.get_flight_table_format()
        elif table_tag.lower() == "flightquery":
            return self.get_flight_query_format()

    def generate_sql_query(self, core_format: dict) -> str:
        header = f'create table {self.table_name} '
        body = "("
        for key, value in core_format.items():
            body += f'{key} {value}, '
        body = f"{body[:-2]});"
        return header + body

    def create_table(self):
        if self.existing_table(self.table_name):
            print(f"Could not create {self.table_name} because that table already exists")
            return
        t_format = self.table_format
        full_sql = self.generate_sql_query(t_format)
        self.db.run_sql_query(full_sql)
        print(f"Table {self.table_name} created successfully with keys = {t_format.keys()}")

    def delete_table(self):
        if not self.existing_table(self.table_name):
            print(f"[{self.table_name}] table does not exist. Impossible to delete it.")
            return
        sql = f"drop table {self.table_name}"
        self.db.run_sql_query(sql)
        print(f"Table {self.table_name} was deleted.")


def __get_pgt():
    db = PostgresRunner()
    return PostgresTableCreation(db)


def __create_all_tables():
    pgt = __get_pgt()
    table_names = ["FlightData", "FlightQuery"]
    for table in table_names:
        pgt.set_table_name(table)
        # pgt.delete_table()
        pgt.create_table()


def __list_all_tables():
    pgt = __get_pgt()
    print(pgt.list_all_tables())


def __main():
    # __list_all_tables()
    __create_all_tables()


if __name__ == "__main__":
    __main()
