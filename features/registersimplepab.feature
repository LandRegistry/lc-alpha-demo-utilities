@RegisterSimplePab

Feature: Register a simple PAB

Scenario: Register a simple PAB using b2b
Given I have selected to register
When I complete a simple PAB
And I click Capture
And I complete a residence address
Then I see the complete page
And I click Next for new registration