from typing import Any

from database.fillers.data_skeleton import get_rio_example
from database.postgres.database_manipulation.db_creation.sql_lines_generator import get_sql_line_create
from database.postgres.runners.postgres_database_runner import PostgresRunner


class PostgresQueryCrud:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name = "FlightQuery"

    def __post_init__(self):
        self.query_amount = len(self.list_all_queries())

    def list_all_queries(self) -> list[dict[Any, Any]]:
        sql = f"select * from {self.table_name}"
        self.db.run_sql_query(sql)
        raw_results = self.db.show_query_results()
        return [self.jsonify_results(item) for item in raw_results]

    def existing_query(self, query_dict: dict) -> bool:
        input_query_name: str = str(query_dict["query_name"])
        input_query_name = input_query_name.lower()
        all_queries = self.list_all_queries()
        if not all_queries:
            return False
        all_tags = [item["query_name"] for item in all_queries]
        return input_query_name in all_tags

    def jsonify_results(self, result_tuple: tuple):
        keys = list(self.get_query_example().keys())
        values = result_tuple[1:]
        return dict(zip(keys, values))

    @staticmethod
    def get_query_example() -> dict:
        return get_rio_example()

    # def get_sql_line_create(self, values: tuple):
    #     columns = list(self.get_query_example().keys())
    #     column_str = "".join(f"{item}, " for item in columns)[:-2]
    #     header = f"insert into {self.table_name} ({column_str}) values ("
    #     for value in values:
    #         header += f"'{value}', " if isinstance(value, str) else f"{value}, "
    #     return f"{header[:-2]});"

    def flight_query_create(self, query_dict: dict) -> bool:
        if self.existing_query(query_dict):
            return False
        dict_example = self.get_query_example()
        values = tuple(query_dict.values())
        table_name = self.table_name
        full_sql = get_sql_line_create(dict_example, values, table_name)
        self.db.run_sql_query(full_sql)
        return True

    def flight_query_read(self, input_tag: str) -> bool or list:
        query_dict = {'query_name': input_tag}
        if not self.existing_query(query_dict):
            return False
        sql = f"select * from {self.table_name} where query_name='{input_tag}'"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()

    def flight_query_update(self, query_dict: dict) -> bool:
        if not self.existing_query(query_dict):
            return False
        query_name = query_dict["query_name"]
        sql = f"update {self.table_name} " \
              f"set fly_from='{query_dict['fly_from']}', fly_to='{query_dict['fly_to']}', " \
              f"date_from='{query_dict['date_from']}', date_to='{query_dict['date_to']}'," \
              f"query_limit={query_dict['query_limit']} WHERE query_name='{query_name}'"
        self.db.run_sql_query(sql)
        return True

    def flight_query_delete(self, input_tag: str) -> bool:
        query_dict = {'query_name': input_tag}
        if not self.existing_query(query_dict):
            return False
        sql = f"delete from {self.table_name} where query_name='{input_tag}'"
        self.db.run_sql_query(sql)
        return True


def __main():
    pgr = PostgresRunner()
    pfe = PostgresQueryCrud(pgr)
    ex = pfe.get_query_example()
    pfe.flight_query_create(ex)
    # pfe.flight_query_delete("fortaleza_rio")
    # print(pfe.flight_query_read("fortaleza_rio"))
    # print(pfe.flight_query_read(get_rio_example()))
    print(pfe.list_all_queries())


if __name__ == "__main__":
    __main()
