from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from webscrapping.base_scrapper import BaseScrapper
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions

from webscrapping.date_tools import strip_date


class SkyscannerScrapper:
    def __init__(self):
        self.firefox = BaseScrapper()
        self.firefox.load_website("https://www.skyscanner.com.br/")

    def query_ticket(self):
        self.input_destination("Rio de Janeiro")
        self.input_origin_date("18/10/2022", direction="depart")
        self.input_origin_date("25/10/2022", direction="return")
        return 0

    def input_destination(self, origin_name: str):
        destination_box_xpath = "//input[@id='fsc-destination-search']"
        destination_box = self.firefox.driver.find_element(by="xpath", value=destination_box_xpath)
        destination_box.send_keys(origin_name)
        suggestion_list_xpath = "//li[@data-suggestion-index='0']"
        wait = WebDriverWait(self.firefox.driver, 10)
        suggestion_list = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, suggestion_list_xpath)))
        suggestion_list.click()

    def input_origin_date(self, origin_date: str, direction: str = "depart"):
        day, month, year = origin_date.split("/")
        month_tag = strip_date(origin_date)
        origin_button_xpath = f"//button[@id='{direction}-fsc-datepicker-button']"
        origin_button = self.firefox.driver.find_element(by="xpath", value=origin_button_xpath)
        origin_button.click()
        origin_select_box_xpath = f"//select[@id='{direction}-calendar__bpk_calendar_nav_select']"
        origin_select_box = self.firefox.driver.find_element(by="xpath", value=origin_select_box_xpath)
        dropdown = Select(origin_select_box)
        dropdown_options = {key.text: key for key in dropdown.options}
        chosen_option = dropdown_options[month_tag]
        chosen_option.click()
        day_table_xpath = "//table[@class='BpkCalendarGrid_bpk-calendar-grid__NzIzO " \
                          "FlightDatepicker_fsc-datepicker__list-size__YTg0M'] "
        day_table = self.firefox.driver.find_element(by="xpath", value=day_table_xpath)
        rows_dict = {int(item.text): item for item in day_table.find_elements(by="tag name", value="td")}
        desired_day = rows_dict[int(day)]
        desired_day.click()


def __main():
    ss = SkyscannerScrapper()
    ss.query_ticket()


if __name__ == "__main__":
    __main()
