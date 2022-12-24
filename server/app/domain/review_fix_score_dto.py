from pydantic import BaseModel, Field


class ReviewSetUserScoreDTO(BaseModel):
    score: float = Field(ge=0, le=10, description="Review score based on user criteria")