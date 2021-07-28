# Created by brucebookman at 7/12/21
Feature: endCursor timeout is 1 hour

  Background:
    Given an authenticated gql client with full access

  Scenario: Ping for cursor every 1 minute
    When a query includes request for endCursor
    When sending a request that includes the endCursor every minute
    Then the cursor will time out after 1 hour

