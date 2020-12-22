import json
import time
from pprint import pprint

from logs import info_log
from utils import get_cache_dir

def load_cache_page(file_no: int):
    cache_file_path = f"{get_cache_dir()}/giantbomb_cache_{file_no}.json"
    with open(cache_file_path, "r") as f:
        return json.load(f)



def load_cached_pages():
    # get number of cache files
    number_of_cache_files = 8
    all_loaded = []

    for i in range(1, number_of_cache_files + 1):
        loaded_group: list = load_cache_page(i)
        info_log(f"Loading cache page #{i}.  {len(loaded_group)} requests in this page")
        for loaded in loaded_group:
            all_loaded.extend(loaded['results'])

    info_log(f"Loaded {len(all_loaded)} results")
    for result in all_loaded:
        if result['number_of_user_reviews'] > 0:
            info_log(f"{result['name']} ({result['site_detail_url']}) - # Reviews: {result['number_of_user_reviews']}")

    time.sleep(600)
# TODO: Write the cache in a better format
# TODO: Expand the "db" to include the rating score
# TODO: use fuzzywuzzy to match the names of existing roms to names in the db
