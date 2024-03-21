import os
import sys

import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


sys.path.append(os.path.join(os.path.dirname(__file__),'../../'))
from backend.parsers.models import Parser
from backend.settings import PROBAHILY_SITE_URL as SITE_URL


class ProbahilyParser(Parser):
    def __init__(self):
        super().__init__(
            company_name='Пробахилы',
            site_url=SITE_URL
        )

    async def parse_names_and_prices(self, to_search: str, return_items_count: int) -> dict:
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

        # создаем словарь с результатми поиска
        result = {}

        # try для случая, если результатов поиска нет
        try:
            # находим результаты поиска на странице.
            find_results = self.browser.find_element(
                By.XPATH,
                "/html/body/main/div/div/div[3]/div[2]/div[1]",
            )
            # ждем пока на страницы отобразяться результаты и записываем их в items.
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products__item")))
            items = find_results.find_elements(
                By.TAG_NAME,
                "div",
            )
        except selenium.common.exceptions.NoSuchElementException:
            result = {
                self.company_name:
                    {
                        to_search:
                         f"Такого наименования нет на сайте {self.company_name}"
                    }
            }
            self.last_results = result
            return result

        # проходимся по items и формируем словарь для вывода
        for ordinal_number, item in enumerate(items):
            if ordinal_number == return_items_count:
                break
            current_item_name = item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div[3]/div[2]/div[1]/div[{ordinal_number + 1}]/a/span[2]/span[1]"
            )
            current_item_price = item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div[3]/div[2]/div[1]/div[{ordinal_number + 1}]/div/form/div[1]/div[1]"
            )
            result[current_item_name.text] = current_item_price.text
        result = {self.company_name: result}
        self.last_results = result
        return result
