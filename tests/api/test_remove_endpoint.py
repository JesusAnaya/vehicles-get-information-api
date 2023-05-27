from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.factories.vehicle_factory import VehicleModelFactory


def test_remove_vehicle_from_cache_by_vin(test_client: TestClient, db_session: Session):
    vehicle_model = VehicleModelFactory(vin="1XK6DB0X77J214824")
    db_session.add(vehicle_model)
    db_session.commit()

    response = test_client.post("/api/v1/remove/1XK6DB0X77J214824")
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XK6DB0X77J214824",
        "cache_delete_success": True,
    }


def test_try_to_remove_vehicle_from_cache_if_it_does_not_exists(test_client: TestClient):
    response = test_client.post("/api/v1/remove/1XK6DB0X77J214824")
    assert response.status_code == 200
    assert response.json() == {
        "vin": "1XK6DB0X77J214824",
        "cache_delete_success": False,
    }
