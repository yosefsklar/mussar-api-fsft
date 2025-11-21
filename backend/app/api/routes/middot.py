from typing import Any, List
import logging

from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.models import Middah, MiddahCreate, MiddahRead

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/middot", tags=["middot"])


@router.get("/", response_model=List[MiddahRead])
def list_middot(session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Retrieve middot.
    """
    logger.info(f"Listing all middot user_id={current_user.id}")
    statement = select(Middah)
    return session.exec(statement).all()


@router.get("/{name_transliterated}", response_model=MiddahRead)
def get_middah(session: SessionDep, current_user: CurrentUser, name_transliterated: str) -> Any:
    """
    Get middah by name_transliterated.
    """
    logger.info(f"Fetching middah user_id={current_user.id} middah_name={name_transliterated}")
    middah = session.get(Middah, name_transliterated)
    if not middah:
        logger.warning(f"Middah not found user_id={current_user.id} middah_name={name_transliterated}")
        raise HTTPException(status_code=404, detail="Middah not found")
    return middah


@router.post("/", response_model=MiddahRead, status_code=status.HTTP_201_CREATED)
def create_middah(*, session: SessionDep, current_user: CurrentUser, middah_in: MiddahCreate) -> Any:
    # Require superuser to create
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted to create middah user_id={current_user.id}")
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    
    payload = middah_in.model_dump()
    logger.info(f"Creating middah user_id={current_user.id} {payload=}")
    middah = Middah.model_validate(middah_in)
    session.add(middah)
    try:
        session.commit()
        session.refresh(middah)
        logger.info(f"Successfully created middah middah_name={middah.name_transliterated}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError creating middah {error_info}")
        if "primary key" in error_info.lower() or "unique" in error_info.lower():
            raise HTTPException(status_code=400, detail="Middah already exists")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return middah


@router.delete("/{name_transliterated}", status_code=status.HTTP_204_NO_CONTENT)
def delete_middah(*, session: SessionDep, current_user: CurrentUser, name_transliterated: str):
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted to delete middah user_id={current_user.id} middah_name={name_transliterated}")
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    middah = session.get(Middah, name_transliterated)
    if not middah:
        logger.warning(f"Middah not found for deletion middah_name={name_transliterated}")
        raise HTTPException(status_code=404, detail="Middah not found")
    
    logger.info(f"Deleting middah user_id={current_user.id} middah_name={name_transliterated}")
    session.delete(middah)
    session.commit()
    logger.info(f"Successfully deleted middah middah_name={name_transliterated}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
