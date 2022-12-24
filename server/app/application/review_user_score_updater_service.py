from fastapi import HTTPException
from domain.review_query_repository import ReviewQueryRepository
from domain.review_dto import ReviewDTO
from domain.review_command_repository import ReviewCommandRepository


class ReviewUserScoreUpdateService:
    """ReviewUserScoreUpdateService defines service for setting user_score column in review table"""

    def __init__(
        self,
        query_repository: ReviewQueryRepository,
        command_repository: ReviewCommandRepository
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository
    

    def update(self, review_id: int, score: float) -> ReviewDTO:
        review = self.query_repository.find_by_id(id = review_id)
        if review is None:
            raise HTTPException(status_code=404, detail="Review not found {}".format(id))

        self.command_repository.set_user_score(review, score)
        return review.to_review_dto()