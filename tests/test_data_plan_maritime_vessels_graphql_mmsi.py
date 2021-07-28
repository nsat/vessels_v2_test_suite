from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check
from loguru import logger


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Restrict by mmsi',
          feature_name="data_plan_maritime_vessels_graphql.feature")
def test_data_plan_mmsi():
    pass


@pytest.fixture
@when('that token limits a set of "<mmsi>"')
def get_vars(mmsi):
    return mmsi.split()



@then("query results will only contain the specified mmsi")
def verify_filtering(get_client, get_vars):
    client = get_client
    mmsi_inputs: list = get_vars

    # a generic query should only include mmsi that are authorized
    response = client.execute(get_query())
    mmsi_outputs = nl('mmsi', response)

    # Did get the specific mmsi
    for output in mmsi_outputs:
        found = False
        for i in mmsi_inputs:
            if str(output) == i:
                found = True
        check.is_true(found)

