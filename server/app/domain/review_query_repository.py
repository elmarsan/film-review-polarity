from abc import ABC, abstractmethod

from .review import Review

class ReviewQueryRepository(ABC):
    """ReviewQueryRepository defines a repository for query review table"""

    @abstractmethod
    def find_all() -> list[Review]:
        raise NotImplementedError