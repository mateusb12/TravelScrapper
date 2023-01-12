from firebase_admin.auth import UserRecord

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_login import FirebaseLogin
from firebase_data.firebase_query_crud import FirebaseQueryCrud
from firebase_data.firebase_run import FirebaseApp
from firebase_data.firebase_user_crud import FirebaseUserCrud


class FirebaseFactory:
    def __init__(self, email: str, password: str):
        self.core = FirebaseCore()
        self.user_crud = FirebaseUserCrud(self.core)
        self.firebase_login = FirebaseLogin(self.user_crud)
        self.firebase_login.login(email, password)
        self.user = self.firebase_login.user
        self.app = FirebaseApp(input_user=self.user, input_core=self.core)
        self.firebase_query = FirebaseQueryCrud(self.app)


def __main():
    factory = FirebaseFactory(email="test@test.com", password="123456")
    queries = factory.firebase_query.all_queries
    return


if __name__ == "__main__":
    __main()
