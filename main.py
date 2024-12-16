import logging,os,time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from prometheus_client import CollectorRegistry, start_http_server, Info

log_format = '%(asctime)s[%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

if __name__ == '__main__':

    logging.info("# initializing exporter...")
    registry = CollectorRegistry()
    start_http_server(int(os.environ.get('PORT', 8000)), registry=registry)

    logging.info("# initializing chromium options...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    logging.info("# create all metrics instances...")
    m = Info('aphorism', '格言をランダムに表示', registry=registry)

    while True:
        if os.path.isfile("/.dockerenv"):
            logging.info("# start display...")
            display = Display(visible=0, size=(1024, 768))
            display.start()

        logging.info("# get aphorism...")
        driver = webdriver.Chrome(service=Service(), options=options)
        driver.implicitly_wait(0.5)
        driver.get("https://dictionary.goo.ne.jp/quote/")

        try:
            quote_box = driver.find_element(By.CSS_SELECTOR, "div.content-box-quote > div.content-box-quote-in")
            infos = {
                'aphorism': quote_box.find_element(By.CSS_SELECTOR, "p:first-child").text,
                'by': quote_box.find_element(By.CSS_SELECTOR, "p:nth-child(2) > strong").text,
            }
            m.info(infos)
            logging.info("## Successfully acquired the aphorism.")

        except NoSuchElementException:
            logging.warning("## 引用が見つかりませんでした(´・ω・`)")

        driver.quit()
        if os.path.isfile("/.dockerenv"):
            display.stop()
        time.sleep(3600*1)
