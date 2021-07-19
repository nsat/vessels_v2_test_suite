from pytest_bdd import scenario, then
from helpers import valid_timerange
from datetime import datetime, timedelta
from nested_lookup import nested_lookup as nl
import pytest



@pytest.mark.smoke_test
@pytest.mark.positive_test
@pytest.mark.short
@scenario(scenario_name='Period, no greater than 30 days, includes both start and end times',
          feature_name="vessel_by_lastUpdate_input.feature")
def test_start_and_end():
    pass


@pytest.mark.smoke_test
@pytest.mark.positive_test
@pytest.mark.short
@scenario(scenario_name='Period includes just start time',
          feature_name="vessel_by_lastUpdate_input.feature")
def test_start_only():
    pass


@pytest.mark.smoke_test
@pytest.mark.positive_test
@pytest.mark.short
@scenario(scenario_name='Period includes start time prior to today and end time beyond today',
          feature_name="vessel_by_lastUpdate_input.feature")
def test_start_end_beyond_today():
    pass



@pytest.mark.negative_test
@pytest.mark.short
@scenario(scenario_name='Period includes start time beyond today',
          feature_name="vessel_by_lastUpdate_input.feature")
def test_start_beyond_today():
    pass



@then("all objects returned will have a timestamp within the time range")
def validate_start_end_input(start_time_and_end_time_input):
    data, start_time, end_time = start_time_and_end_time_input
    assert data
    assert valid_timerange(data=data, start_time=start_time, end_time=end_time)



@then("all objects returned will have a timestamp on or after that start time")
def validate_start_only_input(start_time_input):
    data, start_time = start_time_input
    end_time = datetime.now() + timedelta(days=2) # allow for timezone slop
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    assert data
    assert valid_timerange(data=data, start_time=start_time, end_time=end_time)



@then("no data will be returned")
def no_vessel_data_returned(start_beyond_today):
    data = start_beyond_today
    if data:
        try:
            vessels: list = nl('vessel', data)
        except Exception:
            pass
        if vessels:
            assert False
        else:
            assert True


@then("all vesselPosition objects returned will have a timestamp within 30 days of the start time")
def start_time_within_today_end_time_beyond(end_beyond_today):
    data, start_time, end_time = end_beyond_today
    assert data
    assert valid_timerange(data=data, start_time=start_time, end_time=end_time)
