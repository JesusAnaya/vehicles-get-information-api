from pydantic import BaseModel


class VehicleSchema(BaseModel):
    vin: str
    make: str
    model: str
    year: str
    body_class: str
    cached_result: bool


class DeleteVehicleFromCacheSchema(BaseModel):
    vin: str
    cache_delete_success: bool
