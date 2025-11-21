import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# =============================================================
# New domain models per CRUD specification
# =============================================================


# --------------------------- Middot ---------------------------
class MiddahAttributes(SQLModel):
    name_transliterated: str = Field(max_length=80)
    name_hebrew: str = Field(max_length=80)
    name_english: str = Field(max_length=80)


class MiddahCreate(MiddahAttributes):
    pass


class MiddahRead(MiddahAttributes):
    pass


class Middah(SQLModel, table=True):
    __tablename__ = "middot"
    name_transliterated: str = Field(primary_key=True, max_length=80)
    name_hebrew: str = Field(max_length=80, unique=True, nullable=False)
    name_english: str = Field(max_length=80, unique=True, nullable=False)


# ---------------------- Reminder Phrases ----------------------
class ReminderPhraseAttributes(SQLModel):
    middah: str = Field(max_length=80)
    text: str


class ReminderPhraseCreate(ReminderPhraseAttributes):
    pass


class ReminderPhraseRead(ReminderPhraseAttributes):
    id: int
    created_at: datetime
    updated_at: datetime


class ReminderPhrasePatch(SQLModel):
    middah: str | None = Field(default=None, max_length=80)
    text: str | None = None


class ReminderPhrase(SQLModel, table=True):
    __tablename__ = "reminder_phrases"
    __table_args__ = (
        UniqueConstraint("middah", "text", name="reminder_phrases_middah_text_uq"),
    )
    id: int | None = Field(default=None, primary_key=True)
    middah: str = Field(
        foreign_key="middot.name_transliterated", max_length=80, nullable=False
    )
    text: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


# ------------------------- Daily Texts ------------------------
class DailyTextAttributes(SQLModel):
    # Required keys, values may be null
    middah: str = Field(max_length=80)
    sefaria_url: str | None
    title: str | None
    content: str | None


class DailyTextCreate(DailyTextAttributes):
    pass


class DailyTextRead(DailyTextAttributes):
    id: int
    created_at: datetime
    updated_at: datetime


class DailyTextPatch(SQLModel):
    middah: str | None = Field(default=None, max_length=80)
    sefaria_url: str | None = None
    title: str | None = None
    content: str | None = None


class DailyText(SQLModel, table=True):
    __tablename__ = "daily_texts"
    id: int | None = Field(default=None, primary_key=True)
    middah: str = Field(
        foreign_key="middot.name_transliterated", max_length=80, nullable=False
    )
    sefaria_url: str | None = Field(default=None, unique=True)
    title: str | None = None
    content: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


# -------------------------- Kabbalot --------------------------
class KabbalahAttributes(SQLModel):
    middah: str = Field(max_length=80)
    description: str


class KabbalahCreate(KabbalahAttributes):
    pass


class KabbalahRead(KabbalahAttributes):
    id: int
    created_at: datetime
    updated_at: datetime


class KabbalahPatch(SQLModel):
    middah: str | None = Field(default=None, max_length=80)
    description: str | None = None


class Kabbalah(SQLModel, table=True):
    __tablename__ = "kabbalot"
    __table_args__ = (
        UniqueConstraint(
            "middah", "description", name="kabbalot_middah_description_uq"
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    middah: str = Field(
        foreign_key="middot.name_transliterated", max_length=80, nullable=False
    )
    description: str = Field(nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


# ------------------------- Weekly Texts -----------------------
class WeeklyTextAttributes(SQLModel):
    # Required keys, values may be null
    sefaria_url: str | None
    title: str | None
    content: str | None


class WeeklyTextCreate(WeeklyTextAttributes):
    pass


class WeeklyTextRead(WeeklyTextAttributes):
    id: int
    created_at: datetime
    updated_at: datetime


class WeeklyTextPatch(SQLModel):
    sefaria_url: str | None = None
    title: str | None = None
    content: str | None = None


class WeeklyText(SQLModel, table=True):
    __tablename__ = "weekly_texts"
    id: int | None = Field(default=None, primary_key=True)
    sefaria_url: str | None = Field(default=None, unique=True)
    title: str | None = None
    content: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
