# Created by brucebookman at 6/3/21
Feature: Ability to obtain static vessel data for specified mmsi
  From PRD:
        - The gQL endpoint allows filtering by MMSI(s)

  Test:
      In Scope:
          - single mmsi
          - multiple mmsi

      Out of Scope:
          - invalid mmsi
          - null mmsi
          - if any optional data returned is null, it is ignored
          - data validation beyond mmsi
          - compare to v1 results

  Background:
    Given an authenticated gql client with full access


  Scenario Outline: Execute query with mmsi input
    When one or more "<mmsi>" are specified as input
    Then mmsi returned match the mmsi input

    Examples:
    |mmsi                                                                             |
    |232009459 563066990 271045559 413827924                                          |
    |412524913 261039830 316028584 235095364 413832082 207364000                      |
