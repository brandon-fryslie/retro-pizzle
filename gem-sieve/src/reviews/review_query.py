
# Find this on the google search page

# https://www.google.com/search?q=syphon+filter+3+ps1+review

# data-attrid="kc:/cvg/computer_videogame:reviews"

# Only works w/ newer platforms :/
import os
import re
import sys
import time
from pprint import pprint
from typing import Optional, List

from googlesearch import search

import utils
import soup_helper
from reviews.review_collection import ReviewCollection
from roms.rom_collection import RomCollection
from logs import error_log, info_log
from extractors import gamefaqs, gamespot, google_search_page

def query_other_reviews(query: str):
    # print(f"Getting results for Google search: {query}")
    search_results = search(query, num_results=15, lang="en")

    # dedupe
    search_results = list(set(search_results))

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

    soup = soup_helper.bs_query(url)

    google_reviews = google_search_page.extract_google_reviews(url, soup)

    info_log(f"Querying for other reviews")
    other_review_results = query_other_reviews(f"{title} {platform} review")

    all_reviews = google_reviews + other_review_results
    if len(all_reviews) == 0:
        return None

    return ReviewCollection(google_reviews + other_review_results)

def query_roms(platform: str):

    # load the list from the rom-lists files

    rom_lists_dir = os.path.abspath("../../rom-lists")
    rom_list_path = f"{rom_lists_dir}/rom-list-{platform}.txt"
    logs_dir = os.path.abspath("../../logs")

    if not os.path.exists(rom_list_path):
        error_log(f"ERROR: No rom list created for platform {platform}")
        sys.exit(1)

    rom_titles = utils.read_file(rom_list_path).split('\n')

    info_log(f"INFO: Querying reviews for {len(rom_titles)} roms for platform {platform}")

    rom_scores = {}

    # /// Single rom for testing ///

    # single_rom_title = "Goal!"
    # single_rom_platform = "nes"
    # score_result = query_for_score(single_rom_title, single_rom_platform)
    #
    # if score_result is None:
    #     error_log("Could not find any reviews!")
    #
    # print(f"!!! got score result for {single_rom_title} ({platform})")
    # pprint(score_result)
    # for review in score_result.reviews:
    #     info_log(f"- {review.score} [{review.source}] ({review.url}) [{review.type}]")
    #
    # return

    # /// Single rom for testing ///

    no_review_roms = []
    err_msgs = []
    try:
        for rom_title in rom_titles:
            info_log(f"Querying Google for Review: {rom_title} ({platform})")
            score_result = query_for_score(rom_title, platform)

            if score_result is None:
                error_log(f"\nCould not find reviews for game: {rom_title} ({platform})\n")
                no_review_roms.append(f"{rom_title} ({platform})")
            else:
                info_log(f"""\
                
===
Title: {rom_title}""")

                for review in score_result.reviews:
                    info_log(f"- {review.score} [{review.source}] ({review.url}) [{review.type}]")

                info_log("===\n")

            time.sleep(.2)
    except Exception as e:
        error_log("GOT AN UNKNOWN ERROR.  Continuing anyway")
        error_log(str(e))
        err_msgs.append(str(e))

    utils.write_file(f"{logs_dir}/{platform}-no-review-roms.txt", "\n".join(no_review_roms))
    utils.write_file(f"{logs_dir}/{platform}-errors.log", "\n".join(err_msgs))
