# Created by brucebookman at 7/1/21
Feature: Ability to obtain static vessel data specified by WKT areaOfInterest

  Test:
    In Scope:
      - single polygon of the INDIAN OCEAN
      - vessel location is within polygon
    Out of Scope:
      - invalid or on land polygons

  Schema:
    type Query {
          vessels( areaOfInterest: wkt) {..}

  Background:
    Given an authenticated gql client with full access

  @positive_test @smoke_test @long
  Scenario: Execute query with areaOfInterest defined by WKT
    When a WKT polygon is specified for areaOfInterest
    Then each position is within the AOI