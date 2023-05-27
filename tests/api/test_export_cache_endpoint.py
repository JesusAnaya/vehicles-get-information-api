from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from tests.factories.vehicle_factory import VehicleModelFactory


def test_export_cache_endpoint(test_client: TestClient, db_session: Session):
    vehicle_model = VehicleModelFactory(vin="1XK6DB0X77J214824")
    db_session.add(vehicle_model)
    db_session.commit()

    response = test_client.get("/api/v1/export")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == "attachment; filename=filename.parquet"
