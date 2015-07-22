@SearchDB2RegNoResult

Feature: Search for DB2 registration that returns no result

Scenario: Enter a DB2 Registration number that does not exist.
Given I have selected to search
When I complete the db2_reg_no infill "1234"
And I select the register database
And I submit the application
Then I see the no results page