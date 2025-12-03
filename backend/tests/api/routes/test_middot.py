from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.config import settings


def test_create_middah(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    data = {"name_transliterated": "test_ahavah", 
            "name_hebrew": "test_אהבה",
            "name_english": "test_love"}
    response = client.post(
        f"{settings.API_V1_STR}/middot/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name_transliterated"] == data["name_transliterated"]
    assert content["name_hebrew"] == data["name_hebrew"]
    assert content["name_english"] == data["name_english"]


def test_get_middah(   
    client: TestClient, superuser_token_headers: dict[str, str],  db: Session
) -> None:
    # First create a middah to read
    middah = crud.create_middah(
        session=db,
        middah_in={"name_transliterated": "test_emunah", 
        "name_hebrew": "test_אמונה",
        "name_english": "test_faith"}
    )
    response = client.get(
        f"{settings.API_V1_STR}/middot/{middah.name_transliterated}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name_transliterated"] == middah.name_transliterated
    assert content["name_hebrew"] == middah.name_hebrew
    assert content["name_english"] == middah.name_english


def test_list_middot(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/middot/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2


def test_delete_middah(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    # First create a middah to delete
    middah = crud.create_middah(
        session=db,
        middah_in={"name_transliterated": "test_simcha", 
        "name_hebrew": "test_שמחה",
        "name_english": "test_joy"}
    )
    response = client.delete(
        f"{settings.API_V1_STR}/middot/{middah.name_transliterated}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 204

    # Try to get the deleted middah
    response = client.get(
        f"{settings.API_V1_STR}/middot/{middah.name_transliterated}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404

    # List middot to ensure it's gone
    response = client.get(
        f"{settings.API_V1_STR}/middot/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2