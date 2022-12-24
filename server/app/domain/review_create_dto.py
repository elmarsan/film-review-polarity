from pydantic import BaseModel, Field


class ReviewCreateDTO(BaseModel):
    """ReviewCreateDTO payload for creating new review"""

    film_name: str = Field(description="Film name")
    review_name: str= Field(description="Review name")
    body: str= Field(description="Review text")
    author: str= Field(description="Review author")
