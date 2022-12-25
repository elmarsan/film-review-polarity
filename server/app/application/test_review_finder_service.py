import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from application.review_user_score_updater_service import ReviewUserScoreUpdateService
from application.review_finder_service import ReviewFinderService
from domain.review_create_dto import ReviewCreateDTO
from mocks.mock_repository import MockReviewCommandRepository, MockReviewQueryRepository
from mocks.review_random_factory import ReviewRandomFactory


query_repository = MockReviewQueryRepository()
service = ReviewFinderService(query_repository)


class TestReviewFinderService(unittest.TestCase):
    """TestReviewFinderService unit tests"""

    def test_should_return_review_dto_when_review_exists(self):
        review = ReviewRandomFactory.create(None)
        service.query_repository.find_by_id = MagicMock(return_value=review)
        review_by_id = service.find_by_id(review.id)
        self.assertIsNotNone(review_by_id)

    def test_should_return_None_when_review_does_NOT_exist(self):
        service.query_repository.find_by_id = MagicMock(return_value=None)
        review_by_id = service.find_by_id(1)
        self.assertIsNone(review_by_id)

    def test_should_return_empty_list_when_there_is_NOT_reviews(self):
        review_list = ReviewRandomFactory.create_multiple()
        service.query_repository.find_all = MagicMock(return_value=review_list)
        reviews = service.find_all()
        self.assertEqual(len(review_list), len(reviews))

    def test_should_return_list_with_all_reviews(self):
        service.query_repository.find_all = MagicMock(return_value=[])
        reviews = service.find_all()
        self.assertEqual(0, len(reviews))
