from api_consumer.kiwi_api_call import kiwi_call_example


class TravelAnalyser:
    def __init__(self, data: dict):
        self.data = data


if __name__ == "__main__":
    ta = TravelAnalyser(kiwi_call_example())
    pass

