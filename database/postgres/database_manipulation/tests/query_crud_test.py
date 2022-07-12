import unittest

from database.postgres.database_manipulation.query_crud import PostgresQueryCrud
from database.postgres.runners.postgres_database_runner import PostgresRunner


class PostgresCrudTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PostgresCrudTest, self).__init__(*args, **kwargs)
        self.db = PostgresQueryCrud(PostgresRunner())
        self.example = self.db.get_query_example()
        self.db.flight_query_create(self.example)

    def test_create(self):
        creation_result = self.db.flight_query_create(self.example)
        type_test = isinstance(creation_result, bool)
        self.assertEqual(type_test, True)

    def test_read(self):
        read_result = self.db.flight_query_read("fortaleza_rio")
        type_test = isinstance(read_result, (dict, bool))
        self.assertEqual(type_test, True)

    def test_update(self):
        update_result = self.db.flight_query_update(self.example)
        type_test = isinstance(update_result, bool)
        self.assertEqual(type_test, True)

    def test_delete(self):
        delete_result = self.db.flight_query_delete("fortaleza_rio")
        type_test = isinstance(delete_result, bool)
        self.assertEqual(type_test, True)


if __name__ == '__main__':
    unittest.main()
