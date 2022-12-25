import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from application.review_user_score_updater_service import ReviewUserScoreUpdateService
from domain.review_create_dto import ReviewCreateDTO
from mocks.mock_repository import MockReviewCommandRepository, MockReviewQueryRepository
from mocks.review_random_factory import ReviewRandomFactory


command_repository = MockReviewCommandRepository()
query_repository = MockReviewQueryRepository()
service = ReviewUserScoreUpdateService(query_repository, command_repository)


class TestReviewUserScoreUpdaterService(unittest.TestCase):
    """TestReviewUserScoreUpdaterService unit tests"""

    def test_should_return_review_dto_with_updated_user_score(self):
        score = 7
        updated_review = service.update(1, score)
        self.assertEqual(updated_review.user_score, score)

    def test_should_throw_404_when_review_does_NOT_exist(self):
        service.query_repository.find_by_id = MagicMock(return_value=None)
        with self.assertRaises(HTTPException):
            service.update(1, 5)
