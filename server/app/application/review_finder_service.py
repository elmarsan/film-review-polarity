from typing import Optional
from domain.review_dto import ReviewDTO
from domain.review_query_repository import ReviewQueryRepository


class ReviewFinderService:
    """ReviewFinderService defines service for find records in review table"""

    def __init__(self, query_repository: ReviewQueryRepository):
        self.query_repository = query_repository


    def find_by_id(self, id: int) -> Optional[ReviewDTO]:
        review = self.query_repository.find_by_id(id)
        return review.to_review_dto()


    def find_all(self) -> list[ReviewDTO]:
        review_list = self.query_repository.find_all()
        return  [review.to_review_dto() for review in review_list]

