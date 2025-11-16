from typing import Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ReminderPhrase,
    ReminderPhraseCreate,
    ReminderPhraseRead,
    ReminderPhrasePatch,
)

router = APIRouter(prefix="/reminder_phrases", tags=["reminder_phrases"])


@router.get("/", response_model=List[ReminderPhraseRead])
def list_reminder_phrases(session: SessionDep) -> Any:
    statement = select(ReminderPhrase)
    return session.exec(statement).all()


@router.post("/", response_model=ReminderPhraseRead, status_code=status.HTTP_201_CREATED)
def create_reminder_phrase(*, session: SessionDep, current_user: CurrentUser, rp_in: ReminderPhraseCreate) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    # uniqueness (middah, text)
    existing = session.exec(select(ReminderPhrase).where(ReminderPhrase.middah == rp_in.middah, ReminderPhrase.text == rp_in.text)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Reminder phrase already exists for middah")
    rp = ReminderPhrase.model_validate(rp_in, update={"created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    session.add(rp)
    session.commit()
    session.refresh(rp)
    return rp


@router.get("/{id}", response_model=ReminderPhraseRead)
def get_reminder_phrase(session: SessionDep, id: int) -> Any:
    rp = session.get(ReminderPhrase, id)
    if not rp:
        raise HTTPException(status_code=404, detail="Reminder phrase not found")
    return rp


@router.patch("/{id}", response_model=ReminderPhraseRead)
def patch_reminder_phrase(*, session: SessionDep, current_user: CurrentUser, id: int, patch: ReminderPhrasePatch) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    rp = session.get(ReminderPhrase, id)
    if not rp:
        raise HTTPException(status_code=404, detail="Reminder phrase not found")
    update_dict = patch.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(rp, k, v)
    rp.updated_at = datetime.now(timezone.utc)
    session.add(rp)
    session.commit()
    session.refresh(rp)
    return rp


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder_phrase(*, session: SessionDep, current_user: CurrentUser, id: int):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    rp = session.get(ReminderPhrase, id)
    if not rp:
        raise HTTPException(status_code=404, detail="Reminder phrase not found")
    session.delete(rp)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
