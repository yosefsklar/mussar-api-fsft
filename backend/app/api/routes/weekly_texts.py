from typing import Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    WeeklyText,
    WeeklyTextCreate,
    WeeklyTextRead,
    WeeklyTextPatch,
)

router = APIRouter(prefix="/weekly_texts", tags=["weekly_texts"])


@router.get("/", response_model=List[WeeklyTextRead])
def list_weekly_texts(session: SessionDep) -> Any:
    statement = select(WeeklyText)
    return session.exec(statement).all()


@router.post("/", response_model=WeeklyTextRead, status_code=status.HTTP_201_CREATED)
def create_weekly_text(*, session: SessionDep, current_user: CurrentUser, wt_in: WeeklyTextCreate) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    wt = WeeklyText.model_validate(wt_in, update={"created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    session.add(wt)
    session.commit()
    session.refresh(wt)
    return wt


@router.get("/{id}", response_model=WeeklyTextRead)
def get_weekly_text(session: SessionDep, id: int) -> Any:
    wt = session.get(WeeklyText, id)
    if not wt:
        raise HTTPException(status_code=404, detail="Weekly text not found")
    return wt


@router.patch("/{id}", response_model=WeeklyTextRead)
def patch_weekly_text(*, session: SessionDep, current_user: CurrentUser, id: int, patch: WeeklyTextPatch) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    wt = session.get(WeeklyText, id)
    if not wt:
        raise HTTPException(status_code=404, detail="Weekly text not found")
    update_dict = patch.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(wt, k, v)
    wt.updated_at = datetime.now(timezone.utc)
    session.add(wt)
    session.commit()
    session.refresh(wt)
    return wt


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_weekly_text(*, session: SessionDep, current_user: CurrentUser, id: int):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    wt = session.get(WeeklyText, id)
    if not wt:
        raise HTTPException(status_code=404, detail="Weekly text not found")
    session.delete(wt)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
