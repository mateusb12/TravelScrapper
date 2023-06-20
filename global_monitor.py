from firebase_data.firebase_factory import FirebaseFactory
from utils.singleton_pattern import singleton


@singleton
class GlobalFlightMonitor:
    def __init__(self):
        email = "test@test.com"
        password = "123456"
        self.factory: FirebaseFactory = FirebaseFactory()
        self.factory.run(email, password)


def monitor_all_users():
    gfm = GlobalFlightMonitor()
    monitor = gfm.factory.firebase_monitor
    monitor.search_prices()
    return


def __main():
    monitor_all_users()


if __name__ == "__main__":
    __main()
