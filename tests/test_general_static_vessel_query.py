from pytest_bdd import scenario, when, then
import pytest
from query_sets import query_sets
from nested_lookup import nested_lookup as nl
import pytest_check as check


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Execute a vessels query',
          feature_name="general_static_vessel_query.feature")
def test_generic_vessel_query():
    pass


@pytest.fixture
@when("a vessels query is executed")
def vessel_query(full_auth_client):
    qs = query_sets.GetQuery()
    gql_query = qs.get_vessels_gql_query()
    return full_auth_client.execute(gql_query)


@then("results are returned")
def validate(vessel_query):
    data = vessel_query
    # are there nodes?
    nodes: list = data['vessels']['nodes']
    for node in nodes:
        check.is_true(node)
    # are there vessels?
    vessels: list = nl('vessel', data)
    for vessel in vessels:
        check.is_true(vessel)




