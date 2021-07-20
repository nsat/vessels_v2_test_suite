# Created by brucebookman at 7/19/21
Feature: Restrict result sets through Apigee custom attributes
  In Scope:
    - data plan w mmsi limits


  Scenario Outline: Restrict by mmsi
    When the gql client is authenticated by an "<authorization_token>"
    When that token limits a set of "<mmsi>"
    Then query results will only contain the specified mmsi
    Examples:
    |authorization_token                |mmsi                                         |
    |LOo6r1A07Q3jbf3ZY1o9C52UVneX0bRb   |374053000 419090700 245237000 305901000      |
    |QPklqSQJZQAwkTRuB2acJ83SNwPtpChf   |210350000 477698600 257275000                |