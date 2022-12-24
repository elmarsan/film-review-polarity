from abc import ABC, abstractmethod
from typing import Optional

from .review import Review

class ReviewQueryRepository(ABC):
    """ReviewQueryRepository defines a repository for query review table"""

    @abstractmethod
    def find_all() -> list[Review]:
        raise NotImplementedError
    

    @abstractmethod
    def find_by_id(id: int) -> Optional[Review]:
        raise NotImplementedError