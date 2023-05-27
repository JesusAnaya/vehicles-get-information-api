from sqlalchemy.orm import Session
from db.vehicles import VehicleModel
from tests.factories.vehicle_factory import VehicleModelFactory


# In this test, I'm testing the creation of a VehicleModel object,
# and the interaction with the database through the ORM.


def test_vin_creation(db_session: Session):
    vehicle_model = VehicleModelFactory()
    db_session.add(vehicle_model)
    db_session.commit()

    retrieved_vehicle_model = (
        db_session.query(VehicleModel).filter_by(vin=vehicle_model.vin).first()
    )

    assert retrieved_vehicle_model is not None
    assert retrieved_vehicle_model.vin == vehicle_model.vin
    assert retrieved_vehicle_model.make == vehicle_model.make
    assert retrieved_vehicle_model.model == vehicle_model.model
    assert retrieved_vehicle_model.year == vehicle_model.year
    assert retrieved_vehicle_model.body_class == vehicle_model.body_class


def test_vin_to_dict(db_session: Session):
    vehicle_model = VehicleModelFactory()
    db_session.add(vehicle_model)
    db_session.commit()

    retrieved_vehicle_model = (
        db_session.query(VehicleModel).filter_by(vin=vehicle_model.vin).first()
    )
    serialized_vehicle_model = retrieved_vehicle_model.to_dict()

    expected_result = {
        "vin": "1XPWD40X1ED215307",
        "make": "Ford",
        "model": "Focus",
        "year": "2023",
        "body_class": "Sedan",
    }

    assert serialized_vehicle_model == expected_result
