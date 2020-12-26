
# Find this on the google search page

# https://www.google.com/search?q=syphon+filter+3+ps1+review

# data-attrid="kc:/cvg/computer_videogame:reviews"

# Only works w/ newer platforms :/
import re
import sys
import time
from pprint import pprint
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
from googlesearch import search

import utils
from game import review
from game.review import Review
from game.review_collection import ReviewCollection
from game.rom import Rom
from game.rom_collection import RomCollection
from logs import error_log, info_log, success_log
from extractors import gamefaqs, gamespot, google_search_page


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


def query_other_reviews(query: str):
    # print(f"Getting results for Google search: {query}")
    search_results = search(query, num_results=15, lang="en")
    results = []
    for search_result in search_results:
        # look at specific sites we can parse
        if re.search(r"gamefaqs.gamespot.com", search_result):
            gamefaqs_res = gamefaqs.extract_gamefaqs(search_result)
            results += gamefaqs_res
        elif re.search(r"www.gamespot.com", search_result):
            gamespot_res = gamespot.extract(search_result)
            results += gamespot_res

    return results

def costruct_query(title, platform):
    title_fixed = re.sub(r"[^\w]+", '+', title)
    query_res = f"?q={title_fixed}+{platform}+review"
    return query_res


def query_for_score(title: str, platform: str) -> Optional[ReviewCollection]:
    base_url = "https://www.google.com/search"
    query = costruct_query(title, platform)

    url = f"{base_url}{query}"

    info_log(f"Querying for Google top-level reviews at url: {url}")

    soup = utils.bs_query(url)

    google_reviews = google_search_page.extract_google_reviews(soup)

    info_log(f"Querying for other reviews")
    other_review_results = query_other_reviews(f"{title} {platform} review")

    all_reviews = google_reviews + other_review_results
    if len(all_reviews) == 0:
        return None

    return ReviewCollection(google_reviews + other_review_results)

def query_roms(base_roms_dir: str, platform: str):
    path = f"{base_roms_dir}/{platform}"

    rc = RomCollection(path, platform)

    # limit to a few roms for now, gotta throttle this
    # roms = rc.roms[:100]
    roms = rc.roms

    info_log(f"INFO: Querying reviews for {len(roms)} roms for platform {platform}")

    rom_scores = {}

    # /// Single rom for testing ///

    # single_rom_title = "Super Bomberman 3"
    # single_rom_platform = "snes"
    # score_result = query_for_score(single_rom_title, single_rom_platform)
    #
    # if score_result is None:
    #     error_log("Could not find any reviews!")
    #
    # print(f"!!! got score result for {single_rom_title} ({platform})")
    # pprint(score_result)
    # return

    # /// Single rom for testing ///

    no_review_roms = []
    err_msgs = []
    try:
        for rom in roms:
            info_log(f"Querying Google for Review: {rom.title} ({rom.platform})")
            score_result = query_for_score(rom.title, rom.platform)

            if score_result is None:
                error_log(f"\nCould not find reviews for game: {rom.title} ({rom.platform})\n")
                no_review_roms.append(f"{rom.title} ({rom.platform})")
            else:
                info_log(f"""\
                
    ===
    Title: {rom.title} (path: {rom.fs.path})
    Score Result: {score_result.raw_numbers()} (mean: {score_result.mean():.2f})
    ===
    """)

            time.sleep(.2)
    except Exception as e:
        error_log("GOT AN UNKNOWN ERROR.  Continuing anyway")
        error_log(str(e))
        err_msgs.append(str(e))

    utils.write_file("./no-review-roms.txt", "\n".join(no_review_roms))
    utils.write_file("./errors.log", "\n".join(err_msgs))
