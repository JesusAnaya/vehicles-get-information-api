import factory
from factory.alchemy import SQLAlchemyModelFactory
from tests.common import SessionForTesting
from db.vehicles import VehicleModel


# This is a factory for creating VehicleModel objects, the factory_boy library generates
# data for populating the fields of the VehicleModel object, and create records in the
# database for testing. This class if only a resource for testing, and it is executed

class VehicleModelFactory(SQLAlchemyModelFactory):
    class Meta:
        model = VehicleModel
        sqlalchemy_session = SessionForTesting

    vin = '1XPWD40X1ED215307'
    make = 'Ford'
    model = 'Focus'
    year = '2023'
    body_class = 'Sedan'
