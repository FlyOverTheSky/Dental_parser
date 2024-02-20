from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
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