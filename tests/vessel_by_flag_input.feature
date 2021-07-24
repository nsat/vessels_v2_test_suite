# Created by brucebookman at 6/4/21
Feature: Ability to obtain static vessel data for specified by flag
  From PRD:
        -  The gQL endpoint allows filtering by Flag(s)
        - See flags: https://gist.github.com/tadast/8827699
  Test:
      In Scope:
          - FLAGS = ["UZ", "ES", "TW", "CN", "US"]
          - the flag(s) for input are specified in the code only, not as examples here

      Out of Scope:
          - null flag
          - invalid flags
          - flags not listed In Scope
          - if any optional data returned is null, it is ignored
          - compare to v1 results

  Background:
    Given an authenticated gql client with full access


  Scenario: Execute query with one or more flag values as input
    When one or more flag values are specified in the query
    Then the result matches v1


