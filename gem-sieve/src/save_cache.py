import logging
import time
from pprint import pprint

import requests

from logs import error_log, info_log
from utils import write_cache_file

logger = logging.getLogger(__name__)

GLOBAL_LIMIT_PER_REQUEST = 100
REQUEST_PAGES_PER_CACHE_FILE = 100

def send_gamespot_request(offset, limit):
    api_token = "9026db69bd804fbff5fb73fb91e380601bc1dfdb"
    api_token_postfix = f"?api_key={api_token}"
    gamespot_url = "http://www.gamespot.com/api/games"

    url = f"{gamespot_url}/{api_token_postfix}"

    params = {
        'format': 'json',
        # 'field_list': 'id,genres,upc,name,platform,upc,reviews_api_url',
        'sort': 'id=asc',
        'limit': limit,
        'offset': offset,
    }

    headers = {
        'User-Agent': 'Chuck Norris',
    }

    logger.debug(f"Sending GameSpot request to URL {url} with params {params}")

    r = requests.get(url, headers=headers, params=params)

    return print_gamespot_request(r)

def get_next_page(page_data):
    offset = int(page_data['offset'])
    number_returned = int(page_data['number_of_page_results'])
    limit = int(page_data['limit'])
    next_offset = offset + number_returned

    print(f"Getting next page: offset: {offset}, number_returned: {page_data['number_of_page_results']}, next_offset: {next_offset}")
    return send_gamespot_request(offset=next_offset, limit=limit)


def print_gamespot_request(r):
    if r.status_code == 200:
        # success_log("Request succeeded!")
        pass
    else:
        error_log("Request failed")

    return r.json()

def cache_all_pages():
    info_log(f"Caching all pages!  Sending initial request")

    current_page = send_gamespot_request(offset=0, limit=GLOBAL_LIMIT_PER_REQUEST)

    # loop to get all the next pages

    total_results = int(current_page['number_of_total_results'])
    results_so_far = int(current_page['number_of_page_results'])

    # We already got the first page
    page_number = 2
    cache_file_number = 1

    pages = [current_page]

    info_log(f"Looping to get all pages.  Total results: {total_results}")

    while (results_so_far < total_results):
        info_log(f"Getting page {page_number}. Results so far: {results_so_far}")

        current_page = get_next_page(current_page)

        results_so_far += int(current_page['number_of_page_results'])

        pages.append(current_page)

        # write to the cache file
        if len(pages) >= REQUEST_PAGES_PER_CACHE_FILE:
            # write the cache file
            info_log(f"Writing cache file #{cache_file_number}")
            write_cache_file(cache_file_number, pages)
            pages = []
            cache_file_number += 1

        page_number += 1

        time.sleep(.2)


    # Write one more cache file to get any stragglers
    if len(pages) > 0:
        info_log(f"Found some stragglers.  Writing final cache file #{cache_file_number}")
        write_cache_file(cache_file_number, pages)
        pages = []

