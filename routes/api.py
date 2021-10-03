from fastapi import APIRouter

from .auth import router as auth_router

router = APIRouter()

# include all the api router here
router.include_router(auth_router, tags=["auth"], prefix="/auth")
