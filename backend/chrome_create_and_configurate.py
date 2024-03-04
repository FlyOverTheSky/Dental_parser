from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def chrome_configuration(useragent_name='tester', headless=True) -> webdriver:
    """Функция для конфигурации браузера Chrome."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Отключаем все расширения Хрома
    chrome_options.add_argument("--disable-extensions")
    # Отключаем звук в браузере
    chrome_options.add_argument("--mute-audio")
    # Задаем юзер-агента
    chrome_options.add_argument("user-agent=tester")
    # Браузер работает в фоновом режиме
    if headless:
        chrome_options.add_argument("headless")
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
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