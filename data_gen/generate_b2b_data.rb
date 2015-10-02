require 'faker'
require 'json'
require_relative 'utils'




#json = JSON.pretty_generate(create_bankruptcy_record)
#puts json

unless Dir.exists?('out')
	Dir.mkdir('out')
end

#10.times do |n|
#	data = create_bankruptcy_record
#	filename = data['debtor_name']['forenames'][0] + '_' +
#				data['debtor_name']['surname'] + '_' +
#				data['application_ref' ] + '.json'
#	puts filename
#	File.open("out/#{filename}", 'w') { |file| file.write(JSON.pretty_generate(data)) }
#end

output = "[\n"
100.times do |n|
	data = create_bankruptcy_record
	output = output + JSON.generate(data) + ",\n"
end
output = output + "]"

File.open("rows.txt", 'w') { |file| file.write(output) }






