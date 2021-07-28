from pytest_bdd import scenario, when, then
import pytest
import pytest_check as check
from datetime import datetime
from loguru import logger
from query_sets import query_sets
from utilities import paging

qs = query_sets.GetQuery()


@pytest.mark.long
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Entire fleet request',
          feature_name="consistent_timestamps_bug419.feature")
def test_iso_timestamps():
    pass


@pytest.fixture
@when("A simple entire fleet request is made")
def get_full_fleet(full_auth_client):
    query = qs.get_vessels_gql_query()
    return full_auth_client.execute(query)


@then("the response timestamps will conform to ISO UTC")
def validate(get_full_fleet, full_auth_client):
    # %Y-%m-%dT%H:%M:%S.%fZ
    response = get_full_fleet

    pg = paging.Paging(response)
    query_text = query_sets.GetQuery().get_query_text()
    page = 0

    while True:
        try:
            response, hasNextPage = pg.page_and_get_response(full_auth_client, query_text)
        except BaseException as e:
            logger.error(e)
            raise
        if not response or not hasNextPage:
            break
        else:
            # node ingestionTimestamps
            nodes: list = response['vessels']['nodes']
            for node in nodes:
                candidate = node['ingestionTimestamp']
                check.is_true(is_timestamp(candidate))
                if not is_timestamp(candidate):
                    logger.error(node)
                # vessels
                vessel: dict = node['vessel']
                good: bool = are_timestamps(vessel)

                if not good:
                    logger.error(vessel)
                check.is_true(good)

                # positionUpdate
                pu: dict = node['positionUpdate']
                good: bool = are_timestamps(pu)
                if not good:
                    logger.error(node)
                check.is_true(good)

                # voyage
                voyage: dict = node['voyage']
                good: bool = are_timestamps(voyage)
                if not good:
                    logger.error(node)
                check.is_true(good)


def are_timestamps(candidate_dict: dict):
    ts: str = candidate_dict['timestamp']
    its: str = candidate_dict['ingestionTimestamp']
    return bool(is_timestamp(ts) and is_timestamp(its))



def is_timestamp(candidate):
    result = False
    try:
        result = bool(datetime.strptime(candidate, "%Y-%m-%dT%H:%M:%S.%fZ"))
    except ValueError:
        return result
    return result

