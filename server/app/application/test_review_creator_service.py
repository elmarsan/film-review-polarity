import unittest

from domain.review_create_dto import ReviewCreateDTO
from mocks.mock_repository import MockReviewCommandRepository

from .review_creator_service import ReviewCreatorService

repository = MockReviewCommandRepository()
service = ReviewCreatorService(repository)


class TestReviewCreatorService(unittest.TestCase):
    """TestReviewCreatorService unit tests"""

    def test_should_return_review_dto_when_create_was_successfully(self):
        film_name = "OldBoy"
        review_name = "Probably one of the best films ever"
        author = "elmarsan"
        body = "I love this movie"

        review = service.create(ReviewCreateDTO(
            film_name=film_name,
            review_name=review_name,
            author=author,
            body=body
        ))

        self.assertEqual(review.film_name, film_name)
        self.assertEqual(review.review_name, review_name)
        self.assertEqual(review.author, author)
        self.assertEqual(review.body, body)
        self.assertGreaterEqual(review.model_score, 0)
        self.assertLessEqual(review.model_score, 10)
