# Created by brucebookman at 7/9/21
Feature: Search for port information
  Free text input leads to fuzzy matched port
  In Scope:
    - valid text (meets regex requirements of at least 2 char)
    - invalid text
    - response is returned
  Out of Scope:
    - data validation

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: text supplied meets regex requirements
    When search "<text>" is provided
    Then data is returned
    Examples:
      |text                   |
      |New York               |
      |San Fancisco           |
      |PALMA DE MALLORCA      |

 Scenario Outline:  text supplied does not meet regex requirements
    When search "<text>" is provided
    Then valid error is returned
    Examples:
      |text                   |
      |N                      |
      |Hello&                 |
