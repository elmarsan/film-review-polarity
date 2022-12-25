import http
from fastapi.testclient import TestClient
from fastapi import FastAPI, Path
import pytest

from domain.review_create_dto import ReviewCreateDTO
from domain.review_dto import ReviewDTO
from database import Session, init_database
from domain.review_fix_score_dto import ReviewSetUserScoreDTO
from application.review_finder_service import ReviewFinderService
from application.review_user_score_updater_service import ReviewUserScoreUpdateService
from application.review_creator_service import ReviewCreatorService
from infrastructure.sqlite_review_query_repository import SqliteReviewQueryRepository
from infrastructure.sqlite_review_command_repository import SqliteReviewCommandRepository
from mocks.review_random_factory import ReviewRandomFactory

init_database()

app = FastAPI()

session = Session()

query_repository = SqliteReviewQueryRepository(session)
command_repository = SqliteReviewCommandRepository(session)

review_finder_service = ReviewFinderService(query_repository)
review_user_score_updater_service = ReviewUserScoreUpdateService(query_repository, command_repository)
review_creator = ReviewCreatorService(command_repository)

@app.post("/review", response_model=ReviewDTO, status_code=http.HTTPStatus.CREATED)
async def create_review(create_review_dto: ReviewCreateDTO):
    return review_creator.create(create_review_dto)


@app.get("/review", response_model=list[ReviewDTO])
async def find_reviews():
    return review_finder_service.find_all()


@app.put("/review/{id}", response_model=ReviewDTO)
async def set_user_score(
    review_set_user_score_dto: ReviewSetUserScoreDTO,
    id: int = Path("The id of review to fix score"),
):
    score = review_set_user_score_dto.score
    return review_user_score_updater_service.update(id, score)


client = TestClient(app)


class TestPostReview:
    def test_create_review(self):
        response = client.post("/review", json={
            "film_name": "OldBoy",
            "review_name": "Probably one of the best films ever",
            "body": "elmarsan",
            "author": "I love this movie"
        })
        assert response.status_code == 201
        review = response.json()
        assert review['film_name'] == "OldBoy"
        assert review['review_name'] == "Probably one of the best films ever"
        assert review['body'] == "elmarsan"
        assert review['author'] == "I love this movie"
        assert review['model_score'] >= 0
        assert review['user_score'] is None



class TestGetReview:
    @pytest.fixture(autouse=True)
    def set_up(self):
        review_list = ReviewRandomFactory.create_multiple()
        for review in review_list:
            client.post("/review", json={
            "film_name": review.film_name,
            "review_name": review.review_name,
            "body": review.body,
            "author": review.author
        })


    def test_find_reviews(self):
        response = client.get("/review")
        assert response.status_code == 200
        response = response.json()
        assert len(response) > 0



class TestPutReview:
    @pytest.fixture(autouse=True)
    def set_up(self):
        review = ReviewRandomFactory.create(None)
        client.post("/review", json={
            "film_name": review.film_name,
            "review_name": review.review_name,
            "body": review.body,
            "author": review.author
        })

    def test_update_user_score(self):
        score = 3
        response = client.put("/review/1", json={
            "score": score
        })

        assert response.status_code == 200
        review = response.json()
        assert review['user_score'] == score
