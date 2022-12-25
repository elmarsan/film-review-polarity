from typing import Union

from app.database import Base
from .review_dto import ReviewDTO
from .review_create_dto import ReviewCreateDTO
from sqlalchemy import Column, DateTime, Float, Integer, String, func


class Review(Base):
    """Review holds the information of user review"""

    __tablename__ = "review"

    id: Union[str, Column] = Column(Integer, primary_key=True)
    film_name: Union[str, Column] = Column(String, unique=False, nullable=False)
    review_name: Union[str, Column] = Column(String, nullable=False)
    body: Union[str, Column] = Column(String, nullable=False)
    author: Union[str, Column] = Column(String, nullable=False)
    model_score: Union[float, Column] = Column(Float, nullable=False)
    user_score: Union[float, Column] = Column(Float, nullable=True)
    created_at: Union[int, Column] = Column(DateTime(timezone=True), default=func.now())
    updated_at: Union[int, Column] = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    def to_review_dto(self) -> "ReviewDTO":
        return ReviewDTO(
            film_name = self.film_name,
            review_name = self.review_name,
            body = self.body,
            author = self.author,
            model_score = self.model_score,
            user_score = self.user_score,
            date = str(self.created_at)
        )

    @staticmethod
    def from_review_create_dto(review_create_dto: ReviewCreateDTO) -> 'Review':
        return Review(
            film_name= review_create_dto.film_name,
            review_name= review_create_dto.review_name,
            body= review_create_dto.body,
            author= review_create_dto.author,
            model_score= 0
        )