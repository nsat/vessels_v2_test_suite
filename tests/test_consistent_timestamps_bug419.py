from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query
import pytest_check as check
from nested_lookup import nested_lookup as nl
from datetime import datetime
from loguru import logger

@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Entire fleet request',
          feature_name="consistent_timestamps_bug419.feature")
def test_iso_timestamps():
    pass


@pytest.fixture
@when("A simple entire fleet request is made")
def get_1000_from_full_fleet(full_auth_client):
    return full_auth_client.execute(get_query())


@then("the response timestamps will conform to ISO UTC")
def validate_timestamp(get_1000_from_full_fleet):
    # %Y-%m-%dT%H:%M:%S.%fZ
    response = get_1000_from_full_fleet
    all_timestamps: list = nl('timestamp', response)
    all_timestamps = all_timestamps + nl('ingestionTimestamp', response)
    for timestamp in all_timestamps:
        try:
            result = bool(datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"))
        except ValueError:
            result = False
            logger.error(f"""TIMESTAMP FOUND: {timestamp} does not match %Y-%m-%dT%H:%M:%S.%fZ""")
            check.is_true(result)
        check.is_true(result)
