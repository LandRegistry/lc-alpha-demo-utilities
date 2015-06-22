@RegisterInvestmentAddr

Feature: Register a PAB where the debtor has 2 investment addresses

Scenario: Registration with investment address
Given I have selected to register
When I complete a simple PAB
And I click Capture address
And I complete a residence address
And I select to add another address
And I choose to add investment address
And I complete an investment address
And I select to add another address
And I choose to add investment address
And I complete an investment address
And I submit the application
Then I see a blank register screen