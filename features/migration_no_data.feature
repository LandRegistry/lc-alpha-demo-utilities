@MigrateNoData

Feature: Migration with valid dates but no data found

Scenario: Valid dates entered but no data exists for that date range
Given I have selected to migrate from db2
When I enter valid dates with no corresponding data in db2
And I click start migration
Then I see a no data message