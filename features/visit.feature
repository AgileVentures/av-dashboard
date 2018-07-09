Feature: Visit dashboard

  Scenario: Visit dashboard without error
    When I visit the dashboard
    Then I should be redirected to get a token from WSO
    When I return with a valid token
    Then I should see the dashboard
