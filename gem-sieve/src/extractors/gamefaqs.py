import re
from pprint import pprint
from typing import List

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
        # info_log(f"Extracted gamefaqs User scores: {score.text}")
        review = Review(f"{score.text}/10", "GameFaqs", "user")
        reviews.append(review)

    return reviews

def parse_review_text(text: str) -> Review:
    """
    Parse the review text from the html element
    """
    regex = re.compile(r"\s+([\d.]+\s+?\/\s+?[\d.]+) -- (.*)")
    match = regex.match(text)
    if match is None:
        error_log(f"ERROR: Could not extract review from text: {text}")

    review_score = match.group(1).strip()
    review_source = match.group(2).strip()

    return Review(review_score, source=review_source, type="critic")

def extract_critic(base_url: str):
    """

    :param base_url: The base URL for the title (game) on gamefaqs, e.g. https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock
    :return:
    """

    url = f"{base_url}/critic"
    soup = utils.bs_query(url)

    # these are some of the reviews.  others are in a link
    critic_scores = soup.select(".reviews_critic .info .name")

    return [parse_review_text(s.text) for s in critic_scores]

def extract_gamefaqs(url: str) -> List[Review]:
    "Extract reviews from GameFaqs"
    # First, get rid of specific review on URL so we find the game
    # https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock/reviews/45764
    # ->
    # https://gamefaqs.gamespot.com/snes/588341-the-flintstones-the-treasure-of-sierra-madrock/reviews
    match = re.match(r"(https://gamefaqs\.gamespot\.com/.*)/?(?:reviews|critic)?/?.*$", url)
    if match is None:
        error_log(f"Could not match URL: {url}")

    extracted_url = match.group(1)

    # info_log(f"Got URL match {extracted_url}")

    user_reviews = extract_user(extracted_url)
    critic_reviews = extract_critic(extracted_url)

    reviews = user_reviews + critic_reviews

    return reviews
