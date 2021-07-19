# Created by brucebookman at 7/6/21
Feature: Query by callsign for positionUpdates

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Request positionUpdates with callsign as input
    When "<callsign>" input is provided to query
    Then the response will contain those callsigns
    Examples:
    |callsign                                                 |
    |BO12345 ZKHX TC8998 IP7924 9HB6659 ZKHX 3ADT2 MCZA3      |
    |9H7873 EA8015 9HB3177 YDB6146 YYYY OP7200 DKFQ PD5890    |