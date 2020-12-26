from pprint import pprint

import requests
import time
from bs4 import BeautifulSoup


def ensure_soup(el):
    if el is None:
        raise RuntimeError("ERROR: No soup for you!  Query was None")

    if len(el) == 0:
        raise RuntimeError("ERROR: No soup for you!  No results in query")

def check_soup(el):
    if el is None:
        return False

    if len(el) == 0:
        return False

    return True


def bs_query(url) -> BeautifulSoup:
    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    }

    # get data
    r = requests.get(url, headers = headers)

    # sleep so hopefully we don't get banned
    time.sleep(.2)

    pprint(r.content)

    # parsing html
    return BeautifulSoup(r.content, features='lxml')

