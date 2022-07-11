import psycopg2

from postgres.credentials import get_credentials


class PostgresRunner:
    def __init__(self):
        db_dict = get_credentials()
        self.con = psycopg2.connect(host=db_dict["host"], database=db_dict["database"],
                                    user=db_dict["user"], password=db_dict["password"])
        self.cursor = self.con.cursor()
        self.table_name = "flightquery"
        self.create_flight_query_table()
        self.query_amount = len(self.list_all_queries())

    def run_sql_query(self, query: str):
        self.cursor.execute(query)
        self.con.commit()

    def show_query_results(self):
        return self.cursor.fetchall()

    def run_all_sql_queries(self, queries: list):
        return [self.run_sql_query(query) for query in queries]

    def close_con(self):
        self.con.close()
        return "Connection closed"

    def __del__(self):
        self.close_con()
        print("Connection closed")

    def list_all_tables(self):
        sql = "SELECT * FROM information_schema.tables WHERE table_schema='public';"
        self.run_sql_query(sql)
        return self.show_query_results()

    def list_all_schemas(self):
        sql = "SELECT schema_name FROM information_schema.schemata;"
        self.run_sql_query(sql)
        return self.show_query_results()

    def existing_table(self, input_table_name: str):
        all_tables = self.list_all_tables()
        return any(input_table_name.lower() in table for table in all_tables)

    def existing_query(self, query_dict: dict) -> bool:
        input_query_name = query_dict["query_name"].lower()
        all_queries = self.list_all_queries()
        return any(query["query_name"] == input_query_name for query in all_queries)

    def create_flight_query_table(self):
        if self.existing_table(self.table_name):
            print(f"Could not create {self.table_name} because that table already exists")
            return
        sql = 'create table FlightQuery (id serial primary key, fly_from varchar(20), fly_to varchar(20), ' \
              'date_from varchar(20), date_to varchar(20), query_limit INT, query_name varchar(20))'
        self.run_sql_query(sql)

    def delete_flight_query_table(self):
        sql = f"drop table {self.table_name}"
        self.run_sql_query(sql)

    def list_all_queries(self) -> list[tuple]:
        sql = f"select * from {self.table_name}"
        self.run_sql_query(sql)
        return self.show_query_results()
        # return [{'fly_from': result[1], 'fly_to': result[2], 'date_from': result[3],
        #          'date_to': result[4], 'query_limit': result[5], 'query_name': result[6]} for result in results]

    def get_flight_query_id(self, query_dict: dict):
        sql = f"select id from {self.table_name} where query_name = '{query_dict['query_name']}'"
        self.run_sql_query(sql)
        return self.show_query_results()[0][0]

    def flight_query_create(self, query_dict: dict) -> bool:
        if self.existing_query(query_dict):
            return False
        sql = f"insert into {self.table_name} values ({self.query_amount}, '{query_dict['fly_from']}'," \
              f" '{query_dict['fly_to']}', " \
              f"'{query_dict['date_from']}', '{query_dict['date_to']}', {query_dict['query_limit']}, " \
              f"'{query_dict['query_name']}') "
        self.run_sql_query(sql)
        return True

    def flight_query_read(self, query_dict: dict) -> bool or list:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"select * from {self.table_name} where id={query_id}"
        self.run_sql_query(sql)
        return self.show_query_results()

    def flight_query_update(self, query_dict: dict) -> bool:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"update {self.table_name} " \
              f"set fly_from='{query_dict['fly_from']}', fly_to='{query_dict['fly_to']}', " \
              f"date_from='{query_dict['date_from']}', date_to='{query_dict['date_to']}'," \
              f"query_limit={query_dict['query_limit']} WHERE ID={query_id}"
        self.run_sql_query(sql)
        return True

    def flight_query_delete(self, query_dict: dict) -> bool:
        if not self.existing_query(query_dict):
            return False
        query_id = self.get_flight_query_id(query_dict)
        sql = f"delete from {self.table_name} where id={query_id}"
        self.run_sql_query(sql)
        return True


def __main():
    pgr = PostgresRunner()
    aux = {"fly_from": "FOR", "fly_to": "SP", "date_from": "01/07/2022", "date_to": "01/07/2023", "query_limit": 50,
           "query_name": "fortaleza_rio"}
    a1 = pgr.existing_query(aux)
    # pgr.delete_flight_query_table()
    print(pgr.list_all_queries())
    # print(runner.list_all_schemas())
    # print(runner.existing_table("FlightQuery"))
    # print(runner.existing_table())
    # runner.create_flight_query_table()
    pgr.close_con()


if __name__ == "__main__":
    __main()
