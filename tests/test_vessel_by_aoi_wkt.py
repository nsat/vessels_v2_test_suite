from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query, WKT, INDIAN_OCEAN
from shapely.geometry import shape, Point
import pytest_check as check





@scenario(scenario_name='Execute query with areaOfInterest defined by WKT',
          feature_name="vessel_by_aoi_wkt.feature")
def test_aoi_wkt():
    pass


@pytest.fixture
@when("a WKT polygon is specified for areaOfInterest")
def get_response(full_auth_client):
    wkt = f"""(
            areaOfInterest: {{
                wkt: {WKT}
            }}
            _limit: 1000
    )"""
    response: dict = full_auth_client.execute(get_query(input_text=wkt))
    return response


@then("each position is within the AOI")
def verify_within_aoi(get_response):
    # set up AOI
    aoi = shape(INDIAN_OCEAN)
    # get v2
    v2: dict = get_response
    assert v2
    # get list of latitudes returned
    vessel_voyage_position_bundles: list = v2['vessels']['vessels']
    for bundle in vessel_voyage_position_bundles:
        y = bundle['positionUpdate']['latitude']
        x = bundle['positionUpdate']['longitude']
        point = Point(x,y)
        check.is_true(point.within(aoi))

