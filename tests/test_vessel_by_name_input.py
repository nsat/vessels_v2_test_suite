from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import v1_request, get_query
import pytest_check as check

NAMES = ['YUZHOUFENGSHUNJI 003', 'RHUMB DO', 'MINQUAN', 'SY GOF',  'FISH AND CHILL', 'ROOKE']


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Execute query with vessel name input',
          feature_name="vessel_by_name_input.feature")
def test_name_input():

    pass

@pytest.fixture
@when("one or more vessel names are specified as input")
def name_input(full_auth_client):
    input_text = f"""(name: ["YUZHOUFENGSHUNJI 003", "RHUMB DO", "MINQUAN", "SY GOF",  "FISH AND CHILL", "ROOKE"]
      _limit: 1000)"""
    response = full_auth_client.execute(get_query(input_text=input_text))
    return response


@then("data matches v1 data")
def validate(name_input):
    v2: dict = name_input
    assert v2
    params: str = f'name={NAMES}'
    v1: dict = v1_request(params=params)
    # v1_imos: list = nl('imo', v1)
    # v2_imos: list = nl('imo', v2)
    # for i in v1_imos:
    #     assert i in v2_imos
    # v1_calls: list = nl('callsign', v1)
    # v2_calls: list = nl('callsign', v2)
    # for c in v1_calls:
    #     assert c in v2_calls
    # v1_flags: list = nl('flag', v1)
    # v2_flags: list = nl('flag', v2)
    # for f in v1_flags:
    #     assert f in v2_flags
    # v1_mmsi: list = nl('mmsi', v1)
    # v2_mmsi: list = nl('mmsi', v2)
    # assert v2_mmsi
    # for m in v1_mmsi:
    #     assert m in v2_mmsi
    v1_names: list = nl('name', v1)
    v2_names: list = nl('name', v2)
    check.is_true(v2_names)
    for n in v2_names:
        check.is_in(n, NAMES)
    for n in v1_names:
        check.is_in(n, v1_names)

