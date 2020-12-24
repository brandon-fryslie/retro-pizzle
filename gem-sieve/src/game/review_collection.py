import statistics
from typing import List

from game.review import Review

class ReviewCollection:

    def __init__(self, reviews: List[Review]):
        self.reviews = reviews

    def raw_numbers(self):
        return [review.score for review in self.reviews]

    def mean(self):
        return statistics.mean([r.score for r in self.reviews])

    def __str__(self):
        scores = [review.score for review in self.reviews]
        return f"<Review[scores={scores} (mean: {self.mean()})]"

    def __repr__(self):
        return str(self)
