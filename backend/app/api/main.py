from fastapi import APIRouter

from app.api.routes import (
    items,
    login,
    private,
    users,
    utils,
    middot,
    reminder_phrases,
    daily_texts,
    kabbalot,
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
