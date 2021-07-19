# Created by brucebookman at 6/18/21
Feature: Elimination of duplicate vessels
    PRD:
      "addressing the longstanding challenge of Vessel duplicate"
    Test:
      In Scope:
        - Use of imo as key for duplicate evaluation


  Background:
    Given an authenticated gql client with full access

  @positive_test @duplicates_test @long
  Scenario: imo as duplicate key in v2
    When an imo is obtained from v2 at random
    When that imo is used as input for a query returning all available related data
    Then data derived from the imo will not deviate by name, position or other measures indicating a different physical vessel


  @positive_test @duplicates_test @long
  Scenario: compare vessels from v1 to v2 with imo as identifier
    When a page is obtained from a request for all vessels from v1
    Then the v2 vessel data mirrors the v1 vessel data - using imo as the identifier



