from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check

@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Request positionUpdates with callsign as input',
          feature_name="positionUpdate_by_callsign.feature")
def test_positionUpdate_by_callsign():
    pass


@pytest.fixture
@when('"<callsign>" input is provided to query')
def get_response(full_auth_client, callsign):
    calls: list = callsign.split()
    input_text = f"""(callsign: {calls})"""
    response = full_auth_client.execute(get_query(input_text))
    return response, calls


@then("the response will contain those callsigns")
def verify(get_response):
    data, calls_input = get_response
    calls_returned:list = nl('callsign', data)
    for call in calls_returned:
        check.is_in(call, calls_input)

