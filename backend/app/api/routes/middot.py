from typing import Any, List

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Middah, MiddahCreate, MiddahRead

router = APIRouter(prefix="/middot", tags=["middot"])


@router.get("/", response_model=List[MiddahRead])
def list_middot(session: SessionDep) -> Any:
    """
    Retrieve middot.
    """
    statement = select(Middah)
    return session.exec(statement).all()


@router.get("/{name_transliterated}", response_model=MiddahRead)
def get_middah(session: SessionDep, name_transliterated: str) -> Any:
    """
    Get middah by name_transliterated.
    """
    middah = session.get(Middah, name_transliterated)
    if not middah:
        raise HTTPException(status_code=404, detail="Middah not found")
    return middah


@router.post("/", response_model=MiddahRead, status_code=status.HTTP_201_CREATED)
def create_middah(*, session: SessionDep, current_user: CurrentUser, middah_in: MiddahCreate) -> Any:
    # Require superuser to create
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    existing = session.get(Middah, middah_in.name_transliterated)
    if existing:
        raise HTTPException(status_code=400, detail="Middah already exists")
    middah = Middah.model_validate(middah_in)
    session.add(middah)
    session.commit()
    session.refresh(middah)
    return middah


@router.delete("/{name_transliterated}", status_code=status.HTTP_204_NO_CONTENT)
def delete_middah(*, session: SessionDep, current_user: CurrentUser, name_transliterated: str):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    middah = session.get(Middah, name_transliterated)
    if not middah:
        raise HTTPException(status_code=404, detail="Middah not found")
    session.delete(middah)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
