require_relative 'utils'
require 'json'


if ARGV.length < 2
    abort("Usage: generate.rb <what> <how many> <seed?>")
end

if ARGV.length == 3
    srand ARGV[2].to_i
end

what = ARGV[0]
how_many = ARGV[1]

def generate_name
    main_name = fake_name
    second_name = fake_name(main_name)
    third_name = fake_name(main_name)
    [main_name, second_name, third_name]
end

data = []

case what
when 'names'
    how_many.to_i.times do |n|
        data.push(generate_name)
    end
when 'namelist'
    how_many.to_i.times do |n|
        data.push(fake_name)
    end
when 'addresses'
    how_many.to_i.times do |n|
        data.push(fake_address)
    end
when 'conveyancers'
    how_many.to_i.times do |n|
        data.push(fake_conveyancer)
    end
when 'occupations'
    how_many.to_i.times do |n|
        data.push(fake_occupation)
    end
when 'businesses'
    how_many.to_i.times do |n|
        data.push(fake_company_name)
    end
when 'counties'
    how_many.to_i.times do |n|
        data.push(random_county)
    end
end


puts JSON.generate(data)
