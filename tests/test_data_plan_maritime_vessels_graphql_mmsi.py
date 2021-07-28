from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
import pytest_check as check
from loguru import logger
from query_sets import query_sets


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Restrict by mmsi',
          feature_name="data_plan_maritime_vessels_graphql_mmsi.feature")
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
    qs = query_sets.GetQuery()
    gql_query = qs.get_vessels_gql_query()
    # a generic query should only include mmsi that are authorized
    response = client.execute(gql_query)
    mmsi_outputs = nl('mmsi', response)
    for mmsi in mmsi_outputs:
        if not str(mmsi) in mmsi_inputs:
            logger.error(f"""
            Found: {mmsi}
            Looking for: {mmsi_outputs}
            """)
            check.is_true(False)
        check.is_true(True)



