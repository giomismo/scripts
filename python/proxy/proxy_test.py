import requests
import logging
from proxyficator import proxyficator

class socketed_or_no_socketed:
    def __init__(self, url, proxy=None):
        logging.basicConfig(filename='proxy_test.log',mode="a",level=logging.INFO,format='%(asctime)s %(levelname)s [%(name)-10s] %(process)d.%(processName)s : %(message)s')
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        log = logging.getLogger("main")
        if proxy:
            proxyficator(proxy)       
        print requests.get(url).content
        log.info("Receiving content: {}".format(requests.get(url).content))

if __name__ == "__main__":
    url = "http://ipv4.icanhazip.com"
    socketed_or_no_socketed(url)
    socketed_or_no_socketed(url, "socks5://localhost:8085")

