import re
from pprint import pprint
from typing import List, Union

import statistics

import utils
from logs import info_log, error_log


class Review():

    def __init__(self, score: Union[str,float,int], url: str, source: str, type: str = "unknown"):
        self.source = source
        self.url = url
        self.type = type.lower()
        self.score = normalize_score(score)

    def __str__(self):
        return f"Review[score={self.score},url={self.url},source={self.source},type={self.type}]"

    def __repr__(self):
        return str(self)

def normalize_score(score: str):
    if "/" in score:
        score_normal = utils.convert_to_float(score) * 100
    elif "%" in score:
        match = re.search(r"(\d+)%", score)
        if match is None:
            raise ValueError(f"ERROR: Could not extract percentage from score: {score}")
        score_normal = float(match.group(1))
    else:
        error_msg = "ERROR: Could not normalize score"
        error_log(error_msg)
        error_log(score)
        raise ValueError(error_msg)
    return score_normal

