# Created by brucebookman at 6/23/21
Feature: Paging
  * when more than 99 records will be returned, use metadata to page

   Test:
      In Scope:
        - Confirm paging can occur through all data
        - Any response time > 2.5 seconds is a failure
      Out of Scope:
        - Data validation

  Background:
    Given an authenticated gql client with full access

  Scenario: Request every vessel and all possible static data
    When a request for all vessels is executed
    Then the fields in the ResponseMetadata can be used to page through all vessel
    Then the response time is captured and will be less than an agreed upon max