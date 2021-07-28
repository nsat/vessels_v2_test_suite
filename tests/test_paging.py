from pytest_bdd import scenario, when, then
import pytest
from utilities import paging
from query_sets import query_sets
from loguru import logger



@pytest.mark.long
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Request for entire fleet allows paging all results',
          feature_name="paging.feature")
def test_paging():
    pass


@pytest.fixture
@when("a response from a query on all vessel nodes is returned")
def get_response(full_auth_client):
    qs = query_sets.GetQuery()
    gql_query = qs.get_vessels_gql_query()
    response = full_auth_client.execute(gql_query)
    return response


@then("paging can occur")
def verify_paging(get_response, full_auth_client):
    pg = paging.Paging(get_response)
    query_text = query_sets.GetQuery().get_vessel_query_text()
    page = 0

    while True:
        try:
            response, hasNextPage = pg.page_and_get_response(full_auth_client, query_text)
        except BaseException as e:
            logger.error(e)
            raise
        if not response or not hasNextPage:
            assert False
        else:
            page += 1
            logger.info(f"Page: {page}")



