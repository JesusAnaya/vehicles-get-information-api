from sqlalchemy import Column, String
from db.base import Base


class VehicleModel(Base):
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    year = Column(String)
    body_class = Column(String)

    def to_dict(self) -> dict:
        return dict(
            vin=self.vin,
            make=self.make,
            model=self.model,
            year=self.year,
            body_class=self.body_class
        )
