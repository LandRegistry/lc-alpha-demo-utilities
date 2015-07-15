@MigrateSuccessful

Feature: Successful Migration request

Scenario: Valid dates entered and migration completes successfully
Given I have selected to migrate from db2
When I enter valid dates with corresponding data in db2
And I click start migration
Then I see a migration completed message