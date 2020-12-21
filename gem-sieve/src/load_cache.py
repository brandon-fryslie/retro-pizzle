import json
from pprint import pprint

from logs import info_log
from utils import get_cache_dir

def load_cache_page(file_no: int):
    cache_file_path = f"{get_cache_dir()}/giantbomb_cache_{file_no}.json"
    with open(cache_file_path, "r") as f:
        return json.load(f)

def load_cached_pages():
    # get number of cache files
    number_of_cache_files = 3
    all_loaded = []

    for i in range(1, number_of_cache_files):
        loaded_group: list = load_cache_page(i)
        for loaded in loaded_group:
            all_loaded.extend(loaded['results'])

    info_log(f"Loaded {len(all_loaded)} results")
    for result in all_loaded:
        info_log(f"{result['name']} ({result['id']}) - {result['reviews_api_url']}")

# TODO: Write the cache in a better format
# TODO: Expand the "db" to include the rating score
# TODO: use fuzzywuzzy to match the names of existing roms to names in the db
