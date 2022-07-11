from fillers.query_examples import get_rio_example
from postgres.postgres_database_runner import PostgresRunner


class PostgresFlightEntries:
    def __init__(self, db: PostgresRunner):
        self.db = db
        self.table_name = "flightquery"
        self.query_amount = len(self.list_all_queries())

    def list_all_queries(self) -> list[tuple]:
        sql = f"select * from {self.table_name}"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()

    def existing_query(self, query_dict: dict) -> bool:
        input_query_name = query_dict["query_name"].lower()
        all_queries = self.list_all_queries()
        all_tags = [item[-1] for item in all_queries]
        return input_query_name in all_tags

    def get_flight_query_id(self, query_dict: dict):
        sql = f"select id from {self.table_name} where query_name = '{query_dict['query_name']}'"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()[0][0]

    def flight_query_create(self, query_dict: dict) -> bool:
        if self.existing_query(query_dict):
            return False
        sql = f"insert into {self.table_name} values ({self.query_amount}, '{query_dict['fly_from']}'," \
              f" '{query_dict['fly_to']}', " \
              f"'{query_dict['date_from']}', '{query_dict['date_to']}', {query_dict['query_limit']}, " \
              f"'{query_dict['query_name']}') "
        self.db.run_sql_query(sql)
        return True

    def flight_query_read(self, query_dict: dict) -> bool or list:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"select * from {self.table_name} where id={query_id}"
        self.db.run_sql_query(sql)
        return self.db.show_query_results()

    def flight_query_update(self, query_dict: dict) -> bool:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"update {self.table_name} " \
              f"set fly_from='{query_dict['fly_from']}', fly_to='{query_dict['fly_to']}', " \
              f"date_from='{query_dict['date_from']}', date_to='{query_dict['date_to']}'," \
              f"query_limit={query_dict['query_limit']} WHERE ID={query_id}"
        self.db.run_sql_query(sql)
        return True

    def flight_query_delete(self, query_dict: dict) -> bool:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"delete from {self.table_name} where id={query_id}"
        self.db.run_sql_query(sql)
        return True


def __main():
    pgr = PostgresRunner()
    pfe = PostgresFlightEntries(pgr)
    print(pfe.flight_query_read(get_rio_example()))


if __name__ == "__main__":
    __main()
