import logging
import math
import time
from pprint import pprint

import requests

from logs import error_log, info_log
from utils import write_cache_file

logger = logging.getLogger(__name__)

GLOBAL_LIMIT_PER_REQUEST = 100
REQUEST_PAGES_PER_CACHE_FILE = 100

def send_giantbomb_request(offset, limit):
    api_token = "6be0705e9cb70665179bb77163ef02dea86f046b"
    base_url = "https://www.giantbomb.com/api/games"

    url = base_url

    params = {
        'format': 'json',
        # 'field_list': 'id,guid,name,platform,original_game_rating,number_of_user_reviews',
        'sort': 'id=asc',
        'limit': limit,
        'offset': offset,
        'api_key': api_token,
    }

    headers = {
        'User-Agent': 'Chuck Norris',
    }

    logger.debug(f"Sending GiantBomb request to URL {url} with params {params}")

    r = requests.get(url, headers=headers, params=params)

    return print_giantbomb_request(r)

def get_next_page(page_data):
    offset = int(page_data['offset'])
    number_returned = int(page_data['number_of_page_results'])
    limit = int(page_data['limit'])
    next_offset = offset + number_returned

    print(f"Getting next page: offset: {offset}, number_returned: {page_data['number_of_page_results']}, next_offset: {next_offset}")
    return send_giantbomb_request(offset=next_offset, limit=limit)


def print_giantbomb_request(r):
    if r.status_code == 200:
        # success_log("Request succeeded!")
        pass
    else:
        error_log("Request failed")

    return r.json()

def cache_all_pages(total_result_override = None, initial_offset=0):
    info_log(f"Caching all pages!  Sending initial request (initial_offset: {initial_offset})")

    current_page = send_giantbomb_request(offset=initial_offset, limit=GLOBAL_LIMIT_PER_REQUEST)

    # loop to get all the next pages

    total_results = int(current_page['number_of_total_results'])
    results_so_far = int(current_page['number_of_page_results']) + initial_offset

    if total_result_override is not None:
        total_results = total_result_override

    # We already got the first page
    page_number = 2

    # cache file number is initial_offset
    results_per_cache_file = GLOBAL_LIMIT_PER_REQUEST * REQUEST_PAGES_PER_CACHE_FILE
    cache_file_number = math.ceil(initial_offset / results_per_cache_file)

    print(f"using initial cache file number {cache_file_number}")


    pages = [current_page]

    info_log(f"Looping to get all pages.  Total results: {total_results}")

    while (results_so_far < total_results):
        info_log(f"Getting page {page_number}. Results so far: {results_so_far}")

        current_page = get_next_page(current_page)

        results_so_far += int(current_page['number_of_page_results'])

        pages.append(current_page)

        if len(pages) >= REQUEST_PAGES_PER_CACHE_FILE:
            # write the cache file
            info_log(f"Writing giantbomb cache file #{cache_file_number}")
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

