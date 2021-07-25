from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_matched_port_query
import pytest_check as check
from loguru import logger

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
    e = ''
    try:
        response = full_auth_client.execute(get_matched_port_query(input_text=input_text))
    except BaseException as e:
        return e
    return response, str(e)


@then("data is returned")
def validate_response(get_response):
    data: tuple = get_response
    matchedPort = data[0]['matchedPort']
    matchScore = matchedPort['matchScore']
    check.is_true(matchScore)
    matchScore_is_float: bool = isinstance(matchScore, float)
    matchScore_is_int: bool = isinstance(matchScore, int)
    check.is_true(matchScore_is_float or matchScore_is_int)
    port = matchedPort['port']
    name = port['name']
    unlocode = port['unlocode']
    try:
        latitude = port['centerPoint']['latitude']
        longitude = port['centerPoint']['longitude']
    except TypeError:
        logger.error(f"BAD DATA? {data}")
    if not unlocode:
        logger.error(f"FAILED FOR UNLOCODE:\n {data}")
    check.is_not_none(unlocode)
    if not name:
        logger.error(f"FAILED ON NAME: \n{data}")
    check.is_not_none(name)
    longitude_is_float: bool = isinstance(longitude, float)
    latitude_is_float: bool = isinstance(longitude, float)
    if not latitude or not longitude:
        logger.error(f"FAILED ON LAT/LONG\n{data}")

    check.is_true(latitude_is_float)
    check.is_true(longitude_is_float)




@then("valid error is returned")
def validate_error(get_response):
    message = get_response
    check.is_in('exception', str(message))
