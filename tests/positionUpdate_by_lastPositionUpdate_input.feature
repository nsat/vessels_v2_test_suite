# Created by brucebookman at 7/5/21
Feature: Get positionUpdate by lastPositionUpdate
  Test:
        In Scope:
          - Range no greater than 30 days (data plan default)
          - Specify:
            - Start only (29 days ago)
            - Start and End (29 days ago, and today)
            - Start beyond today (negative case)
            - End only (negative case)

        Out of Scope:
            - history days limits via auth token
            - history beyond 29 days (allow for 1 timezone day slop)
            - Paging, only a single page or 1000 records is verified
            - History before 2021-05-01
            - compare to v1 results

  Background:
    Given an authenticated gql client with full access


  Scenario: Request positionUpdate by start and end dates
    When a start time and an end time are supplied as query input
    Then all objects returned will have a timestamp within the time range


  Scenario: Period includes just start time
    When a start time is supplied as a query input
    Then all objects returned will have a timestamp on or after that start time


  Scenario: Period includes start time beyond today
     When a start time beyond today is supplied as query input
     Then no data will be returned


  Scenario: Period includes start time prior to today and end time beyond today
     When a start date prior to today and end date beyond today are provided
     Then all positionUpdate objects returned will have a timestamp within 30 days of the start time

  Scenario: Period includes end only
    When only an end time is supplied
    Then the response will contain an appropriate error