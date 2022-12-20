import psycopg2

from tokens.token_loader import get_postgres_credentials


class PostgresRunner:
    def __init__(self):
        db_dict = get_postgres_credentials()
        self.con = psycopg2.connect(host=db_dict["host"], database=db_dict["database"],
                                    user=db_dict["user"], password=db_dict["password"])
        self.cursor = self.con.cursor()
        self.table_name = "flightquery"

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

    def list_all_schemas(self):
        sql = "SELECT schema_name FROM information_schema.schemata;"
        self.run_sql_query(sql)
        return self.show_query_results()


def __main():
    pgr = PostgresRunner()
    aux = {"fly_from": "FOR", "fly_to": "SP", "date_from": "01/07/2022", "date_to": "01/07/2023", "query_limit": 50,
           "query_name": "fortaleza_rio"}
    a1 = pgr.existing_query(aux)
    print(pgr.list_all_queries())
    pgr.close_con()


if __name__ == "__main__":
    __main()
