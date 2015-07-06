@SearchWorklist

Feature: Search worklist with forename and surname

Scenario: Search the worklist database using a forename and surname
Given I have completed a registration "PA(B)" "Henry" "Winkler"
And I have selected to search
When I complete the forename infill with "Henry"
And I complete the surname infill with "Winkler"
And I select the worklist database
And I submit the application
Then I see the results of the search