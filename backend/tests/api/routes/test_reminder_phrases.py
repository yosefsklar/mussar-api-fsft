from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.db import engine
from app.core.config import settings
from app.models import ReminderPhrase


def test_create_reminder_phrase(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # First create a middah to reference
    middah = crud.create_middah(
        session=db_func,
        middah_in={
            "name_transliterated": "test_emunah",
            "name_hebrew": "test_אמונה",
            "name_english": "test_faith",
        },
    )

    data = {
        "middah": middah.name_transliterated,
        "text": "Test reminder phrase text",
    }
    response = client.post(
        f"{settings.API_V1_STR}/reminder_phrases/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["middah"] == data["middah"]
    assert content["text"] == data["text"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content

    # Clean up
    crud.delete_reminder_phrase(
        session=Session(engine), reminder_phrase_id=content["id"]
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_get_reminder_phrase(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # First create a middah to reference
    middah = crud.create_middah(
        session=db_func,
        middah_in={
            "name_transliterated": "test_bitachon",
            "name_hebrew": "test_בטחון",
            "name_english": "test_trust",
        },
    )

    # Create a reminder phrase to read
    reminder_phrase = crud.create_reminder_phrase(
        session=db_func,
        reminder_phrase_in={
            "middah": middah.name_transliterated,
            "text": "Test reminder phrase for reading",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/reminder_phrases/{reminder_phrase.id}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == reminder_phrase.id
    assert content["middah"] == reminder_phrase.middah
    assert content["text"] == reminder_phrase.text

    # Clean up
    crud.delete_reminder_phrase(
        session=Session(engine), reminder_phrase_id=reminder_phrase.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_list_reminder_phrases(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # First create a middah to reference
    middah = crud.create_middah(
        session=db_func,
        middah_in={
            "name_transliterated": "test_ahavah",
            "name_hebrew": "test_אהבה",
            "name_english": "test_love",
        },
    )

    data1 = crud.create_reminder_phrase(
        session=db_func,
        reminder_phrase_in={
            "middah": middah.name_transliterated,
            "text": "Test reminder phrase 1",
        },
    )

    data2 = crud.create_reminder_phrase(
        session=db_func,
        reminder_phrase_in={
            "middah": middah.name_transliterated,
            "text": "Test reminder phrase 2",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/reminder_phrases/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

    # Clean up
    crud.delete_reminder_phrase(
        session=Session(engine), reminder_phrase_id=data1.id
    )
    crud.delete_reminder_phrase(
        session=Session(engine), reminder_phrase_id=data2.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_delete_reminder_phrase(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # First create a middah to reference
    middah = crud.create_middah(
        session=db_func,
        middah_in={
            "name_transliterated": "test_simcha",
            "name_hebrew": "test_שמחה",
            "name_english": "test_joy",
        },
    )

    # Create a reminder phrase to delete
    reminder_phrase = crud.create_reminder_phrase(
        session=db_func,
        reminder_phrase_in={
            "middah": middah.name_transliterated,
            "text": "Test reminder phrase to delete",
        },
    )
    response = client.delete(
        f"{settings.API_V1_STR}/reminder_phrases/{reminder_phrase.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Try to get the deleted reminder phrase
    response = client.get(
        f"{settings.API_V1_STR}/reminder_phrases/{reminder_phrase.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

    # List reminder phrases to ensure it's gone
    response = client.get(
        f"{settings.API_V1_STR}/reminder_phrases/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0

    # Clean up
    crud.delete_middah(
        session=Session(engine), name_transliterated=middah.name_transliterated
    )
