from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.routers import get_db_session, router
import pytest


@pytest.fixture(scope="function")
def test_app(db_session) -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    return app


@pytest.fixture(scope="function")
def test_client(db_session: Session, test_app: FastAPI) -> TestClient:
    def override_get_db():
        yield db_session

    test_app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(test_app) as test_client:
        yield test_client
