# Created by brucebookman at 6/3/21
Feature: Ability to obtain static vessel data

  Test:
      In Scope:
          - Simple vessel query with no input parameters
          - Validate a response is returned
          _ Guaranteed return fields (mmsi, timestamp) are of expected type or length
      Out of Scope:
          - Data verification

  Background:
    Given an authenticated gql client with full access

  @positive_test @smoke_test
  Scenario: Execute a vessels query
    When a vessels query is executed
    Then results are returned