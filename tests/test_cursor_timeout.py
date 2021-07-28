from pytest_bdd import scenario, when, then
import pytest
from utilities import paging, helpers
from query_sets import query_sets
from loguru import logger
from datetime import datetime, timedelta
from gql import gql

START = datetime.utcnow()
qs = query_sets.GetQuery()


@pytest.mark.long
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Ping for cursor every 1 minute',
          feature_name="cursor_timeout.feature")
def test_cursor_timeout():
    pass


@pytest.fixture
@when("a query includes request for endCursor")
def get_response_w_cursor(full_auth_client):
    gql_query = qs.get_vessels_gql_query()
    response = full_auth_client.execute(gql_query)
    return response


@pytest.fixture
@when("sending a request that includes the endCursor every minute")
def ping_cursor(get_response_w_cursor, full_auth_client):
    response = get_response_w_cursor
    pg = paging.Paging(response=response)
    endCursor, hasNextPage = pg.get_pageInfo_elements()

    insert_text = f'after: "{endCursor}" '
    txt = qs.get_vessel_query_text()
    new_query = helpers.insert_into_query_header(query=txt, insert_text=insert_text)
    while True:
        # do not allow ping forever
        if datetime.utcnow() - START > timedelta(minutes=70):
            return datetime.utcnow()

        endCursor, hasNextPage = pg.get_pageInfo_elements()
        if not endCursor or not hasNextPage:
            return datetime.utcnow()
        try:
            response = full_auth_client.execute(gql(new_query))
            pg = paging.Paging(response=response)
        except BaseException as e:
            logger.error(e)
            raise


@then("the cursor will time out after 1 hour")
def verify_timeout(ping_cursor):
    end = ping_cursor
    # add a tiny bit of slop for time zone oddities etc
    diff = end - START
    logger.debug(f"""
    Start: {START}
    End: {end}
    """)
    if diff > timedelta(minutes=63):
        assert False
    else:
        assert True
