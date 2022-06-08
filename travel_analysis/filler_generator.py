import random


def random_number(mean, std_dev):
    return round(random.gauss(mean, std_dev), 2)


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
    return f"{hour:02d}:{minute:02d}"


def time_to_seconds(time):
    hour, minute = time.split(":")
    return int(hour) * 3600 + int(minute) * 60


class FillerGenerator:
    def __init__(self, city_from: str = "London", city_to: str = "Madrid"):
        self.price = random_number(126.78, 21.63)
        self.quality = random_number(299.40, 102.42)
        self.departure = random_time(8, 18)
        self.flight_duration = random_time(2, 10)
        self.arrival = sum_time(self.departure, self.flight_duration)
        self.flight_duration_seconds = time_to_seconds(self.flight_duration)
        self.seats_available = random_number(3.008333, 2.027110)




