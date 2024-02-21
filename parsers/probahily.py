import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from chrome_create_and_configurate import chrome_configuration
from settings import PROBAHILY_SITE_URL as SITE_URL


def parse_names_and_prices(to_search: str, return_items_count: int) -> str:
    """Базовая парсинговая функция возвращающая имя и цены."""
    # запсукаем бразер с сайтом пробахилы.рф
    browser = chrome_configuration(headless=True)
    browser.get(SITE_URL)
    # ищем форму поиска и вводим наименование
    find_form = browser.find_element(
        By.XPATH,
        "/html/body/header/div[1]/div[2]/div/form/input"
    )
    find_form.send_keys(to_search)
    find_form.submit()
    # # находим кнопку поиска, ждем пока она станет кликабельна и нажимаем.
    # find_button = browser.find_element(
    #     By.XPATH,
    #     "/html/body/header/div[1]/div[2]/div/form/button"
    # )
    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable(find_button)).click()
    browser.implicitly_wait(10)
    # находим результаты поиска на странице.
    find_results = browser.find_element(
        By.XPATH,
        "/html/body/main/div/div/div/div[3]/div[2]",
    )
    try:

        # ждем пока на страницы отобразяться результаты и записываем их в items.
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products__item")))
        items = find_results.find_elements(
            By.TAG_NAME,
            "div",
        )

        # создаем массив с результатми поиска
        result = [0] * return_items_count
        for counter in range(return_items_count):
            current_item = items[counter]
            item_name = current_item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/a/span[2]/span[1]"
            )
            item_price = current_item.find_element(
                By.XPATH,
                f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/div[2]/form/div[3]/div[1]"
            )

            result[counter] = (item_name.text, item_price.text)

        return result

    # если превышено ожидание элементов поиска или не было найдено элеменетов, то возвращаем строку
    except (selenium.common.exceptions.TimeoutException, selenium.common.NoSuchElementException):
        return 'Такого наименования нет на сайте.'


if __name__ == "__main__":
    browser = chrome_configuration()
    gloves_result = parse_names_and_prices('Перчатки', 10)
    shapes_result = parse_names_and_prices('Игла', 10)

    print(gloves_result)
    print(shapes_result)
