from .setuRoutes.consent import router as consentRouter

from fastapi import APIRouter

router = APIRouter()

router.include_router(consentRouter, prefix="/consent")
