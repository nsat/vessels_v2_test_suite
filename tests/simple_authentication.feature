Feature: The service will provide a mechanism for authentication
  Authentication is required before data can be returned to the user
  Authentication is done through Authorization Bearer and tokens from Apigee

  Test:
      In Scope:
        - tokens that allow authentication
        - invalid tokens
        - Expired tokens:
          - BYF4RkgZhInWWSLjRYKPaQSs6ukmciCc : expired as of 2021-07-07
          - HOoiWAltGpUBXLjoR39GBTktVgKQcwHh : expired after 1 minute, will have forced the expire before this test runs

      Out of Scope:
        - any kind of data plan limitations

  Scenario Outline: Request with invalid authentication token
    When the gql client is authenticated by an "<authorization_token>"
    Then an error is returned
    Examples:
      | authorization_token              |
      | ''                               |
      | invalid                          |
      | X.NOT.a.VALID.token.gJlBEl34WF7y |


    Scenario Outline: Request with valid authentication token
      When the gql client is authenticated by an "<authorization_token>"
      Then a non-error response will be returned

      Examples:
      |authorization_token               |
      |XNuGiabch3ApMZsKgJlBEhbl3F4WF7y1  |
      |1XRDDNWvwQVMsvqpVXbA8nBjHw71wh11  |

    Scenario Outline: Request with expired token
      When the gql client is authenticated by an "<authorization_token>"
      Then an appropriate error is returned

      Examples:
      |authorization_token               |
      |BYF4RkgZhInWWSLjRYKPaQSs6ukmciCc  |
      |HOoiWAltGpUBXLjoR39GBTktVgKQcwHh  |

