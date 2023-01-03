import os

from firebase_admin.auth import EmailAlreadyExistsError, UserNotFoundError, UserRecord, PhoneNumberAlreadyExistsError

from firebase_data.firebase_connection import FirebaseCore


class FirebaseUserCrud:
    def __init__(self, input_firebase_app: FirebaseCore):  # sourcery skip: use-named-expression
        self.app = input_firebase_app
        self.auth = self.app.auth
        self.db = self.app.db
        no_existing_users = self.no_existing_users()
        if no_existing_users:
            self._create_dummy_user()
        self.__set_env_credentials()
        self.user = self._authenticate_using_email_and_password()

    def create_user(self, email: str = "test@example.com", password: str = "123456", name: str = "TestUser",
                    phone_number: str = "+11234567890", custom_claims=None) -> dict:
        if custom_claims is None:
            custom_claims = {"is_admin": False}
        if " " in name:
            return {"output": "error", "outputDetails": f"Name cannot contain spaces. Please adjust [{name}]"}
        try:
            return self._create_new_firebase_user(email, password, name, phone_number, custom_claims)
        except EmailAlreadyExistsError:
            return {"output": "error", "outputDetails": f"User {email} already exists"}
        except PhoneNumberAlreadyExistsError:
            return {"output": "error", "outputDetails": f"Phone number {phone_number} already exists"}
        except ValueError as ve:
            return {"output": "error", "outputDetails": f"ValueError: {ve}"}

    def _create_dummy_user(self) -> dict:
        return self.create_user(email="test@test.com", password="123456", name="TestUser", phone_number="+11234567890",
                                custom_claims=None)

    def _create_new_firebase_user(self, email: str, password: str, name: str, phone_number: str, custom_claims: dict) \
            -> dict:
        self.app.auth.create_user(email=email, password=password, display_name=name, phone_number=phone_number)
        self.auth.generate_email_verification_link(email)
        user = self.get_single_user(email)["outputDetails"]
        user_details = {"name": name, "phone_number": phone_number, "email": email, "unique_id": user.uid}
        for key, value in custom_claims.items():
            self.auth.set_custom_user_claims(user.uid, {key: value})
        user_details["custom_claims"] = custom_claims
        self.app.db.reference(f"user_data/{name}").set(user_details)
        return {"output": "success", "outputDetails": f"User {email} created successfully"}

    def __set_env_credentials(self):
        self.credential_email = os.environ["FIREBASE_DUMMY_LOGIN"]
        self.credential_password = os.environ["FIREBASE_DUMMY_PASSWORD"]

    def _authenticate_using_email_and_password(self) -> UserRecord:
        email = self.credential_email
        password = self.credential_password
        return self.auth.get_user_by_email(email)

    def _get_user_data_by_display_name(self, display_name: str):
        return self.db.reference(f"user_data/{display_name}").get()

    def get_single_user(self, email: str) -> dict:
        try:
            return {"output": "success", "outputDetails": self.auth.get_user_by_email(email)}
        except UserNotFoundError:
            return {"output": "error", "outputDetails": f"User {email} not found"}

    def get_all_users(self) -> dict:
        users = []
        page = self.auth.list_users()
        while page:
            users.extend(page.users)
            page = page.get_next_page()
        return {"output": "success", "outputDetails": users}

    def existing_user(self, email: str) -> bool:
        try:
            self.auth.get_user_by_email(email)
            return True
        except UserNotFoundError:
            return False

    def reset_password(self, input_email: str) -> dict:
        existing_user = self.existing_user(input_email)
        if not existing_user:
            return {"output": "error", "outputDetails": f"User {input_email} not found"}
        user_output = self.get_single_user(input_email)
        user = user_output["outputDetails"]
        self.auth.generate_password_reset_link(user.email)
        return {"output": "success", "outputDetails": f"Password reset link sent to {user.email}"}

    def delete_user(self, input_email: str) -> dict:
        existing_user = self.existing_user(input_email)
        if not existing_user:
            return {"output": "error", "outputDetails": f"User {input_email} not found"}
        user = self.get_single_user(input_email)["outputDetails"]
        user_unique_id = user.uid
        self.auth.delete_user(user_unique_id)
        return {"output": "success", "outputDetails": f"User {input_email} deleted successfully"}

    def delete_all_users(self) -> dict:
        users = self.get_all_users()["outputDetails"]
        for user in users:
            self.auth.delete_user(user.uid)
        return {"output": "success", "outputDetails": "All users deleted successfully"}

    def no_existing_users(self) -> bool:
        users = self.get_all_users()["outputDetails"]
        return not users

    def update_user(self, user_email: str, new_info: dict):
        user = self.get_single_user(user_email)["outputDetails"]
        user_unique_id = user.uid
        self.auth.update_user(user_unique_id, **new_info)
        return {"output": "success", "outputDetails": f"User {user_email} updated successfully"}


def __main():
    fc = FirebaseCore()
    fba = FirebaseUserCrud(fc)
    fba.update_user("testing@purpose.com", {"display_name": "TestingPurpose23"})
    # fba.delete_all_users()
    # all_users = fba.get_all_users()
    # fba.delete_user("test@example.com")
    # aux = fba.create_dummy_user()
    return


if __name__ == "__main__":
    __main()
