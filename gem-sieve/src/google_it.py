
# Find this on the google search page

# https://www.google.com/search?q=syphon+filter+3+ps1+review

# data-attrid="kc:/cvg/computer_videogame:reviews"

# Only works w/ newer platforms :/
import re
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
from extractors import gamefaqs

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

def extract_google_reviews(el: BeautifulSoup) -> Optional[ReviewCollection]:
    # Search for
    # #search
    # Who is it?  <h3 class="zBAuLc"><div class="BNeawe vvjwJb AP7Wnd">Syphon Filter 3 for PlayStation Reviews - Metacritic</div></h3>
    # rating itself: <span class="r0bn4c rQMQod">Rating</span> <span class="r0bn4c rQMQod tP9Zud"> <span aria-hidden="true" class="Eq0J8 oqSTJd">6.5/10</span>

    # ignore who the review is from.  just grab whatever

    # regex = re.compile(r".*(?:[\d.]+\/[\d.]+|\d+%).*")
    regex = re.compile(r"[\d.]+\/[\d.]+|\d+%")
    score_candidate_els = el.find_all("span", text=regex)

    if not check_soup(score_candidate_els):
        return None

    def _check_candidate(item):
        try:
            review.normalize_score(item)
            return True
        except ValueError:
            return False

    scores = [score for score in score_candidate_els if _check_candidate(score.text)]

    if len(scores) == 0:
        return None

    reviews = [Review(score_el.text) for score_el in scores]

    return ReviewCollection(reviews)

def query_other_reviews(query: str):
    print(f"Getting results for Google search: {query}")
    search_results = search(query, num_results=15, lang="en")
    results = []
    for search_result in search_results:
        # look at specific sites we can parse
        if re.search(r"gamefaqs.gamespot.com", search_result):
            gamefaqs_res = gamefaqs.extract_gamefaqs(search_result)
            results.append(gamefaqs_res)

    return results

def costruct_query(title, platform):
    title_fixed = re.sub(r"[^\w]+", '+', title)
    query_res = f"?q={title_fixed}+{platform}+review"
    return query_res


def query_for_score(title: str, platform: str) -> Optional[ReviewCollection]:
    base_url = "https://www.google.com/search"
    query = costruct_query(title, platform)

    url = f"{base_url}{query}"

    info_log(f"Querying google at url: {url}")

    soup = utils.bs_query(url)

    # print(soup.prettify())

    google_reviews = extract_google_reviews(soup)

    if google_reviews is None:
        # query elsewhere
        other_review_results = query_other_reviews(f"{title} {platform} review")
        print("!!! got other review results")
        pprint(other_review_results)

    return google_reviews

def query_snes_roms():
    # todo load snes roms from folders
    # pass folder paths in as arguments

    BASE_ROMS_DIR = "/Volumes/roms"

    platform = "psx"

    path = f"{BASE_ROMS_DIR}/{platform}"

    rc = RomCollection(path, platform)

    # limit to a few roms for now, gotta throttle this
    roms = rc.roms[:20]

    # info_log(f"INFO: Querying for {roms} roms")

    rom_scores = {}

    score_result = query_for_score("Flintstones The The Treasure of Sierra Madrock", "snes")

    print("!!! got score result for flintstones")
    pprint(score_result)

    return


    for rom in roms:
        info_log(f"Querying Google for Review: {rom.title} ({rom.platform})")
        score_result = query_for_score(rom.title, rom.platform)

        rom_scores[rom]
        if score_result is None:
            info_log(f"Could not find easy score result on google for game: {rom.title} ({rom.platform})")
        else:
            info_log(f"""\
            
===
Title: {rom.title} (path: {rom.fs.path})
Score Result: {score_result.raw_numbers()} (mean: {score_result.mean():.2f})
===
""")

        time.sleep(1)
