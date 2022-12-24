from typing import Optional
from domain.review_query_repository import ReviewQueryRepository
from sqlalchemy.orm.session import Session

from domain.review import Review

class SqliteReviewQueryRepository(ReviewQueryRepository):
    """SqliteReviewQueryRepository implements ReviewQueryRepository with Sqlite"""
    
    def __init__(self, session: Session):
        self.session: Session = session

    def find_all(self) -> list[Review]:
        return self.session.query(Review).all()

    def find_by_id(self, id: int) -> Optional[Review]:
        return self.session.query(Review).filter_by(id = id).one_or_none()

