import datetime
from typing import List, Dict, Tuple

import pytest

from price_monitor.flight_utils import analyze_layover_durations, beautify_date


def get_flight_times_same_day_example() -> List[Tuple[Dict[str, str], Dict[str, str]]]:
    return [
        (
            {"type": "departure", "time": "2023-02-12T02:40:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T05:25:00.000Z"},
        ),
        (
            {"type": "departure", "time": "2023-02-12T06:05:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T07:20:00.000Z"},
        ),
        (
            {"type": "departure", "time": "2023-02-12T08:00:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T09:05:00.000Z"},
        ),
    ]


def get_flight_times_different_days_example() -> List[Tuple[Dict[str, str], Dict[str, str]]]:
    return [
        (
            {"type": "departure", "time": "2023-02-11T22:40:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T01:25:00.000Z"},
        ),
        (
            {"type": "departure", "time": "2023-02-12T06:05:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T07:20:00.000Z"},
        ),
        (
            {"type": "departure", "time": "2023-02-13T08:00:00.000Z"},
            {"type": "arrival", "time": "2023-02-12T09:05:00.000Z"},
        ),
    ]


def test_analyze_layover_durations_between_flights_returns_correct_list():
    # Arrange
    flight_times = get_flight_times_same_day_example()
    expected = [datetime.timedelta(hours=0, minutes=40), datetime.timedelta(hours=0, minutes=40)]

    # Actual
    actual = analyze_layover_durations(flight_times)

    # Assert
    assert actual == expected


def test_analyze_layover_durations_different_days_returns_correct_list():
    flight_times = get_flight_times_different_days_example()
    expected = [datetime.timedelta(hours=4, minutes=40), datetime.timedelta(hours=0, minutes=40)]

    actual = analyze_layover_durations(flight_times)
    assert actual == expected


def test_beautify_date_returns_correct_string_object():
    date = "2023-02-12T02:40:00.000Z"
    expected = '12th February 2023 at 02:40 AM'
    expected_format = str

    actual = beautify_date(date)
    actual_format = type(actual)

    assert actual == expected
    assert actual_format == expected_format


def test_beautify_date_sets_am_pm_correctly_a():
    date = "2023-02-12T00:00:00.000Z"
    expected = '12th February 2023 at 12:00 AM'

    actual = beautify_date(date)
    assert actual == expected


def test_beautify_date_sets_am_pm_correctly_b():
    date = "2022-12-19T10:00:00.000Z"
    expected = '19th December 2022 at 10:00 AM'

    actual = beautify_date(date)
    assert actual == expected


def test_beautify_date_sets_am_pm_correctly_c():
    date = "2022-12-19T22:00:00.000Z"
    expected = '19th December 2022 at 10:00 AM'

    actual = beautify_date(date)
    assert actual == expected


def test_beautify_date_handles_invalid_date():
    date = "2023-02-12T02:40:00.000"

    with pytest.raises(ValueError):
        beautify_date(date)


def __main():
    pytest.main()


if __name__ == "__main__":
    __main()
