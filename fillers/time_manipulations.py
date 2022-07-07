import random
from datetime import timedelta


def random_normal_number(mean, std_dev):
    return round(random.gauss(mean, std_dev))


def random_time(start, end):
    hour = random.randint(start, end)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"


def sum_time(time1, time2):
    hour1, minute1 = time1.split(":")
    hour2, minute2 = time2.split(":")
    hour = int(hour1) + int(hour2)
    minute = int(minute1) + int(minute2)
    if minute >= 60:
        hour += 1
        minute -= 60
    if hour >= 24:
        hour -= 24
    return f"{hour:02d}:{minute:02d}"


def time_to_seconds(time):
    hour, minute = time.split(":")
    return int(hour) * 3600 + int(minute) * 60


def seconds_to_time(seconds):
    hour = seconds // 3600
    minute = (seconds % 3600) // 60
    return f"{hour:02d}:{minute:02d}"


def random_date():
    day = random.randint(1, 31)
    month = random.randint(1, 12)
    year = random.randint(2022, 2023)
    return f"{day:02d}/{month:02d}/{year:04d}"


def sum_days(date, days):
    day, month, year = date.split("/")
    day = int(day)
    month = int(month)
    year = int(year)
    day += days
    if day > 31:
        month += 1
        day = day - 31
    if month > 12:
        year += 1
        month -= 12
    return f"{day:02d}/{month:02d}/{year:04d}"


def timedelta_format(td: timedelta):
    s = td.seconds
    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}"


def seconds_to_hours_and_minutes(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}"


def __main():
    test = 11400
    print(seconds_to_hours_and_minutes(test))


if __name__ == "__main__":
    __main()
