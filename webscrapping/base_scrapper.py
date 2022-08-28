from references.paths import geckodriver_reference
from webscrapping.geckodriver_check import check_geckodriver
from selenium.webdriver.firefox.service import Service
from selenium import webdriver


class FlightScrapper:
    def __init__(self):
        check_geckodriver()
        s = Service(str(geckodriver_reference()))
        self.driver = webdriver.Firefox(service=s)
        self.match_id, self.series_id = None, None


def __main():
    fs = FlightScrapper()


if __name__ == "__main__":
    __main()
