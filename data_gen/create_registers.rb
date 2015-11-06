require 'json'
require 'faker'
require_relative 'utils'

$skeleton = File.dirname(__FILE__) + "/pi_skel.json"
#data = JSON.parse(File.read(skeleton))


def create_proprietor()
    name = fake_name
    address = fake_address

    name_obj = {
        "forename" => name["forenames"].join(' '),
        "surname" => name["surname"],
        "name_category" => "PRIVATE INDIVIDUAL"
    }

    proprietor = {
        "name" => name_obj,
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

def create_charge_prop()
    name_obj = {
        "non_private_individual_name" => fake_company_name
    }
    address = fake_address

    proprietor = {
        "name" => name_obj,
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
    data = JSON.parse(File.read($skeleton))
    num_props = rand(1..2)
    props = []
    num_props.times do |n|
        props.push(create_proprietor)
    end

    data['data']['groups'][0]['entries'][0]['infills'][0]['proprietors'] = props
    data['data']['title_number'] = fake_title_number

    # small chance of a PI C reg entry too... (this is partial, just the bits we'll need)
    if rand(1..10) == 1
        prop = create_proprietor()
        entry = {
            "sub_register" => "C",
            "role_code" => "CCHR",
            "category" => "CHARGE",
            "status" => "Current",
            "infills" => [ {
                "proprietors" => [ prop ],
                "type" => "Charge Proprietor"
            } ]
        }

        data['data']['groups'].push( {
            "category" => "CHARGE",
            "entries" => [ entry ]
        })
    elsif rand(1..2) == 1
        prop = create_charge_prop()
        entry = {
            "sub_register" => "C",
            "role_code" => "CCHR",
            "status" => "Current",
            "category" => "CHARGE",
            "infills" => [ {
                "proprietors" => [ prop ],
                "type" => "Charge Proprietor"
            } ]
        }

        data['data']['groups'].push( {
            "category" => "CHARGE",
            "entries" => [ entry ]
        })
    end
    data
end


15.times do |n|
    reg = create_register()
    File.open("fake_registers/#{reg['data']['title_number']}.json", "w") do |file|
        puts "#{reg['data']['title_number']}.json created"
        file.write(JSON.pretty_generate(reg))
    end
end



