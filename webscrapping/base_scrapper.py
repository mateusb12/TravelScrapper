from references.paths import geckodriver_reference
from webscrapping.geckodriver_check import check_geckodriver
from selenium.webdriver.firefox.service import Service
from selenium import webdriver


class BaseScrapper:
    def __init__(self):
        check_geckodriver()
        s = Service(str(geckodriver_reference()))
        self.driver = webdriver.Firefox(service=s)

    def load_website(self, url: str) -> None:
        self.driver.get(url)

    def __existing_driver(self) -> bool:
        return self.driver.session_id is not None

    def __close_driver(self) -> None:
        if self.__existing_driver():
            self.driver.close()

    def __del__(self) -> None:
        self.__close_driver()


def __main():
    fs = BaseScrapper()


if __name__ == "__main__":
    __main()
