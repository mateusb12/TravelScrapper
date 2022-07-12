import unittest

from database.postgres.database_manipulation.flight_crud import PostgresFlightCrud
from database.postgres.postgres_database_runner import PostgresRunner


class PostgresFlightTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PostgresFlightTest, self).__init__(*args, **kwargs)
        self.db = PostgresFlightCrud(PostgresRunner())
        self.example = self.db.get_flight_example()
        self.db.flight_data_create(self.example)

    def test_create(self):
        creation_result = self.db.flight_data_create(self.example)
        type_test = isinstance(creation_result, bool)
        self.assertEqual(type_test, True)

    def test_read(self):
        read_result = self.db.flight_data_read("fortaleza_rio")
        type_test = isinstance(read_result, (dict, bool))
        self.assertEqual(type_test, True)

    def test_update(self):
        update_result = self.db.flight_data_update(self.example)
        type_test = isinstance(update_result, bool)
        self.assertEqual(type_test, True)

    def test_delete(self):
        delete_result = self.db.flight_data_delete("fortaleza_rio")
        type_test = isinstance(delete_result, bool)
        self.assertEqual(type_test, True)


if __name__ == '__main__':
    # db = PostgresFlightCrud(PostgresRunner())
    # example = db.get_flight_example()
    unittest.main()
