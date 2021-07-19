# Created by brucebookman at 7/9/21
Feature: Ability to request port data by unlocode
  In Scope:
    - valid ports
    - check that data is returned
    - error for invalid port
  Out of Scope:
    - data verification for accuracy

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Valid port
    When a "<UNLOCODE>" is provided for input
    Then valid data is returned
    Examples:
    |UNLOCODE |
    |CNTZO    |
    |KRINC    |
    |TWKHH    |

  Scenario Outline: Invalid port
    When a "<UNLOCODE>" is provided for input
    Then an error response will be returned
    Examples:
    |UNLOCODE |
    |CNTO     |
    |RXNCZ    |
