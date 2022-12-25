from abc import ABC, abstractmethod

class PredictionModel(ABC):
    """PredictionModel defines contract for predict review"""
    @abstractmethod
    def predict(review_body: str) -> float:
        raise NotImplementedError
    