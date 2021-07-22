from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check

FLAGS = ["UZ", "ES", "TW", "CN", "US"]



@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Execute query with one or more flag values as input',
          feature_name="vessel_by_flag_input.feature")
def test_flag_input():
    pass



@pytest.fixture
@when("one or more flag values are specified in the query")
def flag_input(full_auth_client):
    input_text = f"""(flag: {FLAGS})"""
    response: dict = full_auth_client.execute(get_query(input_text=input_text))
    return response


@then("the result matches v1")
def verify(flag_input):
    assert flag_input
    # params = f'flag={FLAGS}'
    # v1 = v1_request(params=params)
    # v1_flags = nl('flag', v1)
    # v1_flags = [flag for flag in v1_flags if flag]  # remove None
    v2 = flag_input
    v2_flags = nl('flag', v2)
    assert v2_flags
    for flag in v2_flags:
        check.is_in(flag, FLAGS)
        #check.is_in(flag, v1_flags)
    # for flag in v2_flags:
    #     check.is_in(flag, v1_flags)
    # v1_mmsi = nl('mmsi', v1)
    # v1_mmsi = [i for i in v1_mmsi if i]  # remove None
    # v2_mmsi = nl('mmsi', v2)
    # assert v2_mmsi
    # for mmsi in v2_mmsi:
    #     check.is_in(mmsi, v1_mmsi)
    # for mmsi in v1_mmsi:
    #     check.isin_in(mmsi, v2_mmsi)



