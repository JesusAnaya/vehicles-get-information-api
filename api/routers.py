import io
from typing import Annotated
from fastapi import APIRouter, Depends, Path
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from db.base import get_db_session
from services.vehicles_data_service import VehiclesDataService
from .schemas import VehicleSchema, DeleteVehicleFromCacheSchema

router = APIRouter()
VinAnnotated = Annotated[str, Path(max_length=17, min_length=17, regex=r"^[a-zA-Z0-9]*$")]


async def get_vehicles_data_service(db_session: Session = Depends(get_db_session)):
    yield VehiclesDataService(session=db_session)


@router.get("/lookup/{vin}", response_model=VehicleSchema)
async def lookup_vin(
    vin: VinAnnotated, vehicles_data_service: VehiclesDataService = Depends(get_vehicles_data_service)
):
    return vehicles_data_service.get_vehicle(vin=vin)


@router.post("/remove/{vin}", response_model=DeleteVehicleFromCacheSchema)
async def remove_vin(
    vin: VinAnnotated, vehicles_data_service: VehiclesDataService = Depends(get_vehicles_data_service)
):
    result: bool = vehicles_data_service.remove_vehicle_from_cache(vin=vin)

    return {
        "vin": vin,
        "cache_delete_success": result,
    }


@router.get("/export", response_class=StreamingResponse)
async def export_vehicles(vehicles_data_service: VehiclesDataService = Depends(get_vehicles_data_service)):
    byte_content: bytes = vehicles_data_service.export_cache()
    response = StreamingResponse(io.BytesIO(byte_content), media_type="application/octet-stream")
    response.headers["Content-Disposition"] = "attachment; filename=filename.parquet"
    return response
