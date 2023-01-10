import os

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_user_crud import FirebaseUserCrud


class FirebaseLogin:
    def __init__(self, input_user_crud: FirebaseUserCrud):
        # sourcery skip: use-named-expression
        self.__crud_user = input_user_crud
        no_existing_users = self.__crud_user.no_existing_users()
        if no_existing_users:
            self._create_dummy_user()
        self.user = None
        # self.__login_using_env_credentials()

    def _create_dummy_user(self) -> dict:
        return self.__crud_user.create_user(email="test@test.com", password="123456", name="TestUser",
                                            phone_number="+11234567890", custom_claims=None)

    def login(self, email: str, password: str):
        self.user = self.__crud_user.auth.get_user_by_email(email)

    def __login_using_env_credentials(self):
        credential_email = os.environ["FIREBASE_DUMMY_LOGIN"]
        credential_password = os.environ["FIREBASE_DUMMY_PASSWORD"]
        return self.login(credential_email, credential_password)


def __main():
    fc = FirebaseCore()
    fbc = FirebaseUserCrud(fc)
    fbl = FirebaseLogin(fbc)
    user = fbl.user
    return


if __name__ == "__main__":
    __main()
