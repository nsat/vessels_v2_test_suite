# Created by brucebookman at 6/8/21
Feature: Ability to obtain PositionUpdate by mmsi

  Background:
    Given an authenticated gql client with full access


  Scenario Outline: Get PositionUpdate by mmsi
    When a set of "<mmsi>" are specified
    Then PositionUpdate will be returned if one exists
    Examples:
    |mmsi                                         |
    |319191700 227291690 413832466 244110188      |
    |225912960 236112560 413829503                |