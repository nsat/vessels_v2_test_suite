# Created by brucebookman at 7/5/21
Feature: Ability to get vessel history static fields by time range
  Test:
        In Scope:
            - timestamp returned is within spec, the test will pass

        Out of Scope:
            - if any optional data returned is null, it is ignored
            - history days limits via auth token
            - Paging, only a single page or 1000 records is verified
            - History before 2021-05-01
            - compare to v1 results

  Background:
    Given an authenticated gql client with full access


  Scenario: Period, no greater than 30 days, includes both start and end times
    When a start time and an end time are supplied as query input
    Then all objects returned will have a timestamp within the time range


  Scenario: Period includes just start time
    When a start time is supplied as a query input
    Then all objects returned will have a timestamp on or after that start time


  Scenario: Period includes start time beyond today
     When a start time beyond today is supplied as query input
     Then no data will be returned


  Scenario: Period includes start time prior to today and end time beyond today
     When an end time beyond today is supplied as query input
     Then all vesselPosition objects returned will have a timestamp within 30 days of the start time
