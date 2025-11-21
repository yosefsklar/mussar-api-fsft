from fastapi import APIRouter

from app.api.routes import (
    daily_texts,
    items,
    kabbalot,
    login,
    middot,
    private,
    reminder_phrases,
    users,
    utils,
    weekly_texts,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(middot.router)
api_router.include_router(reminder_phrases.router)
api_router.include_router(daily_texts.router)
api_router.include_router(kabbalot.router)
api_router.include_router(weekly_texts.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
