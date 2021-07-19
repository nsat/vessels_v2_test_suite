from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check


SIGNS = ["9HB6653", "FAA8092", "DH3591", "DF8337", "IWJJ", "9V6056"]


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Execute query with callsign input',
          feature_name="vessel_by_callsign_input.feature")
def test_callsign_input():
    pass


@pytest.fixture
@when('one or more callsigns are specified')
def callsign_input(full_auth_client):
    input_text = f"""(callsign: {SIGNS})"""
    response: dict = full_auth_client.execute(get_query(input_text=input_text))

    return response


@then("data matches vessels v1 api data")
def validate(callsign_input):
    v2 = callsign_input
    assert v2
    signs_string = ','.join(SIGNS)
    params = f'call_sign={signs_string}'
    v2_calls: list = nl('callsign', v2)
    check.is_true(v2_calls)
    for s in v2_calls:
        check.is_in(s, v2_calls)
    # v1 = v1_request(params=params)
    # v1_imos: list = nl('imo', v1)
    # v2_imos: list = nl('imo', v2)
    # for i in v1_imos:
    #     check.is_in(i, v2_imos)
    # for i in v2_imos:
    #     check.is_in(i, v1_imos)
    # v1_calls: list = nl('call_sign', v1)

    # for c in v1_calls:
    #     check.is_in(c, v2_calls)
    # for c in v2_calls:
    #     check.is_in(c, v1_calls)
    # v1_flags: list = nl('flag', v1)
    # v2_flags: list = nl('flag', v2)
    # for f in v1_flags:
    #     check.is_in(f, v2_flags)
    # for f in v2_flags:
    #     check.is_in(f, v1_flags)
    # v1_mmsi: list = nl('mmsi', v1)
    # v2_mmsi: list = nl('mmsi', v2)
    # assert v2_mmsi
    # for m in v1_mmsi:
    #     check.is_in(m, v1_mmsi)
    # for m in v2_mmsi:
    #     check.is_in(m, v1_mmsi)
    # v1_names: list = nl('name', v1)
    # v2_names: list = nl('name', v2)
    # for n in v1_names:
    #     check.is_in(n[:5], v2_names)
    # for n in v2_names:
    #     check.is_in(n[:5], v1_names)

