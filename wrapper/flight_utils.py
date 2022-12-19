from datetime import datetime, timedelta
from typing import List, Tuple, Dict


def analyze_layover_durations(flights: List[Tuple[Dict[str, str], Dict[str, str]]]) -> List[timedelta]:
    waiting_times = []
    time_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    for index, flight in enumerate(flights):
        if index == len(flights) - 1:
            break
        current_arrival = datetime.strptime(flight[1]["time"], time_format)
        next_departure = datetime.strptime(flights[index + 1][0]["time"], time_format)
        # Check if the current flight and the next flight are on the same day
        if current_arrival.date() != next_departure.date():
            # If the flights are not on the same day, adjust the current_arrival time to be the same day
            # as the next_departure time
            current_arrival = current_arrival.replace(year=next_departure.year, month=next_departure.month,
                                                      day=next_departure.day)
        waiting_time = next_departure - current_arrival
        # Check if the waiting time is negative, indicating that the layover spans multiple days
        if waiting_time.total_seconds() < 0:
            # If the waiting time is negative, add a day to the current_arrival time and re-calculate the waiting time
            current_arrival += timedelta(days=1)
            waiting_time = next_departure - current_arrival
        waiting_times.append(waiting_time)
    return waiting_times


def beautify_date(date_string: str):
    # Parse the date string and create a datetime object
    try:
        dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError as e:
        raise ValueError('Invalid date string format') from e
    day, month, year, hour, minute = dt.day, dt.month, dt.year, dt.hour, dt.minute
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]

    # Convert the hour to the 12-hour format
    if hour == 0:
        hour = 12
        am_pm = 'AM'
    elif 1 <= hour < 12:
        am_pm = 'AM'
    elif 12 <= hour < 13:
        am_pm = 'PM'
    else:
        hour -= 12
        am_pm = 'PM'

    return f"{day}{suffix} {month_names[month]} {year} at {hour:02d}:{minute:02d} {am_pm}"


def __main():
    date = "2023-02-12T02:40:00.000"
    aux = beautify_date(date)
    return


if __name__ == "__main__":
    __main()
