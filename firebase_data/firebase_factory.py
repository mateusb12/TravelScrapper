from firebase_admin.auth import UserRecord

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_login import FirebaseLogin
from firebase_data.firebase_query_crud import FirebaseQueryCrud
from firebase_data.firebase_run import FirebaseApp
from firebase_data.firebase_user_crud import FirebaseUserCrud


def login_pipeline(email: str, password: str) -> FirebaseApp:
    fc = FirebaseCore()
    fbc = FirebaseUserCrud(fc)
    fbl = FirebaseLogin(fbc)
    fbl.login(email, password)
    user = fbl.user
    return FirebaseApp(input_user=user, input_core=fc)


def get_all_queries(app: FirebaseApp):
    fqc = FirebaseQueryCrud(app)
    return fqc.all_queries


def __main():
    app = login_pipeline(email="test@test.com", password="123456")
    queries = get_all_queries(app)
    return


if __name__ == "__main__":
    __main()
