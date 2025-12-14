from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.db import engine
from app.core.config import settings
from app.models import Kabbalah


def test_create_kabbalah(
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
        "description": "Test kabbalah description",
    }
    response = client.post(
        f"{settings.API_V1_STR}/kabbalot/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["middah"] == data["middah"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content

    # Clean up
    crud.delete_kabbalah(
        session=Session(engine), kabbalah_id=content["id"]
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_get_kabbalah(
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

    # Create a kabbalah to read
    kabbalah = crud.create_kabbalah(
        session=db_func,
        kabbalah_in={
            "middah": middah.name_transliterated,
            "description": "Test kabbalah for reading",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/kabbalot/{kabbalah.id}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == kabbalah.id
    assert content["middah"] == kabbalah.middah
    assert content["description"] == kabbalah.description

    # Clean up
    crud.delete_kabbalah(
        session=Session(engine), kabbalah_id=kabbalah.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_list_kabbalot(
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

    data1 = crud.create_kabbalah(
        session=db_func,
        kabbalah_in={
            "middah": middah.name_transliterated,
            "description": "Test kabbalah 1",
        },
    )

    data2 = crud.create_kabbalah(
        session=db_func,
        kabbalah_in={
            "middah": middah.name_transliterated,
            "description": "Test kabbalah 2",
        },
    )
    response = client.get(
        f"{settings.API_V1_STR}/kabbalot/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

    # Clean up
    crud.delete_kabbalah(
        session=Session(engine), kabbalah_id=data1.id
    )
    crud.delete_kabbalah(
        session=Session(engine), kabbalah_id=data2.id
    )
    crud.delete_middah(session=Session(engine), name_transliterated=middah.name_transliterated)


def test_delete_kabbalah(
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

    # Create a kabbalah to delete
    kabbalah = crud.create_kabbalah(
        session=db_func,
        kabbalah_in={
            "middah": middah.name_transliterated,
            "description": "Test kabbalah to delete",
        },
    )
    response = client.delete(
        f"{settings.API_V1_STR}/kabbalot/{kabbalah.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Try to get the deleted kabbalah
    response = client.get(
        f"{settings.API_V1_STR}/kabbalot/{kabbalah.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

    # List kabbalot to ensure it's gone
    response = client.get(
        f"{settings.API_V1_STR}/kabbalot/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 0

    # Clean up
    crud.delete_middah(
        session=Session(engine), name_transliterated=middah.name_transliterated
    )
