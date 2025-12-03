import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    WeeklyText,
    WeeklyTextCreate,
    WeeklyTextPatch,
    WeeklyTextRead,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/weekly_texts", tags=["weekly_texts"])


@router.get("/", response_model=list[WeeklyTextRead])
def list_weekly_texts(session: SessionDep, current_user: CurrentUser) -> Any:
    logger.info(f"Listing all weekly texts user_id={current_user.id}")
    statement = select(WeeklyText)
    return session.exec(statement).all()


@router.post("/", response_model=WeeklyTextRead)
def create_weekly_text(
    *, session: SessionDep, current_user: CurrentUser, weekly_text_in: WeeklyTextCreate
) -> Any:
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted to create weekly text user_id={current_user.id}")
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    payload = weekly_text_in.model_dump()
    logger.info(f"Creating weekly text user_id={current_user.id} {payload=}")
    weekly_text = WeeklyText.model_validate(
        weekly_text_in,
        update={
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )
    session.add(weekly_text)
    try:
        session.commit()
        session.refresh(weekly_text)
        logger.info(f"Successfully created weekly text weekly_text_id={weekly_text.id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError creating weekly text {error_info}")
        if "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return weekly_text


@router.get("/{id}", response_model=WeeklyTextRead)
def get_weekly_text(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    logger.info(f"Fetching weekly text user_id={current_user.id} weekly_text_id={id}")
    weekly_text = session.get(WeeklyText, id)
    if not weekly_text:
        logger.warning(f"Weekly text not found user_id={current_user.id} weekly_text_id={id}")
        raise HTTPException(status_code=404, detail="Weekly text not found")
    return weekly_text


@router.patch("/{id}", response_model=WeeklyTextRead)
def patch_weekly_text(
    *, session: SessionDep, current_user: CurrentUser, id: int, patch: WeeklyTextPatch
) -> Any:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to patch weekly text user_id={current_user.id} weekly_text_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    weekly_text = session.get(WeeklyText, id)
    if not weekly_text:
        logger.warning(f"Weekly text not found for patch weekly_text_id={id}")
        raise HTTPException(status_code=404, detail="Weekly text not found")

    update_dict = patch.model_dump(exclude_unset=True)
    logger.info(f"Patching weekly text user_id={current_user.id} weekly_text_id={id} {update_dict}")
    for k, v in update_dict.items():
        setattr(weekly_text, k, v)
    weekly_text.updated_at = datetime.now(timezone.utc)
    try:
        session.commit()
        session.refresh(weekly_text)
        logger.info(f"Successfully patched weekly text weekly_text_id={id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError patching weekly text weekly_text_id={id} {error_info}")
        if "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return weekly_text


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weekly_text(*, session: SessionDep, current_user: CurrentUser, id: int) -> Response:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to delete weekly text user_id={current_user.id} weekly_text_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    weekly_text = session.get(WeeklyText, id)
    if not weekly_text:
        logger.warning(f"Weekly text not found for deletion weekly_text_id={id}")
        raise HTTPException(status_code=404, detail="Weekly text not found")

    logger.info(f"Deleting weekly text user_id={current_user.id} weekly_text_id={id}")
    session.delete(weekly_text)
    session.commit()
    logger.info(f"Successfully deleted weekly text weekly_text_id={id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
