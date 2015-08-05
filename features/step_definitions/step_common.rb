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

class RestAPI
    attr_reader :response, :data

    def initialize(uri)
        @uri = URI(uri)
        @http = Net::HTTP.new(@uri.host, @uri.port)
    end

    def put_data(url, data)
        request = Net::HTTP::Put.new(url)
        request.body = data
        request["Content-Type"] = "application/json"
        @response = @http.request(request)
        if @response.body == ""
            nil
        elsif @response['Content-Type'] =~ /application\/json/i
            @data = JSON.parse(@response.body)
        else
            @data = @response.body
        end
    end

    def get_data(url)
        request = Net::HTTP::Get.new(url)
        @response = @http.request(request)

        if @response['Content-Type'] =~ /application\/json/i
            @data = JSON.parse(@response.body)
        else
            @data = @response.body
        end
    end
end


Before do |scenario|
end

After do |scenario|
    if scenario.name == "Valid dates entered and migration completes successfully"
        ids = `vagrant ssh -c "psql -d landcharges -c 'select register_id from migration_status where original_regn_no in (2435,2434,3423,4343);'"`.split(/\r?\n/)
        param = '(' + ids[2..-2].join(',') + ')'

        `vagrant ssh -c "psql -d landcharges -c 'delete from migration_status where register_id in #{param}'"`
        `vagrant ssh -c "psql -d landcharges -c 'delete from register where register_id in #{param}'"`
    end
end

When(/^I submit the application$/) do
    click_button('submit')
end






