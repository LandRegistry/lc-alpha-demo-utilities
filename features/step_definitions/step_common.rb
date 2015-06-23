require 'capybara'
require 'capybara/dsl'
require 'capybara/rspec'
require 'rspec'
require 'capybara/cucumber'

Capybara.default_driver = :selenium

class AssertionFailure < RuntimeError
end

def assert( condition, message = nil )
    unless( condition )
        raise AssertionFailure, message
    end
end

Given(/^I have selected to register$/) do
  visit( 'http://localhost:5003/start_registration' )
end

When(/^I click Capture address$/) do
    click_button('submit')
end

When(/^I complete a residence address$/) do
    page.fill_in "name_or_number", :with => "34"
    page.fill_in "street", :with => "Jolly Lane"
    page.fill_in "town", :with => "Plymouth"
    page.fill_in "postcode", :with => "PL7 8YT"
end

When(/^I submit the application$/) do
    click_button('submit')
end

When(/^I select to add another address$/) do
    choose('address1')
    click_button('submit')
end

Then (/^I see a blank register screen$/) do
    page.should have_content("Register a bankruptcy")
end




