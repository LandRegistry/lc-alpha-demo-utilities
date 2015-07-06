@SearchNoResult

Feature: Search that returns no result

Scenario: Enter a forename and surname that has not been registered.
Given I have selected to search
When I complete the forename infill with "bor"
And I complete the surname infill with "nosenhpets"
And I select the register database
And I submit the application
Then I see the no results page