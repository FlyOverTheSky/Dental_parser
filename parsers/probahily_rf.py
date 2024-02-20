import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def chrome_configuration(useragent_name='tester', headless=True) -> webdriver:
    """Функция для конфигурации браузера Chrome."""
    ChromeOptions = webdriver.ChromeOptions()
    # Отключаем все расширения Хрома
    ChromeOptions.add_argument("--disable-extensions")
    # Отключаем звук в браузере
    ChromeOptions.add_argument("--mute-audio")
    # Задаем юзер-агента
    ChromeOptions.add_argument("user-agent=tester")
    # Браузер работает в фоновом режиме
    if headless:
        ChromeOptions.add_argument("headless")
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=ChromeOptions,
    )
    # Обход блокировки парсинга
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
     "source": """
          const newProto = navigator.__proto__
          delete newProto.webdriver
          navigator.__proto__ = newProto
          """
    })
    return browser


def parse_names_and_prices(to_search: str, return_items_count: int) -> str:
    """Базовая парсинговая функция возвращающая имя и цены."""
    # запсукаем бразер с сайтом пробахилы.рф
    browser = create_chrome_browser()
    browser.get("https://xn--80abwmlfh7b4c.xn--p1ai/")
    find_form = browser.find_element(
        By.XPATH,
        "/html/body/header/div[1]/div[2]/div/form/input"
    )
    find_form.send_keys(to_search)
    find_button = browser.find_element(
        By.XPATH,
        "/html/body/header/div[1]/div[2]/div/form/button"
    )
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable(find_button)).click()

    find_results = browser.find_element(
        By.XPATH,
        "/html/body/main/div/div/div/div[3]/div[2]",
    )
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products__item")))
        items = find_results.find_elements(
            By.TAG_NAME,
            "div",
        )
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
    except (selenium.common.exceptions.TimeoutException, selenium.common.NoSuchElementException):
        return 'Такого наименования нет на сайте.'


def create_chrome_browser():
    browser = chrome_configuration()
    return browser


if __name__ == "__main__":
    browser = chrome_configuration()
    gloves_result = parse_names_and_prices(browser, 'Перчатки')
    shapes_result = parse_names_and_prices(browser, 'Игла')

    for r in gloves_result:
        print(r)

    for r in shapes_result:
        print(r)
