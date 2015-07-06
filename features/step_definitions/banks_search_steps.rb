Given(/^I have selected to search$/) do
  visit( 'http://localhost:5003/start_search' )
end

Given(/^I have completed a registration$/) do
    step "I have selected to register"
    step "I complete a simple PAB"
    step "I click Capture address"
    step "I complete a residence address"
    step "I submit the application"
    step "I see a blank register screen"
end

When(/^I complete the forename infill with "(.*)"$/) do |forename|
    page.fill_in "forename", :with => "#{forename}"
end

When(/^I complete the surname infill with "(.*)"$/) do |surname|
    page.fill_in "surname", :with => "#{surname}"
end

When(/^I select the register database$/) do
    choose('register')
end

When(/^I select the worklist database$/) do
    choose('worklist')
end

Then (/^I see missing information messages$/) do
    page.should have_content("Missing surname")
end

Then (/^I see the results of the search$/) do
    page.should have_content("Search Results")
end

Then (/^I see the no results page$/) do
    page.should have_content("Search returned no results")
end