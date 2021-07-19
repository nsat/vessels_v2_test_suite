from pytest_bdd import scenario, when, then
import pytest
from nested_lookup import nested_lookup as nl
from helpers import get_route_query
import pytest_check as check


@pytest.mark.short
@pytest.mark.positive_test
@pytest.mark.smoke_test
@scenario(scenario_name='Valid mmsi, locode origin, locode destination, piracy, channel combos',
          feature_name="route_by_vessel_mmsi_origin_locode_dest_locode.feature")
def test_valid_input():
    pass


@pytest.mark.short
@pytest.mark.negative_test
@scenario(scenario_name='Invalid mmsi, locode origin, locode destination, piracy, channel combos',
          feature_name="route_by_vessel_mmsi_origin_locode_dest_locode.feature")
def test_error_messages():
    pass


@pytest.fixture
@when('vessel "<mmsi>", "<origin_locode>", "<destination_locode>", "<piracy>", "<channels>", and "<speed>" are specified')
def get_response(full_auth_client, mmsi, origin_locode, destination_locode, piracy, channels, speed=''):
    if piracy == "True":
        piracy = 'true'
    else:
        piracy = 'false'
    channel_string: str = ''
    if channels:
        channel_string = f"channels: [{channels}]"

    speed_string: str = ''
    if speed:
        speed_string = f"speed: {float(speed)}"

    input_text = f"""
    (
        routeInput: {{
            vessel: {{
                mmsi: {mmsi}
            }}
            origin: {{
                unlocode: {origin_locode}
            }}
            destination:
                [{{unlocode: "{destination_locode}"}}]
        
            piracy: {piracy}
            {speed_string}
            {channel_string}
        }}
        )
    """
    response = full_auth_client.execute(get_route_query(input_text=input_text))
    return response


@then("validated data is returned")
def step_impl():
    raise NotImplementedError(u'STEP: Then validated data is returned')


@then("an error message is returned")
def step_impl():
    raise NotImplementedError(u'STEP: Then an error message is returned')
