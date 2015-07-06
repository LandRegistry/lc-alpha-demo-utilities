@SearchMissingInfill

Feature: Request a search without completing any infills

Scenario: Select to search without any name details
Given I have selected to search
When I submit the application
Then I see missing information messages