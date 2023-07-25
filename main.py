import logging,os,platform,time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from prometheus_client import CollectorRegistry, start_http_server, Info

log_format = '%(asctime)s[%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

if __name__ == '__main__':

    logging.info("initializing exporter...")
    registry = CollectorRegistry()
    start_http_server(int(os.environ.get('PORT', 8000)), registry=registry)

    logging.info("create chrome options...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')

    logging.info("create all metrics instances...")
    m = Info('aphorism', '格言をランダムに表示', registry=registry)

    while True:
        driver_ready = False
        while driver_ready == False:
            try:
                if platform.system() == 'Linux':
                    logging.info("initializing chromium...")
                    driver = webdriver.Chrome(service=ChromiumService(), options=options)
                else:
                    logging.info("initializing chrome...")
                    driver = webdriver.Chrome(service=ChromeService(), options=options)
                driver.implicitly_wait(10)
                driver_ready = True
            except (WebDriverException) as e:
                logging.error(e)
                continue

        logging.info("get aphorism...")
        driver.get("https://dictionary.goo.ne.jp/quote/")

        try:
            quote_box = driver.find_element(By.CSS_SELECTOR, "div.content-box-quote > div.content-box-quote-in")
            infos = {
                'aphorism': quote_box.find_element(By.CSS_SELECTOR, "p:first-child").text,
                'by': quote_box.find_element(By.CSS_SELECTOR, "p:nth-child(2) > strong").text,
            }
            m.info(infos)
            logging.info("Successfully acquired the aphorism.")

        except NoSuchElementException:
            logging.warn("引用が見つかりませんでした(´・ω・`)")

        driver.quit()

        time.sleep(3600*1)
