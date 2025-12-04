from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.db import engine
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

    crud.delete_middah(
        session=Session(engine),
        name_transliterated=data["name_transliterated"]
    )


def test_get_middah(   
    client: TestClient, superuser_token_headers: dict[str, str],  db_func: Session
) -> None:
    # First create a middah to read
    data = crud.create_middah(
        session=db_func,
        middah_in={"name_transliterated": "test_emunah", 
        "name_hebrew": "test_אמונה",
        "name_english": "test_faith"}
    )
    response = client.get(
        f"{settings.API_V1_STR}/middot/{data.name_transliterated}",
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name_transliterated"] == data.name_transliterated
    assert content["name_hebrew"] == data.name_hebrew
    assert content["name_english"] == data.name_english

    crud.delete_middah(
        session=Session(engine),
        name_transliterated=data.name_transliterated
    )


def test_list_middot(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    data1 = crud.create_middah(
        session=db_func,
        middah_in={"name_transliterated": "test_emunah", 
        "name_hebrew": "test_אמונה",
        "name_english": "test_faith"}
    )

    data2 = crud.create_middah(
        session=db_func,
        middah_in={"name_transliterated": "test_ahavah", 
                "name_hebrew": "test_אהבה",
                "name_english": "test_love"}
    )
    response = client.get(
        f"{settings.API_V1_STR}/middot/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) == 2

    crud.delete_middah(
        session=Session(engine),
        name_transliterated=data1.name_transliterated
    )
    crud.delete_middah(
        session=Session(engine),
        name_transliterated=data2.name_transliterated
    )


def test_delete_middah(
    client: TestClient, superuser_token_headers: dict[str, str], db_func: Session
) -> None:
    # First create a middah to delete
    middah = crud.create_middah(
        session=db_func,
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
    assert len(content) == 0