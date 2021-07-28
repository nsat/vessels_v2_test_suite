from pytest_bdd import scenario, when, then
import pytest
from helpers import get_port_query
import pytest_check as check
from nested_lookup import nested_lookup as nl

@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Valid port',
          feature_name="port_by_locode.feature")
def test_valid_locode():
    pass


@pytest.mark.short
@pytest.mark.negative_test
@scenario(scenario_name='Invalid port',
          feature_name="port_by_locode.feature")
def test_invalid_locode():
    pass

@pytest.fixture
@when('a "<UNLOCODE>" is provided for input')
def get_port(full_auth_client, UNLOCODE):
    input_text = f"""(unlocode: "{UNLOCODE}")"""
    try:
        response = full_auth_client.execute(get_port_query(input_text=input_text))
    except BaseException as e:
        return e
    return response


@then("valid data is returned")
def validate_data(get_port):
    data = get_port
    name = nl('name', data)
    check.is_true(name)
    unlocode = nl('unlocode',data)
    check.is_true(unlocode)
    latitude = nl('latitude', data)
    longitude = nl('longitude', data)
    check.is_true(latitude)
    check.is_true(longitude)


@then("an error response will be returned")
def validate_error(get_port):
    data = get_port
    check.is_in('exception', str(data))
