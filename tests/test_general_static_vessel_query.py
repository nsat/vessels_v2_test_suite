from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
from datetime import datetime



@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Execute a vessels query',
          feature_name="general_static_vessel_query.feature")
def test_generic_vessel_query():
    pass



@pytest.fixture
@when("a vessels query is executed")
def vessel_query(full_auth_client):
    return full_auth_client.execute(get_query())


@then("results are returned")
def validate(vessel_query):
    # is data returned?
    data = vessel_query
    assert data
    mmsis: list = nl('mmsi', data)
    stamps: list = nl('timestamp', data)
    # recieved 'required' data
    assert mmsis
    assert stamps
    # data is of correct length / number of digits
    for mmsi in mmsis:
        assert str(mmsi).isdigit()
    for stamp in stamps:
        try:
            datetime.strptime(stamp,  "%Y-%m-%dT%H:%M:%S.%fZ")
        except Exception:
            assert False

