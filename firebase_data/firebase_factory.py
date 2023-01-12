from firebase_admin.auth import UserRecord

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_login import FirebaseLogin
from firebase_data.firebase_query_crud import FirebaseQueryCrud
from firebase_data.firebase_run import FirebaseApp
from firebase_data.firebase_user_crud import FirebaseUserCrud


class FirebaseFactory:
    def __init__(self):
        self.core = None
        self.user_crud = None
        self.firebase_login = None
        self.user = None
        self.app = None
        self.firebase_query = None

    def run(self, email: str, password: str):
        self.core = FirebaseCore()
        self.user_crud = FirebaseUserCrud(self.core)
        self.firebase_login = FirebaseLogin(self.user_crud)
        self.firebase_login.login(email, password)
        self.user = self.firebase_login.user
        self.app = FirebaseApp(input_user=self.user, input_core=self.core)
        self.firebase_query = FirebaseQueryCrud(self.app)
        print("Factory successfully finished!")


def __main():
    factory = FirebaseFactory()
    factory.run("email", "password")
    queries = factory.firebase_query.all_queries
    return


if __name__ == "__main__":
    __main()
