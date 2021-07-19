# Created by brucebookman at 7/7/21
Feature: Ability to specify input of mmsi and imo
  Reference: https://github.com/nsat/maritime/blob/master/vessels-graphql-server/graphql/schema.graphql

  Query for vessels by vessel properties, receiving vessel, current voyage,
  and current position information. For a given query argument arrays, the values
  in the provided array are ORed. Across query arguments, values are
  logically ANDed. For example, if you provide multiple IMO values, all results
  will have to match one of those values. If you provide multiple IMO and multiple
  MMSI values, all results will have to match one of the provided IMO values and
  one of the provided MMSI values.

  In Scope:
    - mmsi + imo : expected to return data
    - mmsi + imo: expect no data to be returned

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Provide ANDed mmsi and imo where results are expected to return
    When "<mmsi>" and "<imo>" are supplied for query input
    Then response will contain vessels matching the mmsi + imo
    Examples:
    |mmsi                               |imo                                    |
    |273419360 413527340 636018131      |9053206 9690121 9336282                |
    |373071000 413690460 257086000      |9494747 8656714 9609990                |



  Scenario Outline: Provide mmsi and imo that should produce no vessels
    When "<mmsi>" and "<imo>" are supplied for query input
    Then response will contain no vessel data
    Examples:
    |mmsi                               |imo                                    |
    |273419360 413527340 636018131      |9494747 8656714 9609990                |
    |373071000 413690460 257086000      |9053206 9690121 9336282                |