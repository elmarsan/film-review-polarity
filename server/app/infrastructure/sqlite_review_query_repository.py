from typing import Optional
from app.domain.review_query_repository import ReviewQueryRepository
from sqlalchemy.orm.session import Session

from app.domain.review import Review

class SqliteReviewQueryRepository(ReviewQueryRepository):
    """SqliteReviewQueryRepository implements ReviewQueryRepository with Sqlite"""
    
    def __init__(self, session: Session):
        self.session: Session = session

    def find_all(self) -> list[Review]:
        return self.session.query(Review).order_by(Review.created_at.desc()).all()

    def find_by_id(self, id: int) -> Optional[Review]:
        return self.session.query(Review).filter_by(id = id).one_or_none()

