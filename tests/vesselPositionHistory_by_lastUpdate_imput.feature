# Created by brucebookman at 7/5/21
Feature: Ability to get vessel position history static fields by time range
  Test:
        In Scope:
            - if ANY timestamp returned is within spec, the test will pass
            - compare to v1 results
        Out of Scope:
            - if any optional data returned is null, it is ignored
            - history days limits via auth token
            - Paging, only a single page or 1000 records is verified
            - History before 2021-05-01


