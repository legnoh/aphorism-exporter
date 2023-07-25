import os,platform,time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from prometheus_client import CollectorRegistry, start_http_server, Info

if __name__ == '__main__':

    # initialize
    print("initializing exporter...")
    registry = CollectorRegistry()
    start_http_server(int(os.environ.get('PORT', 8000)), registry=registry)

    # initialize chromium & selenium webdriver
    print("initializing chromium & selenium webdriver...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')

    # create all metrics instances
    print("create all metrics instances...")
    m = Info('aphorism', '格言をランダムに表示', registry=registry)

    ch_version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text
    if platform.system() == 'Linux':
        ch_type = ChromeType.CHROMIUM
    else:
        ch_type = ChromeType.GOOGLE
    ch_driver_manager = ChromeDriverManager(driver_version=ch_version, chrome_type=ch_type)
    if platform.system() == 'Linux':
        ch_service = ChromiumService(ch_driver_manager.install())
    else:
        ch_service = ChromeService(ch_driver_manager.install())

    while True:

        driver = webdriver.Chrome(service=ch_service)

        print("get aphorism...")
        driver.get("https://dictionary.goo.ne.jp/quote/")
        driver.implicitly_wait(10)

        try:
            quote_box = driver.find_element(By.CSS_SELECTOR, "div.content-box-quote > div.content-box-quote-in")
            infos = {
                'aphorism': quote_box.find_element(By.CSS_SELECTOR, "p:first-child").text,
                'by': quote_box.find_element(By.CSS_SELECTOR, "p:nth-child(2) > strong").text,
            }
            m.info(infos)
            print("Successfully acquired the aphorism.")

        except NoSuchElementException:
            print("WARN: 引用が見つかりませんでした(´・ω・`)")

        driver.quit()

        time.sleep(3600*1)
