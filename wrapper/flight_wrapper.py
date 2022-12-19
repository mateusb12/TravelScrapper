from apis.api_consumer.kiwi_api_call import kiwi_call


class FlightWrapper:
    def __init__(self):
        self.flight_data = kiwi_call(fly_from="FOR", fly_to="RIO", date_from="01/01/2023",
                                     date_to="01/03/2023", limit=500)


def __main():
    fw = FlightWrapper()
    return


if __name__ == "__main__":
    __main()
