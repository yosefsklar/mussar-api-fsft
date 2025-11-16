from typing import Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    DailyText,
    DailyTextCreate,
    DailyTextRead,
    DailyTextPatch,
)

router = APIRouter(prefix="/daily_texts", tags=["daily_texts"])


@router.get("/", response_model=List[DailyTextRead])
def list_daily_texts(session: SessionDep) -> Any:
    statement = select(DailyText)
    return session.exec(statement).all()


@router.post("/", response_model=DailyTextRead, status_code=status.HTTP_201_CREATED)
def create_daily_text(*, session: SessionDep, current_user: CurrentUser, dt_in: DailyTextCreate) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    dt = DailyText.model_validate(dt_in, update={"created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    session.add(dt)
    session.commit()
    session.refresh(dt)
    return dt


@router.get("/{id}", response_model=DailyTextRead)
def get_daily_text(session: SessionDep, id: int) -> Any:
    dt = session.get(DailyText, id)
    if not dt:
        raise HTTPException(status_code=404, detail="Daily text not found")
    return dt


@router.patch("/{id}", response_model=DailyTextRead)
def patch_daily_text(*, session: SessionDep, current_user: CurrentUser, id: int, patch: DailyTextPatch) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    dt = session.get(DailyText, id)
    if not dt:
        raise HTTPException(status_code=404, detail="Daily text not found")
    update_dict = patch.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(dt, k, v)
    dt.updated_at = datetime.now(timezone.utc)
    session.add(dt)
    session.commit()
    session.refresh(dt)
    return dt


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_text(*, session: SessionDep, current_user: CurrentUser, id: int):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    dt = session.get(DailyText, id)
    if not dt:
        raise HTTPException(status_code=404, detail="Daily text not found")
    session.delete(dt)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
