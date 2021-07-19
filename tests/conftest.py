from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from pytest_bdd import given, when
import pytest
from loguru import logger
from helpers import get_query, get_settings
from datetime import datetime, timedelta
import requests.exceptions

logger.add('vessels2.log', rotation="500 MB", retention="10 days", level='DEBUG')


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Supports pytest_bdd reporting of test failures.  Do not change
    """
    try:
        step_func_args = step_func_args[:300]
    except TypeError:
        step_func_args = ''


    details = f"""
    Feature: {feature}
        Scenario: {scenario}    
        Failed Step: {step}
        Failed Step Function:
                                    {step_func}
                                    
        Failed Step Function Args:
                                    {step_func_args}
                                    
        Request: {request}
        Exception: {exception}
    """
    logger.error(details)



@pytest.fixture
@given("A GraphQL endpoint", target_fixture='get_endpoint')
def get_endpoint():
    """Returns the endpoint in the dictionary from get_settings"""
    return get_settings()['endpoint_under_test']


@pytest.fixture
@given('an authenticated gql client with full access')
def full_auth_client(get_full_access_token):
    """
    :param get_full_access_token: pytest fixture returns a token allowing full api
    :rtype gql client: with full access
    """
    authorization_token = get_full_access_token
    headers = dict()
    headers['Authorization'] = f'Bearer {authorization_token}'
    transport = RequestsHTTPTransport(
        url=get_settings()['endpoint_under_test'],
        headers=headers,
        verify=True,
        retries=3,
        timeout=10)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


@pytest.fixture
def get_full_access_token():
    return get_settings()['full_access_token']


@pytest.fixture
@when('the gql client is authenticated by an "<authorization_token>"')
def get_client(get_endpoint, authorization_token):
    """Creates a gql transport client
    :param authorization_token: apigee token
    :type authorization_token: str
    :param get_endpoint: graphql endpoint
    :type get_endpoint: str
    :return: gql transport client
    :rtype: gql.Client
    """

    headers = dict()
    headers['Authorization'] = f'Bearer {authorization_token}'
    transport = RequestsHTTPTransport(
        url=get_endpoint,
        headers=headers,
        verify=True,
        retries=3,
        timeout=10)
    try:
        client = Client(transport=transport, fetch_schema_from_transport=True)
    except requests.exceptions.HTTPError as e:
        client = e
    return client


@pytest.fixture
@when("a start time and an end time are supplied as query input")
def start_time_and_end_time_input(full_auth_client):
    start_time: str = "2021-06-01T17:37:28.411Z"
    end_time: str = "2021-07-01T17:37:28.411Z"
    input_text = f"""(
        lastUpdate:{{
            startTime: "{start_time}"
            endTime: "{end_time}"
        }}
    )"""
    
    response = full_auth_client.execute(get_query(input_text))
    return response, start_time, end_time


@pytest.fixture
@when("a start time is supplied as a query input")
def start_time_input(full_auth_client):
    start_time: str = "2021-05-20T07:07:08.111Z"
    input_text = f"""(
            lastUpdate:{{
                startTime: "{start_time}"
            }}
        )"""
    response = full_auth_client.execute(get_query(input_text))
    return response, start_time


@pytest.fixture
@when("a start time beyond today is supplied as query input")
def start_beyond_today(full_auth_client):
    today = datetime.now()
    start_time = today + timedelta(weeks=1)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    input_text = f"""(
               lastUpdate:{{
                   startTime: "{start_time}"
               }}
           )"""
    response = full_auth_client.execute(get_query(input_text))

    return response


@pytest.fixture
@when("an end time beyond today is supplied as query input")
def end_beyond_today(full_auth_client):
    today = datetime.now()
    start_time = today + timedelta(weeks=-1)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_time = today + timedelta(weeks=1)
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    info = f"""
               startTime: "{start_time}"
               endTime: "{end_time}"
           """
    logger.debug(info)
    response = full_auth_client.execute(get_query(variable='lastUpdate', input=info))

    return response, start_time, end_time
