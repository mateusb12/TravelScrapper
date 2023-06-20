import pytest
import requests as requests
import unittest.mock

from apis.api_consumer.kiwi_api_call import kiwi_call, kiwi_call_example, kiwi_call_sp_example


def test_kiwi_call_returns_valid_json():
    # Arrange
    fly_from = "FOR"
    fly_to = "RIO"
    date_from = "01/01/2023"
    date_to = "01/03/2023"
    limit = 500

    # Act
    response = kiwi_call(fly_from=fly_from, fly_to=fly_to, date_from=date_from, date_to=date_to, limit=limit)

    # Assert
    assert isinstance(response, dict)
    assert "data" in response
    assert "currency" in response



