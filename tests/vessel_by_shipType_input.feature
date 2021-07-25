# Created by brucebookman at 7/24/21
Feature: Restrict results by shipType
  Reference shiptypes: https://docs.google.com/spreadsheets/d/1H5kgLS3uFaS269eerIocUsa-7S904tQM9ZnkKUjoqAQ/edit#gid=520822420

  In Scope:
    - Every shipType as singular input
    - Various shipType(s) as ORed input, see the Scenario Outline Examples
    - Only 1000 records are inspected, no paging
  Out of Scope:
    - Data verification
    - compare to v1

  Background:
    Given an authenticated gql client with full access

  Scenario Outline: Single request for each shipType
    When a "<shipType>" is specified for query input
    Then the response will contain only that shipType
    Examples:
    |shipType                   |
    |Others                     |
    |Fishing                    |
    |Tug                        |
    |Dredger                    |
    |Offshore                   |
    |Military ops               |
    |Sailing                    |
    |Yacht                      |
    |Pilot Vessel               |
    |Search and Rescue          |
    |Law Enforcement            |
    |Passenger                  |
    |Bulk Carrier               |
    |Tanker                     |
    |Dry Bulk                   |
    |Combination Carrier        |
    |Containers                 |
    |General Cargo              |
    |Tankers-Chemicals          |
    |General Tanker             |
    |LNG Carriers               |
    |Gas Carriers               |
    |Tankers - Product Tankers  |
    |Tankers - Crude            |
    |Car Carrier                |
    |Roll-on Roll-off           |
    |Vehicle/Passenger          |
    |Reefer                     |
    |Livestock                  |

    Scenario Outline: More than one shipType is specified as input
      When "<shipTypes>" are specified
      Then the response will contain only those shipType(s)
      Examples:
      |shipTypes                                          |
      |Fishing Tanker Yacht                               |
      |Containers Sailing Passenger Tug                   |