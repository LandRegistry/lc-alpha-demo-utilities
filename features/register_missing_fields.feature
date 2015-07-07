@RegisterMissingFields

Feature: Register without entering any details

Scenario: Register without entering any details
Given I have selected to register
When I click Capture address
And I submit the application
Then I see a validation error