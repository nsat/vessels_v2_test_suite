from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check
from loguru import logger


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Single request for each shipType',
          feature_name="vessel_by_shipType_input.feature")
def test_single_type():
    pass

@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='More than one shipType is specified as input',
          feature_name="vessel_by_shipType_input.feature")
def test_multi_types():
    pass

@pytest.fixture
@when('a "<shipType>" is specified for query input')
def get_single_shipType_response(full_auth_client, shipType):
    response: dict
    client = full_auth_client
    input_text: str = f'(shipType: "{shipType}" _limit: 1000)'
    try:
        response = client.execute(get_query(input_text))
    except BaseException as e:
        logger.error(e)
        raise
    return response, shipType


@then("the response will contain only that shipType")
def validate_ship_type(get_single_shipType_response):
    response: dict
    shipType: str
    response, shipType = get_single_shipType_response
    shipTypes: list = nl('shipType', response)

    for s_type in shipTypes:
        if s_type != shipType:
            logger.error(f"LOOKING FOR {shipType}")
            logger.error(f"FOUND THIS ONE INSTEAD: {s_type}\n")
            logger.error(response)
        check.is_true(s_type == shipType)


@pytest.fixture
@when('"<shipTypes>" are specified')
def get_multi_shipTypes_response(full_auth_client, shipTypes):
    response: dict
    ship_list: list = shipTypes.split()
    string = ''
    for ship in ship_list:
        string+= f'"{ship}",'
    input_text: str = f'(shipType: [{string}] _limit: 1000)'
    try:
        response = full_auth_client.execute(get_query(input_text))
    except BaseException as e:
        logger.error(e)
        raise
    return response, ship_list


@then("the response will contain only those shipType(s)")
def validate_ship_types(get_multi_shipTypes_response):
    response: dict
    ship_list: list
    response, ship_list = get_multi_shipTypes_response
    result_shipTypes: list = nl('shipType', response)
    for s_type in result_shipTypes:
        check.is_in(s_type, ship_list)
