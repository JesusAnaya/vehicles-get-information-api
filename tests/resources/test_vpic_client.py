from unittest.mock import patch
import pytest
from resources.vpic_client import decode_vin, NoVehicleFoundException

# The goal of this test is to ensure that the decode_vin function is working as expected.
# The call to the external API is mocked using the patch decorator.
# The expected response is defined in the expected_response variable.
# This is the response that the external API will return.

expected_response: dict = {
    "Count": 1,
    "Message": "Results returned successfully...",
    "SearchCriteria": "VIN...",
    "Results": [
        {
            "BodyClass": "Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)",
            "Make": "BMW",
            "Model": "X3",
            "ModelYear": "2011",
        }
    ],
}


def test_vin_decode_by_vpic():
    with patch("requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = expected_response

        response = decode_vin("1XPWD40X1ED215307")

    assert response == {
        "make": "BMW",
        "model": "X3",
        "year": "2011",
        "body_class": "Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)",
    }


def test_vin_decode_raise_error_if_status_code_is_not_200():
    with patch("requests.get") as mocked_get:
        mocked_get.return_value.status_code = 404

        with pytest.raises(NoVehicleFoundException) as exc_info:
            try:
                decode_vin("1XPWD40X1ED215307")
            except NoVehicleFoundException as e:
                raise e
            except Exception:
                pytest.fail("Unexpected exception")

        assert exc_info.type == NoVehicleFoundException
        assert str(exc_info.value) == "VIN not found"


def test_vin_decode_raise_error_for_wrong_number_of_results():
    with patch("requests.get") as mocked_get:
        mocked_get.return_value.status_code = 200
        mocked_get.return_value.json.return_value = {"Count": 0}

        with pytest.raises(NoVehicleFoundException) as exc_info:
            try:
                decode_vin("1XPWD40X1ED215307")
            except NoVehicleFoundException as e:
                raise e
            except Exception:
                pytest.fail("Unexpected exception")

        assert exc_info.type == NoVehicleFoundException
        assert str(exc_info.value) == "Bad number of results"
