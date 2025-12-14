from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.db import engine
from app.core.config import settings
from app.models import DailyText


def test_create_daily_text(
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
        "sefaria_url": "https://www.sefaria.org/test1",
        "title": "Test Daily Text Title",
        "content": "Test daily text content",
    }
    response = client.post(
        f"{settings.API_V1_STR}/daily_texts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["middah"] == data["middah"]
    assert content["sefaria_url"] == data["sefaria_url"]
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content

    # Clean up
    crud.delete_daily_text(
        session=Session(engine), daily_text_id=content["id"]
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_get_daily_text(
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

    # Create a daily text to read
    daily_text = crud.create_daily_text(
        session=db_func,
        daily_text_in={
            "middah": middah.name_transliterated,
            "sefaria_url": "https://www.sefaria.org/test2",
            "title": "Test Daily Text",
            "content": "Test content for daily text",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == daily_text.id
    assert content["middah"] == daily_text.middah
    assert content["sefaria_url"] == daily_text.sefaria_url
    assert content["title"] == daily_text.title
    assert content["content"] == daily_text.content

    # Clean up
    crud.delete_daily_text(
        session=Session(engine), daily_text_id=daily_text.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_list_daily_texts(
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

    data1 = crud.create_daily_text(
        session=db_func,
        daily_text_in={
            "middah": middah.name_transliterated,
            "sefaria_url": "https://www.sefaria.org/test3",
            "title": "Test Daily Text 1",
            "content": "Test content 1",
        },
    )

    data2 = crud.create_daily_text(
        session=db_func,
        daily_text_in={
            "middah": middah.name_transliterated,
            "sefaria_url": "https://www.sefaria.org/test4",
            "title": "Test Daily Text 2",
            "content": "Test content 2",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/daily_texts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

    # Clean up
    crud.delete_daily_text(
        session=Session(engine), daily_text_id=data1.id
    )
    crud.delete_daily_text(
        session=Session(engine), daily_text_id=data2.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_delete_daily_text(
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

    # Create a daily text to delete
    daily_text = crud.create_daily_text(
        session=db_func,
        daily_text_in={
            "middah": middah.name_transliterated,
            "sefaria_url": "https://www.sefaria.org/test5",
            "title": "Test Daily Text to Delete",
            "content": "Test content to delete",
        },
    )
    response = client.delete(
        f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Try to get the deleted daily text
    response = client.get(
        f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

    # List daily texts to ensure it's gone
    response = client.get(
        f"{settings.API_V1_STR}/daily_texts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0

    # Clean up
    crud.delete_middah(
        session=Session(engine), name_transliterated=middah.name_transliterated
    )
