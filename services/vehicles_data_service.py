from sqlalchemy.orm import Session
from db.vehicles import VehicleModel
from resources.vpic_client import decode_vin
import pandas as pd
import io
import tempfile
import os


class VehiclesDataService(object):
    def __init__(self, session: Session):
        self.session = session

    def _read_vehicle_from_cache(self, vin: str) -> dict | None:
        vehicle = self.session.query(VehicleModel).filter_by(vin=vin).first()
        if vehicle is None:
            return None
        return vehicle.to_dict()

    def _save_vehicle_to_cache(self, vin: str, vehicle_data: dict):
        vehicle = VehicleModel(
            vin=vin,
            make=vehicle_data["make"],
            model=vehicle_data["model"],
            year=vehicle_data["year"],
            body_class=vehicle_data["body_class"],
        )
        self.session.add(vehicle)
        self.session.commit()

    def _retrieve_vehicle_from_vpic(self, vin: str) -> dict:
        return decode_vin(vin)

    def get_vehicle(self, vin: str) -> dict:
        vehicle_data = self._read_vehicle_from_cache(vin)

        if vehicle_data is None:
            vehicle_data = self._retrieve_vehicle_from_vpic(vin)
            self._save_vehicle_to_cache(vin, vehicle_data)
            vehicle_data["vin"] = vin
            vehicle_data["cached_result"] = False
        else:
            vehicle_data["cached_result"] = True

        return vehicle_data

    def remove_vehicle_from_cache(self, vin: str) -> bool:
        vehicle = self.session.query(VehicleModel).filter_by(vin=vin).first()
        if vehicle is None:
            return False

        self.session.delete(vehicle)
        self.session.commit()

        return True

    def export_cache(self) -> bytes:
        vehicles = self.session.query(VehicleModel).all()

        # Convert the SQLAlchemy objects to a DataFrame
        data = pd.DataFrame([res.to_dict() for res in vehicles])

        # Write the DataFrame to a temporary CSV file
        with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as temp_file:
            data.to_parquet(temp_file.name)

        # Read the CSV file into a BytesIO buffer
        with open(temp_file.name, "rb") as f:
            buffer = io.BytesIO(f.read())

        # Clean up the temporary file
        os.remove(temp_file.name)

        # Get the BytesIO object's byte content
        byte_content = buffer.getvalue()

        return byte_content
