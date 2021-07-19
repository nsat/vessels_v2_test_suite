from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query
import pytest_check as check
from nested_lookup import nested_lookup as nl


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Get a positionUpdate by supplying ship name',
          feature_name="positionUpdate_by_name.feature")
def test_positionUpdate_by_name():
    pass



@pytest.fixture
@when('"<vessel_name>" is provided as query input')
def get_response(full_auth_client, vessel_name):
    # parse vessel names
    vessel_names: list = vessel_name.split()
    input_text = f"""(name: {vessel_names})"""
    response = full_auth_client.execute(get_query(input_text=input_text))
    return response, vessel_names




@then("a vessel will be returned with that name")
def validate_names(get_response):
    data, names_input = get_response
    names_returned: list = nl('name', data)
    for name in names_returned:
        check.is_in(name, names_input)

