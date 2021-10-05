from fastapi import APIRouter

from .setuRoutes.consent import router as consentRouter
from .setuRoutes.data import router as dataRouter


router = APIRouter()

router.include_router(
    consentRouter,
    tags=["consent"],
    prefix="/consent",
)
router.include_router(dataRouter, tags=["data"], prefix="/data")
