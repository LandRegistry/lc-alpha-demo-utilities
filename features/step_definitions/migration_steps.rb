

Given(/^I have selected to migrate from db2$/) do
  visit( 'http://localhost:5003/migration_dashboard' )
end

When(/^I enter valid dates with corresponding data in db2$/) do
    page.fill_in "start_date", :with => "2014-01-01"
    page.fill_in "end_date", :with => "2014-01-31"
end

When(/^I enter valid dates with no corresponding data in db2$/) do
    page.fill_in "start_date", :with => "2017-01-01"
    page.fill_in "end_date", :with => "2017-01-31"
end

When(/^I enter date in wrong format$/) do
    page.fill_in "start_date", :with => "2017/01/01"
    page.fill_in "end_date", :with => "2017/01/31"
end

When(/^I click start migration$/) do
    click_button('start')
end


Then (/^I see a date error message$/) do
    page.should have_content("Incorrect date format")
end

Then (/^I see a no data message$/) do
    page.should have_content("No data found for date range")
end

Then (/^I see a migration completed message$/) do
    page.should have_content("Migration successfully completed for date range")
end
