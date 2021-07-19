from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import PositionCollectionType, get_query


@pytest.mark.postive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Get PositionUpdate by mmsi',
          feature_name="positionUpdate_by_mmsi.feature")
def test_position_update_by_mmsi_input():
    pass


@pytest.fixture
@when('a set of "<mmsi>" are specified')
def get_position_by_mmis(full_auth_client, mmsi):
    mmsis: list = mmsi.split()
    mmsis_ints: list = [int(m) for m in mmsis]
    input_text = f"""(mmsi: {mmsis_ints})"""
    response: dict = full_auth_client.execute(get_query(input_text))
    return response,  mmsis_ints


@then("PositionUpdate will be returned if one exists")
def validate_result(get_position_by_mmis):
    v2, mmsis_ints = get_position_by_mmis
    assert v2
    returned_mmsi: list = nl('mmsi', v2)

    # every mmsi returned is in the mmsi list
    for m in returned_mmsi:
        assert m in mmsis_ints

    collection_types = nl('collectionType', v2)
    for c in collection_types:
        assert c in PositionCollectionType




