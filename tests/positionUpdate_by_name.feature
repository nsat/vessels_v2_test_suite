Feature: Ability to obtain positionUpdate by vessel name

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Get a positionUpdate by supplying ship name
    When "<vessel_name>" is provided as query input
    Then a vessel will be returned with that name

    Examples:
    |vessel_name                                                             |
    |HARMATTAN TSITIKA DARYA YUXINHUO16589                                   |
    |ARIOSA TETRAKTYS JIAOTONG1 TIZIANA CHUANJI37 VTT39 SULIANYUNGANGHUO7666 |