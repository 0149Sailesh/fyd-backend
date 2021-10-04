from .setuRoutes.consent import router as consentRouter
from .setuRoutes.data import router as dataRouter

from fastapi import APIRouter

router = APIRouter()

router.include_router(consentRouter, prefix="/consent")
router.include_router(dataRouter, prefix="/data")
