import random

from domain.prediction_model import PredictionModel


class MockPredictionModel(PredictionModel):
    def predict(self, review_body: str) -> float:
        return random.randint(0, 10)

