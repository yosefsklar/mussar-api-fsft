from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.db import engine
from app.core.config import settings
from app.models import WeeklyText


def test_create_weekly_text(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    data = {
        "sefaria_url": "https://www.sefaria.org/weekly1",
        "title": "Test Weekly Text Title",
        "content": "Test weekly text content",
    }
    response = client.post(
        f"{settings.API_V1_STR}/weekly_texts/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["sefaria_url"] == data["sefaria_url"]
    assert content["title"] == data["title"]
    assert content["content"] == data["content"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content

    # Clean up
    crud.delete_weekly_text(
        session=Session(engine), weekly_text_id=content["id"]
    )


def test_get_weekly_text(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # Create a weekly text to read
    weekly_text = crud.create_weekly_text(
        session=db_func,
        weekly_text_in={
            "sefaria_url": "https://www.sefaria.org/weekly2",
            "title": "Test Weekly Text",
            "content": "Test content for weekly text",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/weekly_texts/{weekly_text.id}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == weekly_text.id
    assert content["sefaria_url"] == weekly_text.sefaria_url
    assert content["title"] == weekly_text.title
    assert content["content"] == weekly_text.content

    # Clean up
    crud.delete_weekly_text(
        session=Session(engine), weekly_text_id=weekly_text.id
    )


def test_list_weekly_texts(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    data1 = crud.create_weekly_text(
        session=db_func,
        weekly_text_in={
            "sefaria_url": "https://www.sefaria.org/weekly3",
            "title": "Test Weekly Text 1",
            "content": "Test content 1",
        },
    )

    data2 = crud.create_weekly_text(
        session=db_func,
        weekly_text_in={
            "sefaria_url": "https://www.sefaria.org/weekly4",
            "title": "Test Weekly Text 2",
            "content": "Test content 2",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/weekly_texts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

    # Clean up
    crud.delete_weekly_text(
        session=Session(engine), weekly_text_id=data1.id
    )
    crud.delete_weekly_text(
        session=Session(engine), weekly_text_id=data2.id
    )


def test_delete_weekly_text(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # Create a weekly text to delete
    weekly_text = crud.create_weekly_text(
        session=db_func,
        weekly_text_in={
            "sefaria_url": "https://www.sefaria.org/weekly5",
            "title": "Test Weekly Text to Delete",
            "content": "Test content to delete",
        },
    )
    response = client.delete(
        f"{settings.API_V1_STR}/weekly_texts/{weekly_text.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Try to get the deleted weekly text
    response = client.get(
        f"{settings.API_V1_STR}/weekly_texts/{weekly_text.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

    # List weekly texts to ensure it's gone
    response = client.get(
        f"{settings.API_V1_STR}/weekly_texts/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0
