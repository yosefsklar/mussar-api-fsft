import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ReminderPhrase,
    ReminderPhraseCreate,
    ReminderPhrasePatch,
    ReminderPhraseRead,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reminder_phrases", tags=["reminder_phrases"])


@router.get("/", response_model=list[ReminderPhraseRead])
def list_reminder_phrases(session: SessionDep, current_user: CurrentUser) -> Any:
    logger.info(f"Listing all reminder phrases user_id={current_user.id}")
    statement = select(ReminderPhrase)
    return session.exec(statement).all()


@router.post("/", response_model=ReminderPhraseRead)
def create_reminder_phrase(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    reminder_phrase_in: ReminderPhraseCreate,
) -> Any:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to create reminder phrase user_id={current_user.id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    payload = reminder_phrase_in.model_dump()
    logger.info(f"Creating reminder phrase user_id={current_user.id} {payload=}")
    reminder_phrase = ReminderPhrase.model_validate(
        reminder_phrase_in,
        update={
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )
    session.add(reminder_phrase)
    try:
        session.commit()
        session.refresh(reminder_phrase)
        logger.info(f"Successfully created reminder phrase reminder_phrase_id={reminder_phrase.id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError creating reminder phrase {error_info}")
        if "reminder_phrases_middah_text_uq" in error_info or "unique" in error_info.lower():
            raise HTTPException(
                status_code=400,
                detail="Reminder phrase already exists for this middah and text",
            )
        elif "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return reminder_phrase


@router.get("/{id}", response_model=ReminderPhraseRead)
def get_reminder_phrase(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    logger.info(f"Fetching reminder phrase user_id={current_user.id} reminder_phrase_id={id}")
    reminder_phrase = session.get(ReminderPhrase, id)
    if not reminder_phrase:
        logger.warning(
            f"Reminder phrase not found user_id={current_user.id} reminder_phrase_id={id}"
        )
        raise HTTPException(status_code=404, detail="Reminder phrase not found")
    return reminder_phrase


@router.patch("/{id}", response_model=ReminderPhraseRead)
def patch_reminder_phrase(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    patch: ReminderPhrasePatch,
) -> Any:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to patch reminder phrase user_id={current_user.id} reminder_phrase_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    reminder_phrase = session.get(ReminderPhrase, id)
    if not reminder_phrase:
        logger.warning(f"Reminder phrase not found for patch reminder_phrase_id={id}")
        raise HTTPException(status_code=404, detail="Reminder phrase not found")

    update_dict = patch.model_dump(exclude_unset=True)
    logger.info(
        f"Patching reminder phrase user_id={current_user.id} reminder_phrase_id={id} {update_dict}"
    )
    for k, v in update_dict.items():
        setattr(reminder_phrase, k, v)
    reminder_phrase.updated_at = datetime.now(timezone.utc)
    try:
        session.commit()
        session.refresh(reminder_phrase)
        logger.info(f"Successfully patched reminder phrase reminder_phrase_id={id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(
            f"IntegrityError patching reminder phrase reminder_phrase_id={id} {error_info}"
        )
        if "reminder_phrases_middah_text_uq" in error_info or "unique" in error_info.lower():
            raise HTTPException(
                status_code=400,
                detail="Reminder phrase already exists for this middah and text",
            )
        elif "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return reminder_phrase


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder_phrase(*, session: SessionDep, current_user: CurrentUser, id: int) -> Response:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to delete reminder phrase user_id={current_user.id} reminder_phrase_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    reminder_phrase = session.get(ReminderPhrase, id)
    if not reminder_phrase:
        logger.warning(f"Reminder phrase not found for deletion reminder_phrase_id={id}")
        raise HTTPException(status_code=404, detail="Reminder phrase not found")

    logger.info(f"Deleting reminder phrase user_id={current_user.id} reminder_phrase_id={id}")
    session.delete(reminder_phrase)
    session.commit()
    logger.info(f"Successfully deleted reminder phrase reminder_phrase_id={id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
