from settings import settings
import requests


class NoVehicleFoundException(Exception):
    def __init__(self, message: str = "VIN not found"):
        super().__init__(message)


def decode_vin(vin: str) -> dict:
    host: str = settings.vpic_host
    url: str = f"{host}/api/vehicles/DecodeVinValues/{vin}?format=json"
    response = requests.get(url)

    if response.status_code != 200:
        raise NoVehicleFoundException()

    data: dict = response.json()

    if data["Count"] != 1:
        raise NoVehicleFoundException("Bad number of results")

    result: dict = data["Results"][0]

    return dict(
        make=result["Make"],
        model=result["Model"],
        year=result["ModelYear"],
        body_class=result["BodyClass"],
    )
