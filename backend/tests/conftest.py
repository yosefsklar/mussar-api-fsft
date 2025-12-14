from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import Item, User, Middah, ReminderPhrase, DailyText, Kabbalah, WeeklyText
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Item)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()   

# New approach for db_func fixture based testing
# kept the old version for prior writtern test modules
@pytest.fixture(scope="session", autouse=True)
def cleanup_db_before() -> Generator[None, None, None]:
    with Session(engine) as session:
        statement = delete(DailyText)
        session.execute(statement)
        statement = delete(Middah)
        session.execute(statement)
        session.commit()   
        yield

# New approach for db_func fixture based testing
# kept the old version for prior writtern test modules
@pytest.fixture(scope="session", autouse=True)
def cleanup_db_after() -> Generator[None, None, None]:
    yield
    # Teardown: cleanup after all tests complete
    # inverse order of FK dependencies
    with Session(engine) as session:
        statement = delete(DailyText)
        session.execute(statement)
        statement = delete(Middah)
        session.execute(statement)

        session.commit()   


@pytest.fixture(scope="function", autouse=True)
def db_func() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()



@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient) -> dict[str, str]:
    with Session(engine) as session:
        return authentication_token_from_email(
            client=client, email=settings.EMAIL_TEST_USER, db=session
        )
