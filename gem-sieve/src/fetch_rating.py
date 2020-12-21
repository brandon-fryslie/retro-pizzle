import logging
from pprint import pprint

import requests

from save_cache import print_gamespot_request

logger = logging.getLogger(__name__)

def send_gamespot_request(url, offset, limit):
    api_token = "9026db69bd804fbff5fb73fb91e380601bc1dfdb"

    params = {
        'format': 'json',
        # 'field_list': 'id,genres,upc,name,platform,upc,reviews_api_url',
        'sort': 'id=asc',
        'limit': limit,
        'offset': offset,
        'api_key': api_token,
    }

    headers = {
        'User-Agent': 'Chuck Norris',
    }

    logger.debug(f"Sending GameSpot request to Reviews URL {url} with params {params}")

    r = requests.get(url, headers=headers, params=params)

    return print_gamespot_request(r)

def fetch_rating():
    url = "https://www.gamespot.com/api/reviews/?filter=association%3A5000-84"
    r = send_gamespot_request(url, offset=0, limit=100)
    print("got response for review")
    pprint(r)
