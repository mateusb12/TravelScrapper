from webscrapping.base_scrapper import BaseScrapper


class SkyscannerScrapper:
    def __init__(self):
        self.firefox = BaseScrapper()
        self.firefox.load_website("https://www.skyscanner.com.br/")

    def query_ticket(self):
        origin_box_xpath = "//input[@id='fsc-origin-search']"
        destination_box_xpath = "//input[@id='fsc-destination-search']"
        origin_date_box_xpath = "//button[@id='depart-fsc-datepicker-button']"
        destination_date_box_xpath = "//button[@id='return-fsc-datepicker-button']"
        origin_box = self.firefox.driver.find_element(by="xpath", value=origin_box_xpath)
        destination_box = self.firefox.driver.find_element(by="xpath", value=destination_box_xpath)
        origin_date = self.firefox.driver.find_element(by="xpath", value=origin_date_box_xpath)
        destination_date = self.firefox.driver.find_element(by="xpath", value=destination_date_box_xpath)
        destination_box.send_keys("Rio de Janeiro")
        origin_date.click()
        month_dropdown_xpath = "//div[@class='BpkCalendarNav_bpk-calendar-nav__month__NzMzZ']"
        all_months = self.firefox.driver.find_element(by="xpath", value=month_dropdown_xpath)
        # destination_date.send_keys("2022-12-10")
        return 0


def __main():
    ss = SkyscannerScrapper()
    ss.query_ticket()


if __name__ == "__main__":
    __main()
