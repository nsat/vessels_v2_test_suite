# Created by brucebookman at 7/12/21
Feature: A response provides a cursor to allow for paging
  The cursor is a string unique identifier for the result set
  The cursor times out after 5 minutes

  Background:
    Given an authenticated gql client with full access

  Scenario: Cursor time out
    When a paging cursor is returned
    Then the cursor will be available for 5 minutes

