When(/^I complete a simple PAB$/) do
    page.fill_in "key_no", :with => "2244095"
    page.fill_in "app_ref", :with => "My ref"
    page.fill_in "app_date", :with => "2015-09-09"
    page.fill_in "forename", :with => "Larry"
    page.fill_in "surname", :with => "David"
    page.fill_in "dob", :with => "1970-09-09"
    page.fill_in "gender", :with => "Male"
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