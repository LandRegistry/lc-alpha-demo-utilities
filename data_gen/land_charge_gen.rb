require 'faker'
require 'json'
require_relative 'utils'

def decode_name(code_name, lcd_code_name, punc_code)
    name_string = lcd_code_name + code_name.reverse

    result = {
        'forenames' => [],
        'surname' => ''
    }

    punc_code.each do |code|
        puntuation = code >> 5
        length = code & 0x1f
        segment = name_string[0..length-1]
        name_string = name_string[length..-1]

        # This assumes there are no spaces after the * - Test this assumption
        result['forenames'].push(segment)
    end
    result['surname'] = name_string
    result
end

def stringify_name(name)
    name['forenames'].join(' ') + ' ' + name['surname']
end

def stringify_address(address)
    address['address_lines'][0..-2].join(' ') + ' ' + address['postcode'] + ' ' + address['address_lines'][-1]
end

# Generate representative data in the 'from' format, with plausible
# representations of the free text fields.
def generate_old_record
    bank = create_bankruptcy_record(false)
    data = {}
    reg_no = 2000 + rand(0..999)
    data['timestamp'] = fake_timestamp
    data['registration_no'] = reg_no
    data['notice'] = ""

    debtor_name = bank['debtor_name']
    encoded_name = encode_name(debtor_name)
    data['coded_name'] = encoded_name['coded_name']
    data['type'] = bank['application_type']
    data['county'] = 0
    data['date'] = Faker::Date.backward(365)
    data['remainder_name'] = encoded_name['remainder_name']
    data['complex_name'] = ""

    hex_code = ''
    encoded_name['hex_code'].each do |num|
        hex_code += num.to_s(16).rjust(2, '0')
    end
    data['hex_code'] = hex_code.upcase

    data['address'] = ''
    bank['residence'].each do |address|
        data['address'] += stringify_address(address).upcase + '  '
    end
    data['address'].strip!

    occupation = '(N/A)'
    bank['debtor_alternative_name'].each do |name|
        occupation += ' AKA ' + stringify_name(name).upcase
    end

    if !bank['trading_name'].nil? && bank['trading_name'] != ""
        trading_as = ""
        case rand(0..2)
            when 0
                trading_as = ' T/A ' + bank['trading_name']
            when 1
                trading_as = ' ' + bank['occupation'] + ' T/A ' + bank['trading_name']
            when 2
                trading_as = ' T/A ' + bank['trading_name'] + ' AS ' + bank['occupation']
        end

        if rand(0..5) == 0
            trading_as.sub!(' T/A ', ' T/AS ' )
        end

        occupation += trading_as
    else
        occupation += ' ' + bank['occupation']
    end

    # TODO: I see 'COB AS <blah>' in the test data. What is 'COB'?

    data['occupation'] = occupation.upcase # TODO: truncate?
    data['county_text'] = ''
    data['court_info'] = fake_court_details.upcase
    data['property'] = ''
    data['parish'] = ''
    data['notice_refs'] = ''
    data
end

def to_separated(data,sep)
    "\"#{data['timestamp']}\"#{sep}\"#{data['registration_no']}\"#{sep}\"#{data['notice']}\"#{sep}\"#{data['coded_name']}\"#{sep}" +
    "\"#{data['county']}\"#{sep}\"#{data['date']}\"#{sep}\"#{data['type']}\"#{sep}\"#{data['remainder_name']}\"#{sep}" +
    "\"#{data['hex_code']}\"#{sep}\"#{data['complex_name']}\"#{sep}\"#{data['address']}\"#{sep}\"#{data['occupation']}\"#{sep}\"#{data['county_text']}\"#{sep}" +
    "\"#{data['court_info']}\"#{sep}\"#{data['property']}\"#{sep}\"#{data['parish']}\"#{sep}\"#{data['notice_refs']}\""
end

#rec = generate_old_record
#puts
name = {
    'forenames' => ['Bob', 'Oscar', 'Francis'],
    'surname' => 'Howard'
}
enc = encode_name(name)
puts enc

#data = generate_old_record
#
#sep = ","
#puts "\"#{data['timestamp']}\"#{sep}\"#{data['registration_no']}\"#{sep}\"#{data['coded_name']}\"#{sep}" +
#    "\"#{data['county']}\"#{sep}\"#{data['date']}\"#{sep}\"#{data['class']}\"#{sep}\"#{data['remainder_name']}\"#{sep}" +
#    "\"#{data['hex_code']}\"#{sep}\"#{data['address']}\"#{sep}\"#{data['occupation']}\"#{sep}\"#{data['county_text']}\"#{sep}" +
#    "\"#{data['court_info']}\"#{sep}\"#{data['property']}\"#{sep}\"#{data['parish']}\"#{sep}\"#{data['notice_refs']}\""


#File.open("out/old_data.csv", "w" ) do |file|
#   100.times do |n|
#       file.puts to_separated(generate_old_record, ",")
#   end
#end
