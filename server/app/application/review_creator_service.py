from domain.review_command_repository import ReviewCommandRepository
from domain.review_create_dto import ReviewCreateDTO
from domain.review_dto import ReviewDTO
from domain.review import Review


class ReviewCreatorService:
    """ReviewCreatorService defines service for insert records in review table"""

    def __init__(self, command_repository: ReviewCommandRepository):
        self.command_repository = command_repository

    
    def create(self, review_create_dto: ReviewCreateDTO) -> ReviewDTO:
        review = Review.from_review_create_dto(review_create_dto)
        return self.command_repository.insert(review).to_review_dto()

