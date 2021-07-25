from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_query
import pytest_check as check
from datetime import datetime, timedelta
from loguru import logger


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Request positionUpdate by start and end dates',
          feature_name="positionUpdate_by_lastPositionUpdate_input.feature")
def test_start_and_end_time_within_30():
    pass


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Period includes just start time',
          feature_name="positionUpdate_by_lastPositionUpdate_input.feature")
def test_start_29_days_ago():
    pass



@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Period includes start time beyond today',
          feature_name="positionUpdate_by_lastPositionUpdate_input.feature")
def test_start_beyond_today():
    pass


@pytest.mark.short
@pytest.mark.negative_test
@scenario(scenario_name='Period includes end only',
          feature_name="positionUpdate_by_lastPositionUpdate_input.feature")
def test_end_only():
    pass


# Period includes start time prior to today and end time beyond today
def test_end_beyond_today():
    pass

@pytest.fixture
@when("a start time and an end time are supplied as query input")
def start_time_and_end_time_input(full_auth_client):
    today = end_time = datetime.utcnow()
    start_time = today - timedelta(days=28)
    start_time_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time_formatted: str = today.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    input_text = f"""(
        lastPositionUpdate:{{
            startTime: "{start_time_formatted}"
            endTime: "{end_time_formatted}"
        }}
    )"""

    response = full_auth_client.execute(get_query(input_text))
    return response, start_time, end_time


@pytest.fixture
@when("a start time is supplied as a query input")
def start_time_input(full_auth_client):
    today = datetime.utcnow()
    start_time = today - timedelta(days=20)  # just to mix things up a bit
    start_time_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    input_text = f"""(
            lastPositionUpdate:{{
                startTime: "{start_time_formatted}"
            }}
        )"""
    response = full_auth_client.execute(get_query(input_text))
    return response, start_time


@pytest.fixture
@when("a start time beyond today is supplied as query input")
def start_beyond_today(full_auth_client):
    today = datetime.utcnow()
    start_time = today + timedelta(weeks=1)
    start_time_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    input_text = f"""(
               lastPositionUpdate:{{
                   startTime: "{start_time_formatted}"
               }}
           )"""
    response = full_auth_client.execute(get_query(input_text))

    return response, start_time


@pytest.fixture
@when("an end time beyond today is supplied as query input")
def end_beyond_today(full_auth_client):
    today = datetime.utcnow()
    start_time = today + timedelta(weeks=-1)
    start_time_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = today + timedelta(weeks=1)
    end_time_formatted = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    info = f"""(
                   lastPositionUpdate:{{
                       startTime: "{start_time_formatted}"
                       endTime: "{end_time_formatted}"
                   }}
               )"""

    response = full_auth_client.execute(get_query(input_text=info))

    return response, start_time, end_time


@when('a start date prior to today and end date beyond today are provided')
def start_prior_to_today_end_after_today(full_auth_client):
    today = datetime.utcnow()
    start_time = today - timedelta(weeks=1)
    start_time_formatted = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = today + timedelta(weeks=2)
    end_time_formatted = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    info = f"""(
                      lastPositionUpdate:{{
                          startTime: "{start_time_formatted}"
                          endTime: "{end_time_formatted}"
                      }}
                  )"""

    response = full_auth_client.execute(get_query(input_text=info))
    return response, start_time, end_time


@then("all objects returned will have a timestamp within the time range")
def validate_date_within_range(start_time_and_end_time_input):
    response, start_time, end_time = start_time_and_end_time_input
    positionUpdates = nl('positionUpdate', response)
    for positionUpdate in positionUpdates:
        timestamp = positionUpdate['timestamp']
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        check.is_true(is_within(start=start_time, end=end_time, timestamp=timestamp))
        if not is_within(start=start_time, end=end_time, timestamp=timestamp):
            logger.error(f"""
            START: {start_time}
            END: {end_time}
            STAMP: {timestamp}
            """)



@then("all objects returned will have a timestamp on or after that start time")
def validate_after_start(start_time_input):
    response, start = start_time_input
    end = start + timedelta(days=29)
    positionUpdates = nl('positionUpdate', response)
    for positionUpdate in positionUpdates:
        timestamp = positionUpdate['timestamp']
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        check.is_true(is_within(timestamp=timestamp, start=start, end=end))
        if not is_within(start=start, end=end, timestamp=timestamp):
            logger.error(f"""
            START: {start}
            END: {end}
            STAMP: {timestamp}
            """)


@then("no data will be returned")
def validate_null_response(start_beyond_today):
    response, start = start_beyond_today
    vessel = nl('vessel', response)
    assert not vessel


@then("all positionUpdate objects returned will have a timestamp within 30 days of the start time")
def validate_within_30_of_start(start_prior_to_today_end_after_today):
    # Period includes start time prior to today and end time beyond today
    response, start, end = start_prior_to_today_end_after_today
    positionUpdates = nl('positionUpdate', response)
    for positionUpdate in positionUpdates:
        timestamp = positionUpdate['timestamp']
        timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
        check.is_true(is_within(timestamp=timestamp, start=start, end=end))


@pytest.fixture
@when("only an end time is supplied")
def end_only(full_auth_client):
    today = datetime.utcnow()
    end_time = today + timedelta(weeks=2)
    end_time_formatted = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    input_text = f"""(
            lastPositionUpdate:{{
                endTime: "{end_time_formatted}"
            }}
        )"""
    response: dict = dict()
    try:
        response = full_auth_client.execute(get_query(input_text))
    except BaseException as e:
        return str(e)


@then("the response will contain an appropriate error")
def validate_error(end_only):
    assert 'invalid value' in end_only


def is_within(timestamp, start=None, end=None):
    # give 10 seconds slop
    timestamp = timestamp + timedelta(seconds=10)
    if start and end:
        return end >= timestamp >= start
    if start and not end:
        end = start + timedelta(days=29)
        return end >= timestamp >= start
