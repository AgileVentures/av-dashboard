Feature: Visit dashboard
  Scenario: Visit dashboard and successfully authenticate on WSO, see dashboard, then come back after token should be expired and be redirected to reauthenticate on WSO
    When the date is 2012-10-01
    When I visit the dashboard
    Then I should be redirected to get a token from WSO
    When I return with a valid token expiring on 2012-10-02
    Then I should see the dashboard
    When the date is 2012-10-03
    When I visit the dashboard
    Then I should be redirected to get a token from WSO
