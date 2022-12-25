from typing import Optional
from domain.review_query_repository import ReviewQueryRepository
from domain.review_command_repository import ReviewCommandRepository
from domain.review import Review
from .review_random_factory import ReviewRandomFactory


class MockReviewQueryRepository(ReviewQueryRepository):
    """MockReviewQueryRepository testing implementation of ReviewQueryRepository"""

    def find_all(self) -> list[Review]:
        return ReviewRandomFactory.create_multiple()

    def find_by_id(self, id: int) -> Optional[Review]:
        return ReviewRandomFactory.create(None)


class MockReviewCommandRepository(ReviewCommandRepository):
    """MockReviewCommandRepository testing implementation of ReviewCommandRepository"""

    def insert(self, review: Review) -> Review:
        return ReviewRandomFactory.create(review)

    def set_user_score(self, review: Review, score: float) -> Review:
        review.user_score = score
        return review
