from database.fillers.data_skeleton import get_flight_table_format, get_flight_query_format
from database.postgres.runners.postgres_database_runner import PostgresRunner


class PostgresTableCreation:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name, self.table_format = None, None

    def set_table_name(self, table_name: str):
        self.table_name: str = table_name
        self.table_format: dict = self.get_table_format(table_name)

    @staticmethod
    def clean_query_table_results(input_query_results: list):
        if input_query_results is None:
            return []
        lower_results = [x.lower() for x in input_query_results if x is not None]
        valid_results = [x for x in lower_results if x]
        trash_info = ['d62utkp249rp3q', 'public', 'base table', 'yes', 'no']
        return [x for x in valid_results if x not in trash_info][0]

    def list_all_tables(self):
        sql = "SELECT * FROM information_schema.tables WHERE table_schema='public';"
        self.db.run_sql_query(sql)
        query_res = self.db.show_query_results()
        clean_query_res = [self.clean_query_table_results(x) for x in query_res]
        if not clean_query_res:
            return []
        return clean_query_res

    def existing_table(self, input_table_name: str):
        all_tables = self.list_all_tables()
        return input_table_name.lower() in all_tables

    @staticmethod
    def get_table_format(table_tag: str):
        if table_tag.lower() == "flightdata":
            return get_flight_table_format()
        elif table_tag.lower() == "flightquery":
            return get_flight_query_format()

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

    def get_table_contents(self, table_name: str):
        sql = f"SELECT * FROM {table_name}"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()


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
    pgt = __get_pgt()
    pgt.set_table_name("flightdata")
    pgt.delete_table()
    print(pgt.get_table_contents("flightdata"))
    # __list_all_tables()
    # __create_all_tables()


if __name__ == "__main__":
    __main()
