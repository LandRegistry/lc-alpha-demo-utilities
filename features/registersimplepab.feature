@RegisterSimplePab

Feature: Register a simple PAB

Scenario: Register a simple PAB using b2b
Given I have selected to register
When I complete a simple PAB
And I click Capture address
And I complete a residence address
And I submit the application
Then I see a blank register screen