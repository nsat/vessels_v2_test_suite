# Created by brucebookman at 7/25/21
Feature: All timestamps returned will be  ISO8601 UTC (2021-07-25T14:12:32Z .. %Y-%m-%dT%H:%M:%S.%fZ)
  See bug https://spireglobal.atlassian.net/browse/SEN-419

  In Scope
    - Every datetime returned
    - 1000 records checked
  Out of Scope
    - no paging

  Background:
    Given an authenticated gql client with full access

  Scenario: Entire fleet request
    When A simple entire fleet request is made
    Then the response timestamps will conform to ISO UTC
