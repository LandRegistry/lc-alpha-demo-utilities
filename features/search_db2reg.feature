@SearchDB2RegPositiveResult

Feature: Search for DB2 registration that returns result

Scenario: Enter a DB2 Registration number that does exist.
Given I have selected to search
When I complete the db2_reg_no infill "2067"
And I select the register database
And I submit the application
Then I see the results of the search
