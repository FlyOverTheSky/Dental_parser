import selenium.common.exceptions
from pprint import pprint

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from chrome_create_and_configurate import chrome_configuration

SITE_URL = "https://averon-td.ru/"


def parse_names_and_prices(to_search: str, return_items_count: int) -> str:
    """Базовая парсинговая функция возвращающая имя и цены."""
    # запсукаем бразер с сайтом пробахилы.рф
    browser = chrome_configuration()
    browser.get(SITE_URL)
    # ищем форму поиска и вводим наименование
    find_button = browser.find_element(
        By.XPATH,
        "/html/body/div[4]/div[4]/div[1]/div[3]/div[3]/div/button"
    )
    find_button.click()

    find_form = browser.find_element(
        By.ID,
        "title-search-input"
    )
    browser.implicitly_wait(10)
    find_form.send_keys(to_search)
    find_form.submit()

    confirm_to_search_button = browser.find_element(
        By.XPATH,
        "/html/body/div[6]/div/div/form/div[2]/button"
    )

    # находим результаты поиска на странице.
    find_results = browser.find_element(
        By.XPATH,
        "/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]",
    )
    try:

        # ждем пока на страницы отобразяться результаты и записываем их в items.
        # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inner_wrap TYPE_1")))
        items = find_results.find_elements(
            By.TAG_NAME,
            "div",
        )
        # создаем массив с результатми поиска
        result = {}
        for counter in range(1, return_items_count + 1):
            try:
                current_item = items[counter]
                current_item_info = current_item.find_element(
                    By.XPATH,
                    f"/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[{counter}]/div[2]/div/div[2]"
                )
                current_item_name = current_item_info.find_element(
                    By.XPATH,
                    f'/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[{counter}]/div[2]/div/div[2]/div[1]/div[2]'
                )
                current_item_price = current_item_name.find_element(
                    By.XPATH,
                    f"/html/body/div[4]/div[6]/div[2]/div/div/div/div/div[2]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div[{counter}]/div[2]/div/div[2]/div[2]/div"
                )
                result[current_item_name.text] = current_item_price.text
            except:
                result[current_item_name.text] = 'Нет в наличии'
        return result

    # если превышено ожидание элементов поиска или не было найдено элеменетов, то возвращаем строку
    except (selenium.common.exceptions.TimeoutException, selenium.common.NoSuchElementException) as error:
        if result:
            return result
        return 'Такого наименования нет на сайте.'


if __name__ == "__main__":
    browser = chrome_configuration()
    gloves_result = parse_names_and_prices('Перчатки', 10)
    shapes_result = parse_names_and_prices('Игла', 10)

    pprint(gloves_result)
    pprint(shapes_result)
