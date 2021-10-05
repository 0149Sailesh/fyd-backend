from fastapi import APIRouter

from .setuRoutes.consent import router as consentRouter
from .setuRoutes.data import router as dataRouter
from .setuRoutes.webhooks import router as webhookRouter

router = APIRouter()

router.include_router(consentRouter, tags=["consent"], prefix="/consent")
router.include_router(dataRouter, tags=["data"], prefix="/data")
router.include_router(webhookRouter, tags=["notification"], prefix="/webhook")
