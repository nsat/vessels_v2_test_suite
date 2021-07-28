# Created by brucebookman at 6/23/21
Feature: Paging

   Test:
      In Scope:
        _ limit is set to 1000 records per page
        - Confirm paging can occur through all data
      Out of Scope:
        - Data validation
        - performance, which is tested elsewhere

  Background:
    Given an authenticated gql client with full access

  Scenario: Request for entire fleet allows paging all results
    When a response from a query on all vessel nodes is returned
    Then paging can occur
