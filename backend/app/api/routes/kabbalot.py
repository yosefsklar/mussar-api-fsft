from typing import Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Kabbalah,
    KabbalahCreate,
    KabbalahRead,
    KabbalahPatch,
)

router = APIRouter(prefix="/kabbalot", tags=["kabbalot"])


@router.get("/", response_model=List[KabbalahRead])
def list_kabbalot(session: SessionDep) -> Any: 
    statement = select(Kabbalah)
    return session.exec(statement).all()


@router.post("/", response_model=KabbalahRead, status_code=status.HTTP_201_CREATED)
def create_kabbalah(*, session: SessionDep, current_user: CurrentUser, kabbalah_in: KabbalahCreate) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    kabbalah = Kabbalah.model_validate(kabbalah_in, update={"created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    session.add(kabbalah)
    try:
        session.commit()
        session.refresh(kabbalah)
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        if "kabbalot_middah_description_uq" in error_info:
            raise HTTPException(status_code=400, detail="Kabbalah already exists for this middah and description")
        elif "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return kabbalah


@router.get("/{id}", response_model=KabbalahRead)
def get_kabbalah(session: SessionDep, id: int) -> Any:
    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    return kabbalah


@router.patch("/{id}", response_model=KabbalahRead)
def patch_kabbalah(*, session: SessionDep, current_user: CurrentUser, id: int, patch: KabbalahPatch) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    update_dict = patch.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(kabbalah, k, v)
    kabbalah.updated_at = datetime.now(timezone.utc)
    session.add(kabbalah)
    session.commit()
    session.refresh(kabbalah)
    return kabbalah


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kabbalah(*, session: SessionDep, current_user: CurrentUser, id: int):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    session.delete(kabbalah)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
