import logging, os, time, requests
from prometheus_client import CollectorRegistry, start_http_server, Info
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry

log_format = '%(asctime)s[%(filename)s:%(lineno)d][%(levelname)s] %(message)s'
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d %H:%M:%S%z', level=logging.INFO)

def get_html_bs(url:str) -> BeautifulSoup|None:

    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = s.get(url=url)
        if response.status_code == 200:
            html = response.content.decode("utf-8")
            soup = BeautifulSoup(html, 'html.parser')
            return soup
        else:
            logging.warning(f"Request HTML error url: {url} response: {response}")
            return None
    except requests.exceptions.RequestException as e:
        logging.warning(f"{url} Request HTML failed: url: {url} exception: {e}")
        return None

if __name__ == '__main__':

    logging.info("# initializing exporter...")
    registry = CollectorRegistry()
    start_http_server(int(os.environ.get('PORT', 8000)), registry=registry)

    logging.info("# create all metrics instances...")
    m = Info('aphorism', '格言をランダムに表示', registry=registry)

    while True:
        logging.info("# get aphorism...")
        soup = get_html_bs("http://www.meigensyu.com/quotations/index/random")
        meigenbox = soup.select_one("div.meigenbox")
        if meigenbox != None:
            infos = {
            'aphorism': meigenbox.select_one("div.text").text,
            'by': meigenbox.select_one("div.link > ul > li> a").text,
            }
            m.info(infos)
            logging.info("## Successfully acquired the aphorism.")
        else:
            logging.warning("## 引用が見つかりませんでした(´・ω・`)")
        time.sleep(3600*1)
