import fix_imports_sys
from firebase_data.firebase_factory import FirebaseFactory


def singleton(cls):
    _instances = {}

    def getinstance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return getinstance


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
