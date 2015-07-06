@RegisterBusinessAddr

Feature: Register a PAB where the debtor has a business address

Scenario: Registration with business address
Given I have selected to register
When I complete a simple PAB "PA(B)" "John" "Kennedy"
And I click Capture address
And I complete a residence address
And I select to add another address
And I complete a business address
And I submit the application
Then I see a blank register screen