# Created by brucebookman at 6/4/21
Feature: Ability to obtain static vessel data for specified vessel name
  From PRD:
    - The gQL endpoint allows filtering by Name(s)

  Test:
      In Scope:
          - the vessel names for input are specified in the code only, not as examples here
          - NAMES = ["YUZHOUFENGSHUNJI 003", "RHUMB DO", "MINQUAN", "SY GOF",  "FISH AND CHILL", "ROOKE"]
          - compare to v1 results
      Out of Scope:
          - invalid names
          - null names
          - if any optional data returned is null, it is ignored

  Background:
    Given an authenticated gql client with full access


  Scenario: Execute query with vessel name input
    When one or more vessel names are specified as input
    Then data matches v1 data
