from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Get a positionUpdate by supplying ship imo',
          feature_name="positionUpdate_by_imo.feature")
def test_positionUpdate_by_imo():
    pass


@pytest.fixture
@when('"<imo>" is provided as input')
def get_response(full_auth_client, imo):
    imos: list = imo.split(' ')
    imo_ints: list = [int(i) for i in imos]
    input_text = f"""(imo: {imo_ints})"""
    response: dict = full_auth_client.execute(get_query(input_text))
    return response, imo_ints


@then("a vessel will be returned with that imo")
def verify(get_response):
    data, imo_ints = get_response
    imo_response: list = nl('imo', data)
    for imo in imo_response:
        check.is_in(imo, imo_ints)

