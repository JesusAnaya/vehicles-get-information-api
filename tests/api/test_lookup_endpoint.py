from unittest.mock import MagicMock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from api.routers import get_vehicles_data_service
import pytest


expected_result = {
    "vin": "1XKWDB0X57J211825",
    "make": "Ford",
    "model": "Focus",
    "year": "2023",
    "body_class": "Sedan",
    "cached_result": False,
}


@pytest.fixture(scope="function")
def client_mock_ok(test_app: FastAPI) -> TestClient:
    async def mock_get_vehicles_data_service_ok():
        vehicles_data_service = MagicMock()
        vehicles_data_service.get_vehicle.return_value = expected_result
        return vehicles_data_service

    test_app.dependency_overrides[
        get_vehicles_data_service
    ] = mock_get_vehicles_data_service_ok

    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def client_mock_not_found(test_app: FastAPI) -> TestClient:
    async def mock_get_vehicles_data_service_not_found():
        vehicles_data_service = MagicMock()
        vehicles_data_service.get_vehicle.side_effect = HTTPException(status_code=404)
        return vehicles_data_service

    test_app.dependency_overrides[
        get_vehicles_data_service
    ] = mock_get_vehicles_data_service_not_found

    with TestClient(test_app) as test_client:
        yield test_client


# Test endpoint with a mocked service and a successful response
def test_lookup_vin_ok(client_mock_ok: TestClient):
    response = client_mock_ok.get("/api/v1/lookup/1XKWDB0X57J211825")
    assert response.status_code == 200
    assert response.json() == expected_result


# Test endpoint with a mocked service and a failed response
def test_lookup_vin_not_found(client_mock_not_found: TestClient):
    response = client_mock_not_found.get("/api/v1/lookup/1XKWDB0X57J211824")
    assert response.status_code == 404


# Test endpoint with a bad vin format
def test_lookup_vin_with_a_bad_vin_format(test_app: FastAPI):
    client = TestClient(test_app)
    response = client.get("/api/v1/lookup/1XK-DB0X-7J21-824")
    assert response.status_code == 422
