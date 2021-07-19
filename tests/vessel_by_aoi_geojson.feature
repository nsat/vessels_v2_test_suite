# Created by brucebookman at 6/4/21
Feature: Ability to obtain static vessel data specified by GeoJson areaOfInterest
  From PRD:
    - The gQL endpoint allows filtering by geopolygon the last reported position

  Test:
    In Scope:
      - single polygon of the INDIAN OCEAN
      - compare to v1
      - vessel location is within polygon
    Out of Scope:
      - invalid or on land polygons

  Schema:
    type Query {
          vessels( areaOfInterest: GeoJson) {..}

  Background:
    Given an authenticated gql client with full access


  Scenario: Execute query with areaOfInterest defined by GeoJson
    When a GoeJson polygon is specified for areaOfInterest
    Then each vessel position is within the aoi




