from datetime import datetime, timedelta
from typing import List, Tuple, Dict


def analyze_layover_durations(flights: List[Tuple[Dict[str, str], Dict[str, str]]]) -> List[str]:
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
    return convert_timedelta_list_to_beautiful_string(waiting_times)


def convert_timedelta_list_to_beautiful_string(timedelta_list: list[timedelta]):
    formatted_list = []

    for td in timedelta_list:
        total_seconds = td.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_list.append(f"{int(hours)} hours {int(minutes)} min")
    return formatted_list


def convert_seconds_to_beautiful_string(seconds: int) -> str:
    # Convert amount of seconds to a format like "5h45min"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h{minutes}min"


def get_formatted_today_date():
    today_date = datetime.now()
    return today_date.strftime("%d %B %Y")


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


def get_date_tuple(date_string: str) -> Tuple[int, int, int]:
    month_map = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                 "September": 9, "October": 10, "November": 11, "December": 12}
    date_parts = date_string.split()
    year = int(date_parts[2])
    month = month_map[date_parts[1]]
    day = int(date_parts[0])
    return year, month, day


def reorder_flight_data_node_by_date(flight_data: dict) -> dict:
    sorted_dates = sorted(flight_data.keys(), key=get_date_tuple, reverse=True)
    return {date: flight_data[date] for date in sorted_dates}


def convert_html_date(input_html_date: str):
    """This function converts a date like '2023-01-01' to '01 'January 2023' format"""
    year, month, day = input_html_date.split('-')
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return f"{day} {month_names[int(month)]} {year}"


def __main():
    aux = beautify_date("2022-01-01")
    return


if __name__ == "__main__":
    __main()
