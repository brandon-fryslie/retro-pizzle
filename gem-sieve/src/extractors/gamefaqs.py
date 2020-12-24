import re

import utils
from game.review import Review
from logs import info_log, error_log

def extract_user(base_url: str):
    """

    :param base_url: The base URL for the title (game) on gamefaqs, e.g. https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock
    :return:
    """

    url = f"{base_url}/reviews"
    soup = utils.bs_query(url)

    # Only extracts user scores
    # TODO: extract critic scores
    scores = soup.select(".review_score")

    reviews = []
    for score in scores:
        info_log(f"Extracted gamefaqs User scores: {score.text}")
        review = Review(f"{score.text}/10", "GameFaqs", "user")
        reviews.append(review)

    return reviews

def extract_gamefaqs(url: str):
    "Extract reviews from GameFaqs"
    # First, get rid of specific review on URL so we find the game
    # https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock/reviews/45764
    # ->
    # https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock/reviews
    match = re.match(r"(https://gamefaqs\.gamespot\.com/.*)/?(?:reviews|critic)/?.*$", url)
    if match is None:
        error_log(f"Could not match URL: {url}")

    extracted_url = match.group(1)

    info_log(f"Got URL match {extracted_url}")

    # reviews = Review(score, )
    reviews = extract_user(extracted_url)

    # pprint(soup.prettify())

    return reviews
