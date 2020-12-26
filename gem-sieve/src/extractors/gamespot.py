from pprint import pprint
from typing import List

from bs4 import BeautifulSoup

import soup_helper
from reviews.review import Review
from logs import info_log

# TODO: get entire score breaking down including
# number of reviews, etc.  maybe create a separate review for each of them
def extract_user(url: str, soup: BeautifulSoup):
    """

    :param base_url: The URL for the title (game) on GameSpot, e.g., https://www.gamespot.com/games/the-lawnmower-man/reviews/
    :return:
    """
    user_score = soup.select_one(".reviewObject__userAvg dd a").text.strip()

    pprint(user_score)

    reviews = []
    review = Review(f"{user_score}/10", url=url, source="GameSpot", type="user")
    reviews.append(review)

    pprint(reviews)

    return reviews

# this is prolly mostly useless
def extract_metacritc(url: str, soup: BeautifulSoup):
    """

    :param base_url: The URL for the title (game) on GameSpot, e.g., https://www.gamespot.com/games/the-lawnmower-man/reviews/
    :return:
    """
    score_el = soup.select_one(".reviewObject__metacritic dd")

    if score_el.text.strip() == "--":
        return []

    score = score_el.text.strip()

    reviews = []
    review = Review(f"{score}/10", url=url, source="GameSpot", type="metacritic")
    reviews.append(review)

    return reviews


def extract(url) -> List[Review]:
    # reviewObject__metacritic
    info_log(f"Extracting from GameSpot url: {url}")
    all_reviews = []
    soup = soup_helper.bs_query(url)
    all_reviews += extract_user(url, soup)
    all_reviews += extract_metacritc(url, soup)
    return all_reviews
