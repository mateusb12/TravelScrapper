import psycopg2

from postgres.credentials import get_credentials


class PostgresRunner:
    def __init__(self):
        db_dict = get_credentials()
        self.con = psycopg2.connect(host=db_dict["host"], database=db_dict["database"],
                                    user=db_dict["user"], password=db_dict["password"])
        self.cursor = self.con.cursor()
        self.table_name = "flightquery"
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

    def create_flight_query_table(self):
        if self.existing_table(self.table_name):
            print(f"Could not create {self.table_name} because that table already exists")
            return
        sql = 'create table FlightQuery (id serial primary key, fly_from varchar(20), fly_to varchar(20), ' \
              'date_from varchar(20), date_to varchar(20), query_limit INT)'
        self.run_sql_query(sql)

    def delete_flight_query_table(self):
        sql = f"drop table {self.table_name}"
        self.run_sql_query(sql)

    def list_all_queries(self):
        sql = f"select * from {self.table_name}"
        self.run_sql_query(sql)
        return self.show_query_results()

    def insert_flight_query(self, query_dict: dict):
        sql = f"insert into {self.table_name} values ({self.query_amount}, '{query_dict['fly_from']}'," \
              f" '{query_dict['fly_to']}', " \
              f"'{query_dict['date_from']}', '{query_dict['date_to']}', {query_dict['query_limit']}) "
        self.run_sql_query(sql)

    def get_flight_query_id(self, query_dict: dict):
        sql = f"select id from {self.table_name} where fly_from = '{query_dict['fly_from']}'" \
              f" and fly_to = '{query_dict['fly_to']}' and " \
              f"date_from = '{query_dict['date_from']}' and date_to = '{query_dict['date_to']}' and " \
              f"query_limit = {query_dict['query_limit']}"
        self.run_sql_query(sql)
        return self.show_query_results()[0][0]

    def modify_flight_query(self, query_dict: dict):
        query_id = self.get_flight_query_id(query_dict)
        sql = f"update {self.table_name} " \
              f"set fly_from='{query_dict['fly_from']}', fly_to='{query_dict['fly_to']}', " \
              f"date_from='{query_dict['date_from']}', date_to='{query_dict['date_to']}'," \
              f"query_limit={query_dict['query_limit']} WHERE ID={query_id}"
        self.run_sql_query(sql)

    def delete_flight_query(self, query_dict: dict):
        query_id = self.get_flight_query_id(query_dict)
        sql = f"delete from {self.table_name} where id={query_id}"
        self.run_sql_query(sql)


# sql = 'create table cidade (id serial primary key, nome varchar(100), uf varchar(2))'
# cur.execute(sql)
# sql = "insert into cidade values (default,'São Paulo,'SP')"
# cur.execute(sql)
# con.commit()
# cur.execute('select * from cidade')
# recset = cur.fetchall()
# for rec in recset:
#     print (rec)

def __main():
    runner = PostgresRunner()
    # runner.delete_flight_query_table()
    # runner.create_flight_query_table()
    aux = {"fly_from": "FOR", "fly_to": "SP", "date_from": "01/07/2022", "date_to": "01/07/2023", "query_limit": 50}
    runner.delete_flight_query(aux)
    print(runner.list_all_queries())
    # print(runner.list_all_schemas())
    # print(runner.existing_table("FlightQuery"))
    # print(runner.existing_table())
    # runner.create_flight_query_table()
    runner.close_con()


if __name__ == "__main__":
    __main()
