# Created by brucebookman at 7/9/21
Feature: Ability to request suggested routing by specifying mmsi, origin locode and dest locode
  Test:
      In Scope:
        - verify that valid input produces output
        - invalid input yields appropriate error
        - mmsi input
        - origin locode
        - destination locode
        - piracy on + off
        - channels:
            - various choices of: Panama, Suez, Kiel
      Out of Scope:
        - imo
        - other channel combinations
        - matrix of piracy + channel combinations, which would be approx 10
        - verification that routes are logical

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Valid mmsi, locode origin, locode destination, piracy, channel combos
    When vessel "<mmsi>", "<origin_locode>", "<destination_locode>", "<piracy>", "<channels>", and "<speed>" are specified
    Then validated data is returned
    Examples:
    |mmsi           |origin_locode|destination_locode|piracy|channels                 |speed|
    |412219791      |USNYC        |SGSIN             |False |                         |     |
    |412219791      |USNYC        |SGSIN             |True  |                         |     |
    |35062619       |DEHAM        |CNZHE             |True  |SUEZ PANAMA KIEL         |     |
    |35062619       |DEHAM        |CNZHE             |True  |KIEL                     |     |
    |35062619       |DEHAM        |CNZHE             |False |KIEL                     |     |
    |412219791      |USNYC        |SGSIN             |False |                         |1    |
    |412219791      |USNYC        |SGSIN             |True  |PANAMA                   |30   |


  Scenario Outline: Invalid mmsi, locode origin, locode destination, piracy, channel combos
    When vessel "<mmsi>", "<origin_locode>", "<destination_locode>", "<piracy>", "<channels>", and "<speed>" are specified
    Then an error message is returned
    Examples:
    |mmsi           |origin_locode|destination_locode|piracy|channels         |speed|
    |412219791      |USNY         |SGSIN             |False |                 |     |
    |412219791      |USNYC        |SGSIN             |No    |                 |     |
    |35062619       |DEHAM        |CNZHE             |True  |SUEZ PAN    KIEL |     |
    |35062619       |DEHAM        |CNZH              |True  |KIEL             |     |
    |412219791      |USNYC        |SGSIN             |False |                 |x    |
