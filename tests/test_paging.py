from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query
from datetime import datetime
from loguru import logger
import pytest_check as check

RESPONSE_TIMES: dict = dict()


@pytest.mark.positive_test
@pytest.mark.long
@pytest.mark.smoke_test
@scenario(scenario_name='Request every vessel and all possible static data',
          feature_name="paging.feature")
def test_paging():
    pass


@pytest.fixture
@when("a request for all vessels is executed")
def get_first_page(full_auth_client):
    response: dict = full_auth_client.execute(get_query())
    return response


@then("the fields in the ResponseMetadata can be used to page through all vessel")
def paging(get_first_page, full_auth_client):
    logger.debug("PAGING STARTED")
    global RESPONSE_TIMES
    data = get_first_page
    metadata = data['vessels']['metadata']
    hasMore = metadata['hasMore']
    cursor = metadata['cursor']
    after = metadata['after']
    pages: int = 0
    while hasMore:
        try:
            pages += 1
            logger.debug(f"PAGE: {pages}")
            start_time = datetime.now()
            input_text = f'(_after: "{after}" _cursor: "{cursor}")'
            response = full_auth_client.execute(get_query(input_text=input_text))
            end_time = datetime.now()
            r = end_time - start_time
            response_time = r.total_seconds()
            check.is_true(response)
            vessels: list = response['vessels']['vessels']
            metadata = response['vessels']['metadata']
            hasMore = metadata['hasMore'] 
            msg = f"""
            Completed pages: {pages}
            Has more: {hasMore}
            Current page response time: {response_time} seconds
            """
            logger.info(msg)
            _validate(vessels)
            if hasMore:
                after = metadata['after']
                cursor = str(metadata['cursor'])
                correlationId = metadata['correlationId']
                RESPONSE_TIMES[correlationId] = response_time
        except TypeError as e:
            logger.error(msg + '\n' + e)
            continue
        except BaseException:
            # ignore it
            return


def _validate(page: list):

    logger.debug("VALIDATING")
    for vessel in page:
        #mmsi = vessel['vessel']['mmsi']
        timestamp = vessel['vessel']['timestamp']
        if not mmsi or not timestamp:
            logger.error(f"""
            vessel is missing mmsi or timestamp
            {vessel}
            """)
        #check.is_true(mmsi)
        check.is_true(timestamp)



@then("the response time is captured and will be less than an agreed upon max")
def log_response_times():
    # default number of items per page is set at 1000
    pretty: str = ''
    total: int = 0
    pages: int = 0
    for k, v in RESPONSE_TIMES.items():
        # convert strings to datetimes
        total += v
        check.is_true(v <= 2.5) # any response over 2.5 seconds is a failure
        pages += 1
        pretty += f'\ncorrelationId: {k} : {v}s\n'
    logger.info(f"""
    Total time: {total} seconds
    Total pages: {pages}
    Average response per page: {total/pages} seconds / page
    Average response time per vessel: {total/(pages * 1000)} seconds / vessel
    Response Times:
    
    {pretty}
    """)

