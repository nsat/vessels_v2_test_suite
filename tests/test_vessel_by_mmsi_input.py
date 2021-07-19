from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check

DATA = dict()



@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Execute query with mmsi input',
          feature_name="vessel_by_mmsi_input.feature")
def test_mmsi_input():
    pass


@pytest.fixture
@when('one or more "<mmsi>" are specified as input')
def mmsi_input(full_auth_client, mmsi: str):
    global DATA
    mmsis: list = mmsi.split(' ')
    mmsi_string = ','.join(mmsis)
    input_text = f"""(mmsi: [{mmsi_string}]
    _limit: 1000)"""
    response = full_auth_client.execute(get_query(input_text=input_text))
    DATA = response
    return response, mmsis


@then("mmsi returned match the mmsi input")
def verify(mmsi_input):
    data, mmsis_input = mmsi_input
    mmsis: list = nl('mmsi', data)
    for mmsi in mmsis:
        check.is_in(str(mmsi), mmsis_input)