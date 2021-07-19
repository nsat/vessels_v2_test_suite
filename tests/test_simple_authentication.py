from pytest_bdd import scenario, then
import pytest
from helpers import get_query



@pytest.mark.negative_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Request with invalid authentication token',
          feature_name="simple_authentication.feature")
def test_invalid_tokens():
    pass


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Request with valid authentication token',
          feature_name="simple_authentication.feature")
def test_valid_tokens():
    pass


@pytest.mark.positive_test
@pytest.mark.short
@pytest.mark.smoke_test
@scenario(scenario_name='Request with expired token',
          feature_name="simple_authentication.feature")
def test_expired_tokens():
    pass


@then("an error is returned")
def error(get_client):
    result = None
    client = get_client
    try:
        result = client.execute(get_query())
    except BaseException as e:
        assert 'Unauthorized' in str(e)



@then("a non-error response will be returned")
def no_error(get_client):
    result = None
    client = get_client
    try:
        result = client.execute(get_query())
        assert 'vessel' in result
    except BaseException as e:
        assert 'Unauthorized' not in str(e)



@then("an appropriate error is returned")
def verify_expired_token(get_client):
    result = None
    client = get_client
    try:
        result = client.execute(get_query())
        print(result)
    except BaseException as e:
        assert 'Unauthorized' in str(e)



