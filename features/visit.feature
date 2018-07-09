Feature: Visit dashboard

  Scenario: Visit dashboard without error
    When I visit the dashboard
    Then I should see a proper title page
