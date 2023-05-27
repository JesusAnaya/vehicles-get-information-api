import pandas as pd
from sqlalchemy.orm import Session
from db.vehicles import VehicleModel
from services.vehicles_data_service import VehiclesDataService
from tests.factories.vehicle_factory import VehicleModelFactory
from unittest.mock import patch, MagicMock
import pytest
import io


# The vehicles_data_service fixture is used to create a VehiclesDataService object
# with a mocked database session for testing.

@pytest.fixture(scope="function")
def vehicles_data_service(db_session: Session):
    return VehiclesDataService(db_session)


# The test are going to validate the behavior of the VehiclesDataService class
# for successful and failed cases.

def test_read_vehicle_from_cache(db_session: Session, vehicles_data_service: VehiclesDataService):
    vin = "1XKWDB0X57J211825"
    expected_result = {
        "vin": "1XKWDB0X57J211825",
        "make": "Ford",
        "model": "Focus",
        "year": "2023",
        "body_class": "Sedan",
    }
    vehicle = VehicleModelFactory(vin=vin)
    db_session.add(vehicle)
    db_session.commit()

    result = vehicles_data_service._read_vehicle_from_cache(vin)

    assert result is not None
    assert result == expected_result


def test_read_vehicle_from_cache_does_not_exists(vehicles_data_service: VehiclesDataService):
    vin = "1XKWDB0X57J212345"
    vehicle_data = vehicles_data_service._read_vehicle_from_cache(vin)

    assert vehicle_data is None


def test_save_vehicle_to_cache(db_session: Session, vehicles_data_service: VehiclesDataService):
    vehicle_info = {
        "vin": "1XKWDB0X57J211825",
        "make": "Ford",
        "model": "Focus",
        "year": "2023",
        "body_class": "Sedan",
    }

    vehicles_data_service._save_vehicle_to_cache(vehicle_info["vin"], vehicle_info)

    vehicle = db_session.query(VehicleModel).filter_by(vin=vehicle_info["vin"]).first()

    assert vehicle is not None
    assert vehicle.vin == vehicle_info["vin"]
    assert vehicle.make == vehicle_info["make"]
    assert vehicle.model == vehicle_info["model"]
    assert vehicle.year == vehicle_info["year"]
    assert vehicle.body_class == vehicle_info["body_class"]


def test_retrieve_vehicle_from_vpic(vehicles_data_service: VehiclesDataService):
    with patch("services.vehicles_data_service.decode_vin") as mocked_decode_vin:
        vehicles_data_service._retrieve_vehicle_from_vpic("1XKWDB0X57J298765")

        # assert that decode_vin was called
        mocked_decode_vin.assert_called_once()


@patch("services.vehicles_data_service.decode_vin")
def test_get_from_cache(mocked_decode_vin: MagicMock, vehicles_data_service: VehiclesDataService):
    vin = "1XKWDB0X57J211825"
    expected_result = {
        "vin": "1XKWDB0X57J211825",
        "make": "Ford",
        "model": "Focus",
        "year": "2023",
        "body_class": "Sedan",
        "cached_result": True,
    }

    # This patch changes the behavior of the _retrieve_vehicle_from_vpic method
    mocked_decode_vin.return_value = expected_result

    result = vehicles_data_service.get_vehicle(vin)

    assert result is not None
    assert result == expected_result


@patch("services.vehicles_data_service.VehiclesDataService._save_vehicle_to_cache")
@patch("services.vehicles_data_service.VehiclesDataService._retrieve_vehicle_from_vpic")
@patch("services.vehicles_data_service.VehiclesDataService._read_vehicle_from_cache")
def test_get_from_vpic_api(
    mocked_read_vehicle_from_cache: MagicMock,
    mocked_retrieve_vehicle_from_vpic: MagicMock,
    mocked_save_vehicle_to_cache: MagicMock,
    vehicles_data_service: VehiclesDataService,
):
    vin = "1XKWDB0X57J211825"
    vehicle_info = {
        "make": "Ford",
        "model": "Focus",
        "year": "2023",
        "body_class": "Sedan",
    }

    # This is the expected result
    expected_result = {
        "vin": vin,
        "cached_result": False,
    }
    expected_result.update(vehicle_info)

    # This patch changes the behavior of the _read_vehicle_from_cache method
    mocked_read_vehicle_from_cache.return_value = None
    # This patch changes the behavior of the _retrieve_vehicle_from_vpic method
    mocked_retrieve_vehicle_from_vpic.return_value = vehicle_info

    result = vehicles_data_service.get_vehicle(vin)

    assert result is not None
    assert result == expected_result

    # assert that _save_vehicle_to_cache was called correctly
    mocked_save_vehicle_to_cache.assert_called_with(vin, vehicle_info)


def test_remove_vehicle_from_cache(db_session: Session, vehicles_data_service: VehiclesDataService):
    vin = "1XKWDB0X57J211825"
    vehicle = VehicleModelFactory(vin=vin)
    db_session.add(vehicle)
    db_session.commit()

    response = vehicles_data_service.remove_vehicle_from_cache(vin)

    vehicle = db_session.query(VehicleModel).filter_by(vin=vin).first()

    assert vehicle is None
    assert response is True


def test_remove_vehicle_from_cache_does_not_exists(
    db_session: Session, vehicles_data_service: VehiclesDataService
):
    vin = "1XKWDB0X57J211825"

    response = vehicles_data_service.remove_vehicle_from_cache(vin)

    assert response is False


def test_export_cache_to_parquet(vehicles_data_service: VehiclesDataService, db_session: Session):
    vehicle_model = VehicleModelFactory(vin="1XKWDB0X57J211825")
    db_session.add(vehicle_model)
    db_session.commit()

    result_bytes = vehicles_data_service.export_cache()

    assert isinstance(result_bytes, bytes)

    # Read the parquet file and check that the data is correct
    result = io.BytesIO(result_bytes)
    result.seek(0)
    df = pd.read_parquet(result)

    assert not df.empty
