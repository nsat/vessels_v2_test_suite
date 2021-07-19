from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_matched_port_query
import pytest_check as check

@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='text supplied meets regex requirements',
          feature_name="matchedPort.feature")
def test_valid_input():
    pass


@pytest.mark.short
@pytest.mark.negative_test
@scenario(scenario_name='text supplied does not meet regex requirements',
          feature_name="matchedPort.feature")
def test_invalid_input():
    pass


@pytest.fixture
@when('search "<text>" is provided')
def get_response(full_auth_client, text):
    input_text = f"""(text: "{text}")"""
    try:
        response = full_auth_client.execute(get_matched_port_query(input_text=input_text))
    except BaseException as e:
        return e
    return response


@then("data is returned")
def validate_response(get_response):
    data = get_response
    matchScore = data['matchedPort']['matchScore']
    check.is_true(matchScore)
    name = nl('name', data)
    check.is_not_none(name)
    unlocode = nl('unlocode', data)
    check.is_not_none(unlocode)
    latitude = nl('latitude', data)
    longitude = nl('longitude', data)
    check.is_instance(longitude[0], float)
    check.is_instance(latitude[0], float)


@then("valid error is returned")
def validate_error(get_response):
    message = get_response
    check.is_in('exception', str(message))
