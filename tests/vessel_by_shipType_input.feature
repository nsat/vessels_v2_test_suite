# Created by brucebookman at 6/4/21
Feature: Ability to obtain static vessel data for specified shipType(s)
  From PRD:
    - The gQL endpoint allows filtering by Vessel Type(s)

  Info:
  https://www.navcen.uscg.gov/?pageName=AISMessagesB
    0 = not available or no ship = default
    1-99 = as defined
    100-199 = reserved, for regional use
    200-255 = reserved, for future use

  Test:
      In Scope:
        - All ship types are input (code only)

      Out of Scope:
        - if any optional data returned is null, it is ignored
        - compare to v1 results MMSIs

  Background:
    Given an authenticated gql client with full access

  @positive_test @long @smoke_test
  Scenario: Execute a query for one or more shipType(s)
    When one or more shipType(s) are specified for input
    Then the results will include the shipType specified and no other