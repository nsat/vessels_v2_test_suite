from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query
from datetime import datetime
from loguru import logger
import csv

RESPONSE_TIMES: dict = dict()


@pytest.mark.long
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Cursor time out',
          feature_name="cursor_timeout.feature")
def test_cursor_timeout():
    pass


@pytest.fixture
@when("a paging cursor is returned")
def get_cursor(full_auth_client):
    response = full_auth_client.execute(get_query())
    cursor_return_time = datetime.utcnow()
    logger.info(f"START CURSOR: {cursor_return_time}")
    return response, cursor_return_time


@then("the cursor will be available for 5 minutes")
def verify_timeout(get_cursor, full_auth_client):
    logger.debug("PAGING STARTED")
    global RESPONSE_TIMES
    data, cursor_return_time = get_cursor
    metadata: dict = data['vessels']['metadata']
    hasMore: bool = metadata['hasMore']
    after: str = metadata['after']
    cursor: str = metadata['cursor']
    pages: int = 0
    while hasMore:
        try:
            pages += 1
            # logger.debug(f"PAGE: {pages}")
            start_time = datetime.now()
            input_text = f'(_after: "{after}" _cursor: "{cursor}")'
            response = full_auth_client.execute(get_query(input_text=input_text))
            end_time = datetime.now()
            r = end_time - start_time
            response_time = r.total_seconds()
            metadata = response['vessels']['metadata']
            hasMore = metadata['hasMore']
            total: int = 0
            response_info = ''
            if RESPONSE_TIMES:
                total = 0
                for k, v in RESPONSE_TIMES.items():
                    response_info += f'correlationId: {k}, {v}\n'
                    total += v
            av: float
            try:
                av: float = total / pages
            except ZeroDivisionError as e:
                logger.error("IGNORING DIV BY ZERO")
                logger.error(e)
                logger.error(RESPONSE_TIMES)
                continue
            if hasMore:
                after = metadata['after']
                cursor = str(metadata['cursor'])
                correlationId = metadata['correlationId']
                RESPONSE_TIMES[correlationId] = response_time
                try:
                    with open('response_times.csv', 'a+') as f:
                        writer = csv.writer(f)
                        if correlationId and response_time:
                            writer.writerow([datetime.utcnow(),
                                             pages,
                                             response_time])
                except FileNotFoundError as e:
                    raise

                #logger.info(f"Page: {pages}, response time: {response_time} ")

        except BaseException as e:
            msg = f"""" 
            -------------
            CURSOR START: {cursor_return_time}
            CURSOR END: {datetime.utcnow()}
            -------------
            Average: {av} seconds / page
            
            Response Times:
            {response_info}
            
            ERROR: {e}
            """
            logger.error(msg)
            raise
