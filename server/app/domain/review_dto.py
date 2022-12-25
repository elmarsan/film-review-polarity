from typing import Optional
from pydantic import BaseModel, Field


class ReviewDTO(BaseModel):
    """ReviewDTO public data of review record"""

    film_name: str = Field(description="Film name")
    review_name: str = Field(description="Review name")
    body: str = Field(description="Review text")
    author: str = Field(description="Review author")
    model_score: float = Field(description="Review score predicted by model")
    user_score: Optional[float] = Field(description="Review score based on user criteria")
    date: Optional[str] = Field(description="Review date")