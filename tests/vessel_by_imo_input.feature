# Created by brucebookman at 6/3/21
Feature: Ability to obtain static vessel data specified by imo
  From PRD:
        - The gQL endpoint allows filtering by IMO(s)

   Test:
      In Scope:
          - multiple imo
          - compare to v1 results

      Out of Scope:
          - invalid imo
          - null imo
          - if any optional data returned is null, it is ignored
          - data validation beyond imo, mmsi


  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Execute query with imo input
    When one or more "<imo>" are specified as given input
    Then data matches vessel v1 data
    Examples:
    |imo                                                      |
    |4194304 8138841 9564621                                  |
    |9876543 7222695 9828637 9788306                          |

