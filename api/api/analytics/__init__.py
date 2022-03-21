from fastapi import APIRouter

from api.analytics import judgment, species

router = APIRouter(prefix="/analytics")
router.include_router(judgment.router)
router.include_router(species.router)
