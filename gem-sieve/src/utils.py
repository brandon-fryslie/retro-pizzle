import json
import os
from pprint import pprint

from logs import info_log


def print_response(r):
    print(f"status_code: {r['status_code']}")
    print(f"error: {r['error']}")
    print(f"number_of_total_results: {r['number_of_total_results']}")
    print(f"number_of_page_results: {r['number_of_page_results']}")
    print(f"offset: {r['offset']}")
    info_log("results:")
    pprint(r['results'])

def write_cache_file(file_no: int, pages):
    cache_file_path = f"{get_cache_dir()}/gamespot_cache_{file_no}.json"
    with open(cache_file_path, "w") as f:
        json.dump(pages, f, indent=4, sort_keys=True)

def get_cache_dir():
    cache_dir = os.path.abspath(f"./cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)
