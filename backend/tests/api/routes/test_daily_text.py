from fastapi.testclient import TestClient

from sqlmodel import Session

from app import crud
from app.core.config import settings


# def test_create_daily_text(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     data = {
#         "middah": "ahavah",
#         "title": "Messilat Yesharim - Love",
#         "content": "This is the daily text content.",
#         "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.1",

#     }
#     response = client.post(
#         f"{settings.API_V1_STR}/daily_texts/",
#         headers=superuser_token_headers,
#         json=data,
#     )
#     assert response.status_code == 200
#     content = response.json()
#     assert content["title"] == data["title"]
#     assert content["content"] == data["content"]
#     assert "id" in content
#     assert "created_at" in content
#     assert "updated_at" in content


# def test_create_daily_text_not_enough_permissions(
#     client: TestClient, normal_user_token_headers: dict[str, str]
# ) -> None:
#     data = {
#             "middah": "Yirah",
#             "title": "Messilat Yesharim - Fear",
#             "content": "This is the daily text content.",
#             "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.2",
#         }
#     response = client.post(
#         f"{settings.API_V1_STR}/daily_texts/",
#         headers=normal_user_token_headers,
#         json=data,
#     )
#     assert response.status_code == 403
#     content = response.json()
#     assert content["detail"] == "The user doesn't have enough privileges"


# def test_create_daily_text_invalid_middah(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     data = {
#             "middah": "invalid_middah",
#             "title": "Messilat Yesharim - Invalid",
#             "content": "This is the daily text content.",
#             "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.3",
#         }
#     response = client.post(
#         f"{settings.API_V1_STR}/daily_texts/",
#         headers=superuser_token_headers,
#         json=data,
#     )
#     assert response.status_code == 400
#     content = response.json()
#     assert content["detail"] == "Invalid middah specified"


# def test_get_daily_text(
#     client: TestClient, superuser_token_headers: dict[str, str], db: Session
# ) -> None:
#     # First create a daily text to read
#     daily_text = crud.create_daily_text(
#         session=db,
#         daily_text_in={
#             "middah": "Yirah",
#             "title": "Messilat Yesharim - Fear",
#             "content": "This is the daily text content.",
#             "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.2",
#         },
#     )
#     response = client.get(
#         f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
#         headers=superuser_token_headers,
#     )

#     assert response.status_code == 200
#     content = response.json()
#     assert content["id"] == str(daily_text.id)
#     assert content["title"] == daily_text.title
#     assert content["content"] == daily_text.content
#     assert content["sefaria_url"] == daily_text.sefaria_url
   

# def test_list_daily_texts(
#     client: TestClient, normal_user_token_headers: dict[str, str]
# ) -> None:
#     response = client.get(
#         f"{settings.API_V1_STR}/daily_texts/",
#         headers=normal_user_token_headers,
#     )
#     assert response.status_code == 200
#     content = response.json()
#     assert len(content)== 2


# def test_get_daily_text_not_found(
#     client: TestClient, normal_user_token_headers: dict[str, str]
# ) -> None:
#     response = client.get(
#         f"{settings.API_V1_STR}/daily_texts/9999",
#         headers=normal_user_token_headers,
#     )
#     assert response.status_code == 404
#     content = response.json()
#     assert content["detail"] == "Daily text not found"

# def test_patch_daily_text(
#     client: TestClient, superuser_token_headers: dict[str, str], db: Session
# ) -> None:
#     # First create a daily text to patch
#     daily_text = crud.create_daily_text(
#         session=db,
#         daily_text_in={
#             "middah": "savlanut",
#             "title": "Messilat Yesharim - Patience",
#             "content": "This is the daily text content.",
#             "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.3",
#         },
#     )
#     patch_data = {
#         "title": "Updated Title",
#         "content": "Updated content.",
#     }
#     response = client.patch(
#         f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
#         headers=superuser_token_headers,
#         json=patch_data,
#     )

#     assert response.status_code == 200
#     content = response.json()
#     assert content["id"] == str(daily_text.id)
#     assert content["title"] == patch_data["title"]
#     assert content["content"] == patch_data["content"]


# def test_patch_daily_text_not_found(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     patch_data = {
#         "title": "Updated Title",
#         "content": "Updated content.",
#     }
#     response = client.patch(
#         f"{settings.API_V1_STR}/daily_texts/9999",
#         headers=superuser_token_headers,
#         json=patch_data,
#     )
#     assert response.status_code == 404
#     content = response.json()
#     assert content["detail"] == "Daily text not found"


# def test_delete_daily_text(
#     client: TestClient, superuser_token_headers: dict[str, str], db: Session
# ) -> None:
#     # First create a daily text to delete
#     daily_text = crud.create_daily_text(
#         session=db,
#         daily_text_in={
#             "middah": "anavah",
#             "title": "Messilat Yesharim - Humility",
#             "content": "This is the daily text content.",
#             "sefaria_url": "https://www.sefaria.org/Messilat_Yesharim.1.4",
#         },
#     )
#     response = client.delete(
#         f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
#         headers=superuser_token_headers,
#     )
#     assert response.status_code == 204

#     # Try to get the deleted daily text
#     response = client.get(
#         f"{settings.API_V1_STR}/daily_texts/{daily_text.id}",
#         headers=superuser_token_headers,
#     )
#     assert response.status_code == 404

# def test_delete_daily_text_not_found(
#     client: TestClient, superuser_token_headers: dict[str, str]
# ) -> None:
#     response = client.delete(
#         f"{settings.API_V1_STR}/daily_texts/9999",
#         headers=superuser_token_headers,
#     )
#     assert response.status_code == 404
#     content = response.json()
#     assert content["detail"] == "Daily text not found"