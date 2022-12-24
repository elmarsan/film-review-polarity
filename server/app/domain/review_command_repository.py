from abc import ABC, abstractmethod

from .review import Review

class ReviewCommandRepository(ABC):
    """ReviewCommandRepository defines a repository for mutate review table"""

    @abstractmethod
    def insert(review: Review) -> Review:
        raise NotImplementedError

    @abstractmethod
    def set_user_score(review: Review, score: float) -> Review:
        raise NotImplementedError