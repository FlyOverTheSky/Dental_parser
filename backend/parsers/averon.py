import selenium.common.exceptions

from selenium.webdriver.common.by import By

from backend.parsers.models import Parser
from backend.settings import AVERON_SITE_URL as SITE_URL


class AveronParser(Parser):
    def __init__(self):
        super().__init__(
            company_name='Averon',
            site_url=SITE_URL
        )

    async def parse_names_and_prices(self, to_search: str, return_items_count: int) -> str:
        """Базовая парсинговая функция возвращающая наименования и цены."""
        # запсукаем бразер с сайтом пробахилы.рф
        self.browser.get(self.site_url)
        # ищем форму поиска и вводим наименование
        find_button = self.browser.find_element(
            By.XPATH,
            "/html/body/div[4]/div[4]/div[1]/div[3]/div[3]/div/button"
        )
        find_button.click()

        find_form = self.browser.find_element(
            By.ID,
            "title-search-input"
        )
        self.browser.implicitly_wait(10)
        find_form.send_keys(to_search)
        find_form.submit()

        confirm_to_search_button = self.browser.find_element(
            By.XPATH,
            "/html/body/div[6]/div/div/form/div[2]/button"
        )

        # создаем словарь с результатми поиска
        result = {}

        # находим результаты поиска на странице.
        try:
            find_results = self.browser.find_element(
                By.XPATH,
                "/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]",
            )
            items = find_results.find_elements(
                By.TAG_NAME,
                "div",
            )
        except selenium.common.exceptions.NoSuchElementException:
            self.last_results = {to_search: f"Такого наименования нет на сайте {self.company_name}"}
            return

        for ordinal_number, item in enumerate(items):
            try:
                if ordinal_number == return_items_count:
                    break
                current_item_info = item.find_element(
                    By.XPATH,
                    f"/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div["
                    f"1]/div/div[2]/div[{ordinal_number + 1}]/div[2]/div/div[2]"
                )
                current_item_name = current_item_info.find_element(
                    By.XPATH,
                    f'/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div['
                    f'1]/div/div[2]/div[{ordinal_number + 1}]/div[2]/div/div[2]/div[1]/div[2]'
                )
                current_item_price = current_item_name.find_element(
                    By.XPATH,
                    f"/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div["
                    f"1]/div/div[2]/div[{ordinal_number + 1}]/div[2]/div/div[2]/div[2]/div"
                )
                result[current_item_name.text] = current_item_price.text
            except selenium.common.exceptions.NoSuchElementException:
                result[current_item_name.text] = 'Нет в наличии'
                continue
        result = {self.company_name: result}
        self.last_results = result
        return result
