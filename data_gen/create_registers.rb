require 'json'
require 'faker'
require_relative 'utils'

skeleton = File.dirname(__FILE__) + "/pi_skel.json"
data = JSON.parse(File.read(skeleton))


def create_proprietor()
    name = fake_name
    address = fake_address

    proprietor = {
        "name" => {
            "forename" => name["forenames"].join(' '),
            "surname" => name["surname"],
            "name_category" => "PRIVATE INDIVIDUAL"
        },
        "addresses" => [ {
            "town" => address["address_lines"][1],
            "house_no" => rand(1..99).to_s,
            "street_name" => Faker::Address.street_address.sub(/\d+ /, ''),
            "address_type" => "UK",
            "local_name" => "",
            "address_string" => "",
            "postal_county" => address["county"],
            "postcode" => address["postcode"]
        } ]
    }
end

def create_register()
    data = JSON.parse(File.read(skeleton))
    num_props = rand(1..2)
    props = []
    num_props.times do |n|
        props.push(create_proprietor)
    end

    data['data']['groups'][0]['entries'][0]['infills'][0]['proprietors'] = props
    data['data']['title_number'] = fake_title_number

    # small chance of a PI C reg entry too...
    if rand(1..1) == 1
        prop = create_proprietor()



    end
end



