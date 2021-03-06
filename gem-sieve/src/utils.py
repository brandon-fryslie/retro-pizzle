import json
import os
import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

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
    cache_file_path = f"{get_cache_dir()}/giantbomb_cache_{file_no}.json"
    with open(cache_file_path, "w") as f:
        json.dump(pages, f, indent=4, sort_keys=True)

def get_cache_dir():
    dir = os.path.abspath(f"./giantbomb_cache")
    os.makedirs(dir, exist_ok=True)
    return dir

def get_results_dir() -> str:
    dir = os.path.abspath(f"./giantbomb_results")
    os.makedirs(dir, exist_ok=True)
    return dir

def write_file(path, content) -> None:
    with open(path, "w") as f:
        f.write(content)

def read_file(path) -> str:
    with open(path, "r") as f:
        return f.read()

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        num, denom = (num.strip(), denom.strip())
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0

        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac
