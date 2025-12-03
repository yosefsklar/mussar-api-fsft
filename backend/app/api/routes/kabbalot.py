import logging
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Kabbalah,
    KabbalahCreate,
    KabbalahPatch,
    KabbalahRead,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/kabbalot", tags=["kabbalot"])


@router.get("/", response_model=list[KabbalahRead])
def list_kabbalot(session: SessionDep, current_user: CurrentUser) -> Any:
    logger.info(f"Listing all kabbalot user_id={current_user.id}")
    statement = select(Kabbalah)
    return session.exec(statement).all()


@router.post("/", response_model=KabbalahRead)
def create_kabbalah(
    *, session: SessionDep, current_user: CurrentUser, kabbalah_in: KabbalahCreate
) -> Any:
    if not current_user.is_superuser:
        logger.warning(f"Non-superuser attempted to create kabbalah user_id={current_user.id}")
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    payload = kabbalah_in.model_dump()
    logger.info(f"Creating kabbalah user_id={current_user.id} {payload=}")
    kabbalah = Kabbalah.model_validate(
        kabbalah_in,
        update={
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        },
    )
    session.add(kabbalah)
    try:
        session.commit()
        session.refresh(kabbalah)
        logger.info(f"Successfully created kabbalah kabbalah_id={kabbalah.id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError creating kabbalah {error_info}")
        if "kabbalot_middah_description_uq" in error_info:
            raise HTTPException(
                status_code=400,
                detail="Kabbalah already exists for this middah and description",
            )
        elif "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return kabbalah


@router.get("/{id}", response_model=KabbalahRead)
def get_kabbalah(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    logger.info(f"Fetching kabbalah user_id={current_user.id} kabbalah_id={id}")
    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        logger.warning(f"Kabbalah not found user_id={current_user.id} kabbalah_id={id}")
        raise HTTPException(status_code=404, detail="Kabbalah not found")
    return kabbalah


@router.patch("/{id}", response_model=KabbalahRead)
def patch_kabbalah(
    *, session: SessionDep, current_user: CurrentUser, id: int, patch: KabbalahPatch
) -> Any:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to patch kabbalah user_id={current_user.id} kabbalah_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        logger.warning(f"Kabbalah not found for patch kabbalah_id={id}")
        raise HTTPException(status_code=404, detail="Kabbalah not found")

    update_dict = patch.model_dump(exclude_unset=True)
    logger.info(f"Patching kabbalah user_id={current_user.id} kabbalah_id={id} {update_dict}")
    for k, v in update_dict.items():
        setattr(kabbalah, k, v)
    kabbalah.updated_at = datetime.now(timezone.utc)
    try:
        session.commit()
        session.refresh(kabbalah)
        logger.info(f"Successfully patched kabbalah kabbalah_id={id}")
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        logger.error(f"IntegrityError patching kabbalah kabbalah_id={id} {error_info}")
        if "kabbalot_middah_description_uq" in error_info:
            raise HTTPException(
                status_code=400,
                detail="Kabbalah already exists for this middah and description",
            )
        elif "foreign key constraint" in error_info.lower():
            raise HTTPException(status_code=400, detail="Invalid middah specified")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    return kabbalah


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_kabbalah(*, session: SessionDep, current_user: CurrentUser, id: int) -> Response:
    if not current_user.is_superuser:
        logger.warning(
            f"Non-superuser attempted to delete kabbalah user_id={current_user.id} kabbalah_id={id}"
        )
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    kabbalah = session.get(Kabbalah, id)
    if not kabbalah:
        logger.warning(f"Kabbalah not found for deletion kabbalah_id={id}")
        raise HTTPException(status_code=404, detail="Kabbalah not found")

    logger.info(f"Deleting kabbalah user_id={current_user.id} kabbalah_id={id}")
    session.delete(kabbalah)
    session.commit()
    logger.info(f"Successfully deleted kabbalah kabbalah_id={id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
