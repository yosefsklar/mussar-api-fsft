import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    DailyText,
    DailyTextCreate,
    Item,
    ItemCreate,
    Kabbalah,
    KabbalahCreate,
    Middah,
    MiddahCreate,
    ReminderPhrase,
    ReminderPhraseCreate,
    User,
    UserCreate,
    UserUpdate,
    WeeklyText,
    WeeklyTextCreate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_middah(*, session: Session, middah_in: MiddahCreate) -> Middah:
    db_middah = Middah.model_validate(middah_in)
    session.add(db_middah)
    session.commit()
    session.refresh(db_middah)
    return db_middah

def delete_middah(*, session: Session, name_transliterated: str) -> None:
    middah = session.get(Middah, name_transliterated)
    if middah:
        session.delete(middah)
        session.commit()
    else:
        raise ValueError("Middah not found in db crud operation")

def create_reminder_phrase(
    *, session: Session, reminder_phrase_in: ReminderPhraseCreate
) -> ReminderPhrase:
    db_reminder_phrase = ReminderPhrase.model_validate(reminder_phrase_in)
    session.add(db_reminder_phrase)
    session.commit()
    session.refresh(db_reminder_phrase)
    return db_reminder_phrase


def create_daily_text(*, session: Session, daily_text_in: DailyTextCreate) -> DailyText:
    db_daily_text = DailyText.model_validate(daily_text_in)
    session.add(db_daily_text)
    session.commit()
    session.refresh(db_daily_text)
    return db_daily_text

def delete_daily_text(*, session: Session, daily_text_id: str) -> None:
    daily_text = session.get(DailyText, daily_text_id)
    if daily_text:
        session.delete(daily_text)
        session.commit()
    else:
        raise ValueError("DailyText not found in db crud operation")

def create_kabbalah(*, session: Session, kabbalah_in: KabbalahCreate) -> Kabbalah:
    db_kabbalah = Kabbalah.model_validate(kabbalah_in)
    session.add(db_kabbalah)
    session.commit()
    session.refresh(db_kabbalah)
    return db_kabbalah


def create_weekly_text(*, session: Session, weekly_text_in: WeeklyTextCreate) -> WeeklyText:
    db_weekly_text = WeeklyText.model_validate(weekly_text_in)
    session.add(db_weekly_text)
    session.commit()
    session.refresh(db_weekly_text)
    return db_weekly_text
