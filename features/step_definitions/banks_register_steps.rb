Given(/^I have selected to register$/) do
  visit( 'http://localhost:5003/start_registration' )
end

When(/^I complete a simple PAB "(.*)" "(.*)" "(.*)"$/) do |type, forename, surname|
    page.fill_in "key_no", :with => "2244095"
    page.fill_in "app_ref", :with => "My ref"
    page.fill_in "app_type", :with => "#{type}"
    page.fill_in "app_date", :with => "2015-09-09"
    page.fill_in "forename", :with => "#{forename}"
    page.fill_in "surname", :with => "#{surname}"
    page.fill_in "dob", :with => "1970-09-09"
    page.fill_in "gender", :with => "Male"
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

When(/^I select to add another address$/) do
    choose('address1')
    click_button('submit')
end

When(/^I complete a business address$/) do
    page.fill_in "name_or_number", :with => "Seaton Court"
    page.fill_in "street", :with => "William Prance Road"
    page.fill_in "town", :with => "Plymouth"
    page.fill_in "postcode", :with => "PL5 8AA"
end

When(/^I choose to add investment address$/) do
    choose('address_type3')
end

When(/^I complete an investment address$/) do
    page.fill_in "name_or_number", :with => "1A"
    page.fill_in "street", :with => "By the Beach"
    page.fill_in "town", :with => "Corfu"
    page.fill_in "postcode", :with => "PL11 2AA"
end

When(/^I select that the address has been withheld$/) do
    choose('withheld2')
end

Then (/^I see a blank register screen$/) do
    page.should have_content("Register a bankruptcy")
    page.should have_no_content("Unable to submit application")
end

Then (/^I see a validation error$/) do
    page.should have_content("Unable to submit application")
end

Then (/^I see invalid application type screen$/) do
    page.should have_content("not one of ['PA(B)', 'WO(B)']")
end
