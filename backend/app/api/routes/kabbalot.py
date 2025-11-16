from typing import Any, List
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

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
def create_kabbalah(*, session: SessionDep, current_user: CurrentUser, kb_in: KabbalahCreate) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    existing = session.exec(select(Kabbalah).where(Kabbalah.middah == kb_in.middah, Kabbalah.description == kb_in.description)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Kabbalah already exists for middah")
    kb = Kabbalah.model_validate(kb_in, update={"created_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
    session.add(kb)
    session.commit()
    session.refresh(kb)
    return kb


@router.get("/{id}", response_model=KabbalahRead)
def get_kabbalah(session: SessionDep, id: int) -> Any:
    kb = session.get(Kabbalah, id)
    if not kb:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    return kb


@router.patch("/{id}", response_model=KabbalahRead)
def patch_kabbalah(*, session: SessionDep, current_user: CurrentUser, id: int, patch: KabbalahPatch) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    kb = session.get(Kabbalah, id)
    if not kb:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    update_dict = patch.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(kb, k, v)
    kb.updated_at = datetime.now(timezone.utc)
    session.add(kb)
    session.commit()
    session.refresh(kb)
    return kb


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kabbalah(*, session: SessionDep, current_user: CurrentUser, id: int):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    kb = session.get(Kabbalah, id)
    if not kb:
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    session.delete(kb)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
