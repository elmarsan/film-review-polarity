from domain.review_command_repository import ReviewCommandRepository
from domain.review import Review
from sqlalchemy.orm.session import Session

class SqliteReviewCommandRepository(ReviewCommandRepository):
    """SqliteReviewCommandRepository implements ReviewCommandRepository with Sqlite"""

    def __init__(self, session: Session):
        self.session: Session = session


    def insert(self, review: Review) -> Review:
        self.session.add(review)
        self.session.commit()
        return review


    def set_user_score(self, review: Review, score: float) -> Review:
        review.user_score = score
        self.session.commit()
        return review

    