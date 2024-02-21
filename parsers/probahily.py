import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from parsers.models import Parser
from settings import PROBAHILY_SITE_URL as SITE_URL


class ProbahilyParser(Parser):
    def __init__(self):
        super().__init__(
            company_name='Пробахилы',
            site_url=SITE_URL
        )

    def parse_names_and_prices(self, to_search: str, return_items_count: int) -> str:
        """Базовая парсинговая функция возвращающая имя и цены."""
        # запсукаем бразер с сайтом пробахилы.рф
        self.browser.get(self.site_url)

        # ищем форму поиска и вводим наименование
        find_form = self.browser.find_element(
            By.XPATH,
            "/html/body/header/div[1]/div[2]/div/form/input"
        )
        find_form.send_keys(to_search)

        # находим кнопку поиска, ждем пока она станет кликабельна и нажимаем.
        find_button = self.browser.find_element(
            By.XPATH,
            "/html/body/header/div[1]/div[2]/div/form/button"
        )
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(find_button)).click()

        # try для случая, если результатов поиска нет
        try:
            # находим результаты поиска на странице.
            find_results = self.browser.find_element(
                By.XPATH,
                "/html/body/main/div/div/div/div[3]/div[2]",
            )
            # ждем пока на страницы отобразяться результаты и записываем их в items.
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products__item")))
            items = find_results.find_elements(
                By.TAG_NAME,
                "div",
            )
        except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.TimeoutException):
            self.last_results = {to_search: f"Такого наименования нет на сайте {self.company_name}"}
            return
        # создаем массив с результатми поиска
        result = {}
        #
        for counter in range(return_items_count):
            current_item = items[counter]
            current_item_name = current_item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/a/span[2]/span[1]"
            )
            current_item_price = current_item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/div[2]/form/div[3]/div[1]"
            )

            result[current_item_name.text] = current_item_price.text
        self.last_results = result
        return
