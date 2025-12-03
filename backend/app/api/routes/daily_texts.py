import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    DailyText,
    DailyTextCreate,
    DailyTextPatch,
    DailyTextRead,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/daily_texts", tags=["daily_texts"])


@router.get("/", response_model=list[DailyTextRead])
def list_daily_texts(session: SessionDep, current_user: CurrentUser) -> Any:
    logger.info(f"Listing all daily texts user_id={current_user.id}")
    statement = select(DailyText)
    return session.exec(statement).all()


@router.post("/", response_model=DailyTextRead)
def create_daily_text(
    *, session: SessionDep, current_user: CurrentUser, daily_text_in: DailyTextCreate
) -> Any:
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted to create daily text user_id={current_user.id}")
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    payload = daily_text_in.model_dump()
    logger.info(f"Creating daily text user_id={current_user.id} {payload=}")
    daily_text = DailyText.model_validate(
        daily_text_in,
        update={
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )
    session.add(daily_text)
    try:
        session.commit()
        session.refresh(daily_text)
        logger.info(f"Successfully created daily text daily_text_id={daily_text.id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError creating daily text {error_info}")
        if "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return daily_text


@router.get("/{id}", response_model=DailyTextRead)
def get_daily_text(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    logger.info(f"Fetching daily text user_id={current_user.id} daily_text_id={id}")
    daily_text = session.get(DailyText, id)
    if not daily_text:
        logger.warning(f"Daily text not found user_id={current_user.id} daily_text_id={id}")
        raise HTTPException(status_code=404, detail="Daily text not found")
    return daily_text


@router.patch("/{id}", response_model=DailyTextRead)
def patch_daily_text(
    *, session: SessionDep, current_user: CurrentUser, id: int, patch: DailyTextPatch
) -> Any:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to patch daily text user_id={current_user.id} daily_text_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    daily_text = session.get(DailyText, id)
    if not daily_text:
        logger.warning(f"Daily text not found for patch daily_text_id={id}")
        raise HTTPException(status_code=404, detail="Daily text not found")

    update_dict = patch.model_dump(exclude_unset=True)
    logger.info(f"Patching daily text user_id={current_user.id} daily_text_id={id} {update_dict}")
    for k, v in update_dict.items():
        setattr(daily_text, k, v)
    daily_text.updated_at = datetime.now(timezone.utc)
    try:
        session.commit()
        session.refresh(daily_text)
        logger.info(f"Successfully patched daily text daily_text_id={id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError patching daily text daily_text_id={id} {error_info}")
        if "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return daily_text


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_text(*, session: SessionDep, current_user: CurrentUser, id: int) -> Response:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to delete daily text user_id={current_user.id} daily_text_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    daily_text = session.get(DailyText, id)
    if not daily_text:
        logger.warning(f"Daily text not found for deletion daily_text_id={id}")
        raise HTTPException(status_code=404, detail="Daily text not found")

    logger.info(f"Deleting daily text user_id={current_user.id} daily_text_id={id}")
    session.delete(daily_text)
    session.commit()
    logger.info(f"Successfully deleted daily text daily_text_id={id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
