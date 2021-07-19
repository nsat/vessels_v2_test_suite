Feature: Ability to obtain positionUpdate by vessel imo

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Get a positionUpdate by supplying ship imo
    When "<imo>" is provided as input
    Then a vessel will be returned with that imo
    Examples:
    |imo                                                                    |
    |9557575 9876543 9786437 7222695 9828637 9788306                        |
    |9564621 7222695 9788306                                                |