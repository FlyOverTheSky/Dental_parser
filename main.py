import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

OBJECTS_COUNT = 5


browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
ChromeOptions = webdriver.ChromeOptions()
# Отключаем все расширения Хрома
ChromeOptions.add_argument("--disable-extensions")
# Отключаем звук в браузере
ChromeOptions.add_argument("--mute-audio")

# Обход блокировки парсинга
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
     "source": """
          const newProto = navigator.__proto__
          delete newProto.webdriver
          navigator.__proto__ = newProto
          """
    })

browser.get("https://xn--80abwmlfh7b4c.xn--p1ai/")
find_form = browser.find_element(
    By.XPATH,
    "/html/body/header/div[1]/div[2]/div/form/input"
)
find_form.send_keys("Перчатки")
find_button = browser.find_element(
    By.XPATH,
    "/html/body/header/div[1]/div[2]/div/form/button"
)
WebDriverWait(browser, 10).until(EC.element_to_be_clickable(find_button)).click()

find_results = browser.find_element(
    By.XPATH,
    "/html/body/main/div/div/div/div[3]/div[2]",
)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "products__item")))
items = find_results.find_elements(
    By.TAG_NAME,
    "div",
)
for counter in range(OBJECTS_COUNT):
    current_item = items[counter]
    item_name = current_item.find_element(
        By.XPATH,
        f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/a/span[2]/span[1]"
    )
    item_price = current_item.find_element(
        By.XPATH,
        f"/html/body/main/div/div/div/div[3]/div[2]/div[{counter + 1}]/div[2]/form/div[3]/div[1]"
    )
    print(item_name.text, item_price.text)