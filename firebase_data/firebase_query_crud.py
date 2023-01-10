import copy

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_run import FirebaseApp
from price_monitor.flight_utils import get_formatted_today_date


class FirebaseQueryCrud:
    def __init__(self, input_app: FirebaseApp):
        self.app = input_app
        self.app.firebase_folder = "query_data"
        self.user = input_app.user
        self.query_date = get_formatted_today_date()
        self.all_queries = self._get_all_queries()

    def create_query(self, query_params: dict):
        if existing_query := self._existing_query(query_params):
            return {"output": "error", "outputDetails": "Query already exists"}
        base_dict = {"userEmail": self.user.email, "queryDate": self.query_date, **query_params}
        self.app.add_entry(base_dict)
        return {"output": "success", "outputDetails": "Query created"}

    def _get_all_queries(self):
        return self.app.get_all_entries()

    def _get_query_unique_id(self, query_params: dict):  # sourcery skip: use-next
        useless_keys = ["userEmail", "queryDate"]
        fixed_params = self.fix_dict(query_params, useless_keys)
        for unique_id, content in self.all_queries.items():
            fixed_content = self.fix_dict(content, useless_keys)
            if fixed_params == fixed_content:
                return unique_id
        return None

    def _existing_query(self, query_params: dict) -> bool:
        if self.all_queries is None:
            return False
        unique_id = self._get_query_unique_id(query_params)
        return unique_id is not None

    @staticmethod
    def fix_dict(main_dict: dict, keys_to_remove: list[str]):
        copy_dict = copy.deepcopy(main_dict)
        for key in keys_to_remove:
            copy_dict.pop(key, None)
        return {key: value for key, value in copy_dict.items() if value is not None}

    def _get_query_by_unique_id(self, unique_id: str):  # sourcery skip: use-next
        for key, value in self.all_queries.items():
            if key == unique_id:
                return value
        return None

    def get_query(self, query_params: dict):
        unique_id = self._get_query_unique_id(query_params)
        if unique_id is None:
            return {"output": "error", "outputDetails": "Query does not exist"}
        query = self._get_query_by_unique_id(unique_id)
        return {"output": "success", "outputDetails": query}

    def update_query(self, existing_query: dict, new_params: dict):
        unique_id = self._get_query_unique_id(existing_query)
        if unique_id is None:
            return {"output": "error", "outputDetails": "Query does not exist"}
        query = self._get_query_by_unique_id(unique_id)
        for key, value in new_params.items():
            query[key] = value
        self.app.update_entry_by_unique_id(unique_id, query)
        return {"output": "success", "outputDetails": "Query updated"}

    def delete_query(self, query_params: dict):
        unique_id = self._get_query_unique_id(query_params)
        if unique_id is None:
            return {"output": "error", "outputDetails": "Query does not exist"}
        self.app.delete_entry_by_unique_id(unique_id)
        return {"output": "success", "outputDetails": "Query deleted"}


def __get_query_example():
    return {"departureAirport": "FOR", "arrivalAirport": "CDG", "departureDate": "02 March 2022", "returnDate": None}


def __main():
    firebase_app = FirebaseApp()
    fqc = FirebaseQueryCrud(firebase_app)
    query = __get_query_example()
    aux = fqc.create_query(query)
    return


if __name__ == "__main__":
    __main()
