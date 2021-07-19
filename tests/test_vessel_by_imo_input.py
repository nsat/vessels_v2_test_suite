from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import v1_request, get_query
import pytest_check as check



@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Execute query with imo input',
          feature_name="vessel_by_imo_input.feature")
def test_imo_input():
    pass


@pytest.fixture
@when('one or more "<imo>" are specified as given input')
def imo_input(full_auth_client, imo):
    i = imo.split(' ')
    inp = ' , '.join(i)
    input_text = f"""(imo: [{inp}]
    _limit: 1000)"""
    response: dict = full_auth_client.execute(get_query(input_text=input_text))
    return response, imo


@then("data matches vessel v1 data")
def validate(imo_input):
    v2, imo = imo_input
    check.is_true(v2)

    p_imo = imo.split(' ')
    p_imo = ','.join(p_imo)
    params = f'imo={p_imo}'
    v1 = v1_request(params=params)
    v1_imos: list = nl('imo', v1)
    v2_imos: list = nl('imo', v2)
    check.is_true(v2_imos)
    v1set = len(set(v1_imos))
    v2set = len(set(v2_imos))
    check.is_true(v2set >= v1set)

    for i in v1_imos:
        check.is_in(i, v2_imos)

    v2_mmsi: list = nl('mmsi', v2)
    check.is_true(v2_mmsi)
    # for m in v1_mmsi:
    #     check.is_in(m, v2_mmsi)
    # for m in v2_mmsi:
    #     check.is_in(m, v1_mmsi)
    # v1_names: list = nl('name', v1)
    # v2_names: list = nl('name', v2)
    # for n in v2_names:
    #     check.is_in(n, v1_names)
    # for n in v1_names:
    #     check.is_in(n, v2_names)
    # v1_calls: list = nl('call_sign', v1)
    # v2_calls: list = nl('callsign', v2)
    # for c in v2_calls:
    #     check.is_in(c, v1_calls)
    # for c in v1_calls:
    #     check.is_in(c, v2_calls)
    # v1_flags: list = nl('flag', v1)
    # v2_flags: list = nl('flag', v2)
    # for f in v2_flags:
    #     check.is_in(f, v1_flags)
    # for f in v1_calls:
    #     check.is_in(f, v2_flags)
