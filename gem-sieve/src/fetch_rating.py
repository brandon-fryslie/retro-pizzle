import logging
from pprint import pprint

import requests

from save_cache import print_giantbomb_request

logger = logging.getLogger(__name__)


def send_giantbomb_request(url, offset, limit):
    # giantbomb token
    api_token = "6be0705e9cb70665179bb77163ef02dea86f046b"


    params = {
        'format': 'json',
        'api_key': api_token,
    }

    headers = {
        'User-Agent': 'Chuck Norris',
    }

    logger.debug(f"Sending GiantBomb request to Reviews URL {url} with params {params}")

    r = requests.get(url, headers=headers, params=params)

    return print_giantbomb_request(r)

def fetch_rating():
    pass
