@MigrateDateFormatError

Feature: Migration with invalid dates

Scenario: In valid dates entered
Given I have selected to migrate from db2
When I enter date in wrong format
And I click start migration
Then I see a date error message