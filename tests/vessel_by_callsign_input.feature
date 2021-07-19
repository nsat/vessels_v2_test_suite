# Created by brucebookman at 6/3/21
Feature: Ability to obtain static vessel data for specified callsign
  Schema:
    type Query {
            vessels(
              callsign: [String!] . . .
  Test:
      In Scope:
          - Multiple callsigns
          - the callsigns for input are specified in the code only, not as examples here
          - SIGNS = ["9HB6653", "FAA8092", "DH3591", "DF8337", "IWJJ", "9V6056"]

      Out of Scope:
          - null callsign
          - single callsign.  If multiple work, single will work
          - invalid callsign.  Will either return an error or empty data)
          - if any optional data returned is null, it is ignored
          - compare to v1 results

  Background:
    Given an authenticated gql client with full access


  Scenario: Execute query with callsign input
    When one or more callsigns are specified
    Then data matches vessels v1 api data
