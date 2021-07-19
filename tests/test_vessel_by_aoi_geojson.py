from pytest_bdd import scenario, when, then
import pytest
from helpers import get_query, INDIAN_OCEAN, AOI
from shapely.geometry import shape, Point

import pytest_check as check
from loguru import logger




@pytest.mark.smoke_test
@pytest.mark.positive_test
@scenario(scenario_name='Execute query with areaOfInterest defined by GeoJson',
          feature_name="vessel_by_aoi_geojson.feature")
def test_aoi_geojson():
    pass


@pytest.fixture
@when("a GoeJson polygon is specified for areaOfInterest")
def aoi_input(full_auth_client):
    input_text = f"""(
        areaOfInterest:
            {AOI}
        _limit: 1000
    
    )"""
    response: dict = full_auth_client.execute(get_query(input_text=input_text))
    return response


@then("each vessel position is within the aoi")
def verify_within_aoi(aoi_input):
    # set up AOI
    aoi = shape(INDIAN_OCEAN)
    # get v2
    v2: dict = aoi_input
    # get list of latitudes returned
    vessel_voyage_position_bundles: list = v2['vessels']['vessels']
    for bundle in vessel_voyage_position_bundles:
        y = bundle['positionUpdate']['latitude']
        x = bundle['positionUpdate']['longitude']
        point = Point(x, y)
        check.is_true(point.within(aoi))
        if not point.within(aoi):
            vessel: str = ''
            for k, v in bundle.items():
                if v:
                    vessel += f'{k}:{v}\n'
            logger.error(f"""{vessel}""")