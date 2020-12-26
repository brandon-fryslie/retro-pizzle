"""
Extracts ratings from top-level widgets on the google search page (which are scraped from other sites already)
"""
from typing import List, Optional

import re
from bs4 import BeautifulSoup

from game import review
from game.review import Review


def find_ratings(el: BeautifulSoup) -> List[str]:
    rating_els = el.find_all("span", text="Rating")
    # if not check_soup(rating_els):
    #     error_log("Could not find any ratings!")

    scores = []
    for rating_el in rating_els:
        sibling_el = rating_el.find_next("span")
        rating = sibling_el.select_one("span[aria-hidden=\"true\"]").text

        if re.search(r"%", rating):
            rating = f"{rating.replace('%', '')}/100"

        if not re.search(r"\/", rating):
            # these always seem to be out of 5?
            # if its not already a fraction, assume its /5
            rating = f"{rating}/5"

        scores.append(rating)


    return scores

def extract_google_reviews(el: BeautifulSoup) -> Optional[List[Review]]:
    # Search for
    # #search
    # Who is it?  <h3 class="zBAuLc"><div class="BNeawe vvjwJb AP7Wnd">Syphon Filter 3 for PlayStation Reviews - Metacritic</div></h3>
    # rating itself: <span class="r0bn4c rQMQod">Rating</span> <span class="r0bn4c rQMQod tP9Zud"> <span aria-hidden="true" class="Eq0J8 oqSTJd">6.5/10</span>

    # ignore who the review is from.  just grab whatever

    # regex = re.compile(r".*(?:[\d.]+\/[\d.]+|\d+%).*")
    regex = re.compile(r"[\d.]+\/[\d.]+|\d+%")
    score_candidate_els = el.find_all("span", text=regex)

    def _check_candidate(item):
        try:
            review.normalize_score(item)
            return True
        except ValueError:
            return False

    scores = [score.text for score in score_candidate_els if _check_candidate(score.text)]

    # Find more scores (TODO: make sure we don't get dupes here!)
    # This is definitely finding dupes.  need to combine the two methods of extracting google results
    # we can probably just delete the earlier stuff since find_ratings seems to find them all now
    # TODO: scores should be int/100 instead of float.  to many stupid decimals
    more_scores = find_ratings(el)

    # pprint(f"Found orig scores {scores}")
    # pprint(f"Found more scores {more_scores}")

    all_scores = scores + more_scores

    return [Review(score) for score in all_scores]
