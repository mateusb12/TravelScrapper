import pytest

from firebase_data.firebase_connection import FirebaseCore
from firebase_data.firebase_user_crud import FirebaseUserCrud


@pytest.fixture(scope="module")
def get_user_crud_instance():
    fc = FirebaseCore()
    return FirebaseUserCrud(fc)


@pytest.mark.search_prices(order=1)
def test_create_user(get_user_crud_instance):
    """Test that the create_user method creates a new user in Firebase with the specified email, password,
     name, phone number, and custom claims"""
    firebase_crud = get_user_crud_instance
    firebase_crud.delete_user("testing@purpose.com")
    data = {"email": "testing@purpose.com", "password": "testing_purpose", "name": "TestingPurpose",
            "phone": "+11234567891", "custom_claim": {"admin": True}}
    result = firebase_crud.create_user(email=data["email"], password=data["password"], name=data["name"],
                                       phone_number=data["phone"], custom_claims=data["custom_claim"])
    assert result["output"] == "success"


@pytest.mark.search_prices(order=2)
def test_create_user_already_exists(get_user_crud_instance):
    """Test that the create_user method returns an error if a user with the specified email already exists
    in Firebase"""
    firebase_crud = get_user_crud_instance
    data = {"email": "testing@purpose.com", "password": "123456", "name": "TestingPurposeRepeated",
            "phone": "+11278567890", "custom_claim": {"admin": True}}
    result = firebase_crud.create_user(email=data["email"], password=data["password"], name=data["name"],
                                       phone_number=data["phone"], custom_claims=data["custom_claim"])
    assert result["output"] == "error"


@pytest.mark.search_prices(order=3)
def test_create_user_name_with_spaces(get_user_crud_instance):
    """Test that the create_user method returns an error if the name parameter contains spaces"""
    firebase_crud = get_user_crud_instance
    data = {"email": "testing2@purpose.com", "password": "123456", "name": "Testing Purpose",
            "phone": "+11248567890", "custom_claim": {"admin": True}}
    result = firebase_crud.create_user(email=data["email"], password=data["password"], name=data["name"],
                                       phone_number=data["phone"], custom_claims=data["custom_claim"])
    assert result["output"] == "error"


@pytest.mark.search_prices(order=4)
def test_create_user_phone_already_exists(get_user_crud_instance):
    """Test that the create_user method returns an error if a user with the specified phone number already
    exists in Firebase"""
    firebase_crud = get_user_crud_instance
    data = {"email": "testing3@purpose.com", "password": "123456789", "name": "TestingPurpose",
            "phone": "+11234567891", "custom_claim": {"admin": True}}
    result = firebase_crud.create_user(email=data["email"], password=data["password"], name=data["name"],
                                       phone_number=data["phone"], custom_claims=data["custom_claim"])
    assert result["output"] == "error"


@pytest.mark.search_prices(order=5)
def test_create_user_invalid_phone(get_user_crud_instance):
    """Test that the create_user method returns an error if the phone number parameter is not a valid"""
    firebase_crud = get_user_crud_instance
    data = {"email": "testing3@purpose.com", "password": "123456789", "name": "TestingPurpose",
            "phone": "123456", "custom_claim": {"admin": True}}
    result = firebase_crud.create_user(email=data["email"], password=data["password"], name=data["name"],
                                       phone_number=data["phone"], custom_claims=data["custom_claim"])
    assert result["output"] == "error"


@pytest.mark.search_prices(order=6)
def test_get_user(get_user_crud_instance):
    """Test that the get_user method returns the correct user data for the specified user"""
    firebase_crud = get_user_crud_instance
    result = firebase_crud.get_single_user("testing@purpose.com")
    user = result["outputDetails"]
    comparison_dict = {"email": "testing@purpose.com", "name": "TestingPurpose",
                       "phone": "+11234567891", "custom_claim": {"admin": True}}
    user_dict = {"email": user.email, "name": user.display_name, "phone": user.phone_number,
                 "custom_claim": user.custom_claims}
    assert user_dict == comparison_dict


@pytest.mark.search_prices(order=7)
def test_update_user(get_user_crud_instance):
    """Test that the update_user method updates the specified user's data in Firebase"""
    firebase_crud = get_user_crud_instance
    email = "testing@purpose.com"
    new_data = {"display_name": "NewBeautifulName"}
    result = firebase_crud.update_user(email, new_data)
    true_data_result = firebase_crud.get_single_user(email)
    true_data = true_data_result["outputDetails"]
    assert result["output"] == "success"
    assert true_data.display_name == "NewBeautifulName"
    new_data["display_name"] = "TestingPurpose"
    firebase_crud.update_user(email, new_data)


@pytest.mark.search_prices(order=8)
def test_delete_user(get_user_crud_instance):
    """Test that the delete_user method deletes the specified user from Firebase"""
    firebase_crud = get_user_crud_instance
    result = firebase_crud.delete_user("testing@purpose.com")
    assert result["output"] == "success"


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
