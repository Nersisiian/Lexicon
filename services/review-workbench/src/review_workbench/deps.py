from .service import ReviewService
from .repository import ReviewRepository
from .config import settings

_repo = ReviewRepository(str(settings.DATABASE_URL))

def get_review_service():
    return ReviewService(_repo)


