from firebase_admin.auth import EmailAlreadyExistsError, UserNotFoundError

from firebase_data.firebase_run import FirebaseApp


class FirebaseUserCrud:
    def __init__(self):  # sourcery skip: use-named-expression
        self.app = FirebaseApp()
        self.auth = self.app.auth
        no_existing_users = self.no_existing_users()
        if no_existing_users:
            self.create_dummy_user()

    def create_user(self, email: str = "test@example.com", password: str = "123456", name: str = "TestUser",
                    phone_number: str = "+11234567890", admin: bool = False) -> dict:
        if " " in name:
            return {"output": "error", "outputDetails": f"Name cannot contain spaces. Please adjust [{name}]"}
        try:
            return self._create_new_firebase_user(email, password, name, phone_number, admin)
        except EmailAlreadyExistsError:
            print("User already exists")
            return {"output": "error", "outputDetails": f"User {email} already exists"}

    def create_dummy_user(self) -> dict:
        return self.create_user(email="test@test.com", password="123456", name="TestUser", phone_number="+11234567890",
                                admin=True)

    def _create_new_firebase_user(self, email: str, password: str, name: str, phone_number: str, admin: bool) -> dict:
        self.app.auth.create_user(email=email, password=password, display_name=name, phone_number=phone_number)
        self.auth.generate_email_verification_link(email)
        user = self.get_single_user(email)["outputDetails"]
        user_details = {"name": name, "phone_number": phone_number, "email": email, "unique_id": user.uid,
                        "is_admin": admin}
        self.app.db.reference(f"user_data/{name}").set(user_details)
        return {"output": "success", "outputDetails": f"User {email} created successfully"}

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


def __main():
    fba = FirebaseUserCrud()
    all_users = fba.get_all_users()
    # fba.delete_user("test@example.com")
    aux = fba.create_dummy_user()
    return


if __name__ == "__main__":
    __main()
