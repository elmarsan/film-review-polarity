from pydantic import BaseModel, Field


class ReviewDTO(BaseModel):
    film_name: str = Field(description="Film name")
    review_name: str = Field(description="Review name")
    body: str = Field(description="Review text")
    author: str = Field(description="Review author")
    model_score: float = Field(description="Review score predicted by model")
    user_score: float | None = Field(description="Review score based on user criteria")
    date: str | None = Field(description="Review date")