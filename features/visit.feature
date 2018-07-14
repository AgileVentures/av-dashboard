Feature: Visit dashboard
  Scenario: Visit dashboard and successfully authenticate as an authorized user on WSO, see dashboard, then come back after token should be expired and be redirected to reauthenticate on WSO
    When the date is 2012-10-01
    When I visit the dashboard
    Then I should be redirected to get a token from WSO
    When I return with a valid token with authorization privileges expiring on 2012-10-02
    Then I should see the dashboard
    When the date is 2012-10-03
    When I visit the dashboard
    Then I should be redirected to get a token from WSO

  Scenario: Visit dashboard and successfully authenticate as an unauthorized user on WSO, see message on dashboard about not having access
    When the date is 2012-10-01
    When I visit the dashboard
    Then I should be redirected to get a token from WSO
    When I return with a valid token without authorization privileges expiring on 2012-10-02
    Then I should see a message saying I do not have access
