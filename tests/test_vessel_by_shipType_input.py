from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
from loguru import logger
import pytest_check as check

DATA: list = list()


@pytest.mark.long
@pytest.mark.positive_test
@scenario(scenario_name='Execute a query for one or more shipType(s)',
          feature_name="vessel_by_shipType_input.feature")
def test_ship_type_input():
    pass


@pytest.fixture
@when("one or more shipType(s) are specified for input")
def ship_type_input(full_auth_client):
    return full_auth_client


@then("the results will include the shipType specified and no other")
def validate(ship_type_input):
    global DATA
    client = ship_type_input
    # valid ship types
    shipType_input: str
    for i in range(0, 100):
        if i <= 9:
            shipType_input = f"0{i}"
        else:
            shipType_input = f"{i}"
        input_text = f"""(shipType: ["{shipType_input}"]
        _limit: 1000)"""
        v2 = client.execute(get_query(input_text=input_text))
        v2_vessels: list = nl('vessel', v2)
        for vessel in v2_vessels:
            pretty: str = str()
            for k, v in vessel.items():
                if v:
                    pretty += f'{k}:{v}\n'
            shipType_response = vessel['shipType']
            check.is_true(shipType_response)
            if not shipType_response == shipType_input:
                logger.error(f"""
                shipType_input: {shipType_input}
                vessel: 
                
                {pretty}
                """)
            check.is_in(shipType_response, shipType_input)
