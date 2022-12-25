import random
import string
from datetime import datetime
from typing import Optional

from domain.review import Review


def random_string(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class ReviewRandomFactory:
    """ReviewRandomFactory for testing purpose"""

    @staticmethod
    def create(review: Optional[Review]) -> Review:
        if review is None:
            return Review(
                id=random.randint(0, 10),
                film_name=random_string(),
                review_name=random_string(),
                body=random_string(),
                author=random_string(),
                model_score=random.randint(0, 10),
                user_score=random.randint(0, 10),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        review.id = random.randint(0, 10),
        review.created_at = datetime.now()
        review.updated_at = datetime.now()
        return review

    @staticmethod
    def create_multiple(count: int = 10) -> list[Review]:
        return [ReviewRandomFactory.create(None) for i in range(count)]
