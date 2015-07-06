@SearchName

Feature: Search with forename and surname

Scenario: Search the register database using a forename and surname
Given I have completed a registration "PA(B)" "Larry" "David"
And I have selected to search
When I complete the forename infill with "Larry"
And I complete the surname infill with "David"
And I select the register database
And I submit the application
Then I see the results of the search