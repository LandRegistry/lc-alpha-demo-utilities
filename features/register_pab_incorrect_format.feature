@RegisterPabInWrongFormat

Feature: Register a PAB in the incorrect format

Scenario: Register a PAB in the incorrect format
Given I have selected to register
When I complete a simple PAB "PAB" "Larry" "David"
And I click Capture address
And I complete a residence address
And I submit the application
Then I see invalid application type screen