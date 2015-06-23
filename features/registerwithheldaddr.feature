@RegisterWitheldAddr

Feature: Register a PAB where the address for the debtor has been withheld

Scenario: Registration with address withheld
Given I have selected to register
When I complete a simple PAB
And I click Capture address
And I select that the address has been withheld
And I submit the application
Then I see a blank register screen