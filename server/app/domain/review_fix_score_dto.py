from pydantic import BaseModel, Field


class ReviewSetUserScoreDTO(BaseModel):
    """ReviewSetUserScoreDTO payload for updating user_score review property"""
    
    score: float = Field(ge=0, le=10, description="Review score based on user criteria")