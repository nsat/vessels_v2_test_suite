from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
from loguru import logger
import pytest_check as check



@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Provide ANDed mmsi and imo where results are expected to return',
          feature_name="vessel_by_mmsi_imo.feature")
def test_vessel_by_mmsi_imo_positive():
    # write_captured_data(DATA, 'test_name_input')
    pass


@pytest.mark.negative_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Provide mmsi and imo that should produce no vessels',
          feature_name="vessel_by_mmsi_imo.feature")
def test_vessel_by_mmsi_imo_negative():
    # write_captured_data(DATA, 'test_name_input')
    pass


@pytest.fixture
@when('"<mmsi>" and "<imo>" are supplied for query input')
def get_response(full_auth_client, mmsi, imo):
    # prep inputs for query
    mmsis: list = mmsi.split()
    mmsi_string: str = ','.join(mmsis)
    imos: list = imo.split()
    imo_string: str = ','.join(imos)
    input_text = f"""(
    mmsi: [{mmsi_string}]
    imo: [{imo_string}]
    _limit: 1000)
    """
    response = full_auth_client.execute(get_query(input_text=input_text))
    return response, mmsis, imos


@then("response will contain vessels matching the mmsi + imo")
def verify_positive(get_response):
    data, mmsis, imos = get_response
    vessels: list = nl('vessel', data)

    for idx in range(len(mmsis)):
        input_mmsi = mmsis[idx]
        input_imo = imos[idx]
        found: bool = False
        for vessel in vessels:
            vessel_mmsi = str(vessel['mmsi'])
            vessel_imo = str(vessel['imo'])
            if input_mmsi == vessel_mmsi and input_imo == vessel_imo:
                found = True
                break
            else:
                continue
        if not found:
            logger.error(f"""
            input_mmsi: {input_mmsi}
            input_imo: {input_imo}
            """)
        check.is_true(found)



@then("response will contain no vessel data")
def verify_negative(get_response):
    data, mmsis, imos = get_response
    vessels: list = nl('vessel', data)
    check.is_false(vessels)