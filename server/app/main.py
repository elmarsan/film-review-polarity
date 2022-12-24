from domain.review_create_dto import ReviewCreateDTO
from fastapi import FastAPI, HTTPException, Path
from domain.review_dto import ReviewDTO
from database import Session, init_database
from domain.review import Review
from domain.review_fix_score_dto import ReviewSetUserScoreDTO
from application.review_finder_service import ReviewFinderService
from application.review_user_score_updater_service import ReviewUserScoreUpdateService
from application.review_creator_service import ReviewCreatorService
from infrastructure.sqlite_review_query_repository import SqliteReviewQueryRepository
from infrastructure.sqlite_review_command_repository import SqliteReviewCommandRepository

init_database()

app = FastAPI()

session = Session()

query_repository = SqliteReviewQueryRepository(session)
command_repository = SqliteReviewCommandRepository(session)

review_finder_service = ReviewFinderService(query_repository)
review_user_score_updater_service = ReviewUserScoreUpdateService(query_repository, command_repository)
review_creator = ReviewCreatorService(command_repository)

@app.post("/review", response_model=ReviewDTO)
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

