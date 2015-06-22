require 'faker'
require 'json'

$occupations = ["Accountant", "Actor", "Acupuncturist", "Administrator", "Advertising executive", "Air traffic controller", "Aircraft engineer", "Anaesthetist", "Anthropologist", "Antique dealer", "Archaeologist", "Architect", "Archivist", "Aromatherapist", "Art critic", "Art dealer", "Art historian", "Artist", "Assembly line worker", "Astrologer", "Astronomer", "Au pair", "Auctioneer", "Auditor", "Author", "Baggage handler", "Bailiff", "Baker", "Bank clerk", "Bank manager", "Bar staff", "Barber", "Barrister", "Beauty therapist", "Blacksmith", "Boat builder", "Bodyguard", "Book-keeper", "Bookmaker", "Brewer", "Bricklayer", "Broadcaster", "Builder", "Building labourer", "Bus driver", "Business consultant", "Business owner", "Butcher", "Butler", "Cabin crew", "Cabinet maker", "Camera operator", "Car dealer", "Car wash attendant", "Care assistant", "Careers advisor", "Caretaker", "Carpenter", "Carpet fitter", "Cartoonist", "Cashier", "Catering staff", "Chauffeur", "Chef", "Chemist", "Childcare worker", "Childminder", "Childrens entertainer", "Chiropodist", "Chiropractor", "Choreographer", "Circus worker", "Civil servant", "Clairvoyant", "Cleaner", "Clergyman", "Cleric", "Clerical assistant", "Clockmaker", "Coastguard", "Comedian ", "Community worker", "Company director", "Composer", "Computer analyst", "Computer engineer", "Computer programmer", "Conservationist", "Construction worker", "Cook", "Coroner", "Costume designer", "Counsellor", "Councillor", "Courier", "Craftsperson", "Crane driver", "Crematorium worker", "Croupier", "Crown prosecutor", "Curator", "Customs officer", "Dancer", "Data processor", "Debt collector", "Decorator", "Delivery driver", "Dental hygienist", "Dental nurse", "Dentist", "Designer", "Dietician", "Diplomat", "Director", "Disc jockey", "Diver", "Doctor", "Domestic staff", "Doorman", "Dressmaker", "Driving instructor", "Economist", "Editor", "Electrician", "Engineer", "Estate agent", "Events organiser", "Factory worker", "Fairground worker", "Farmer", "Farm worker", "Fashion designer", "Film director", "Financial advisor", "Firefighter", "Fitness instructor", "Flower arranger", "Flying instructor", "Footballer", "Fork-lift driver", "Fundraiser", "Funeral director", "Gamekeeper", "Garden designer", "Gardener", "Gas fitter", "Grave digger", "Hairdresser", "Handyman", "Healthcare assistant", "Health visitor", "Heating engineer", "Herbalist", "Historian", "Horticulturalist", "Housekeeper", "Hypnotherapist", "Illustrator", "Immigration officer", "Insurance consultant", "Interior designer", "Interpreter", "Inventor", "IT consultant", "Jewellery maker", "Jockey", "Journalist", "Judge", "Kennel worker", "Laboratory technician", "Labourer", "Landowner", "Landscape gardener", "Lawyer", "Leaflet distributor", "Lecturer", "Legal secretary", "Librarian", "Lifeguard", "Lift engineer", "Lighthouse keeper", "Literary agent", "Local govt worker", "Lock keeper", "Locksmith", "Lorry driver", "Machinist", "Magician", "Magistrate", "Make-up artist", "Management consultant", "Managing director", "Manicurist", "Market trader", "Marketing director", "Massage therapist", "Mathematician", "Medical student", "Merchant navy personnel", "Meteorologist", "Meter reader", "Midwife", "Miner", "Minister", "Moneylender", "Mortician", "Musician", "Nurse", "Occupational therapist", "Optician", "Osteopath", "Paramedic", "Party planner", "Pathologist", "Pest controller", "Pharmacist", "Photographer", "Physiotherapist", "Picture framer", "Pilot", "Plasterer", "Plumber", "Police officer", "Politician", "Porter", "Printer", "Prison officer", "Private investigator", "Probation officer", "Producer", "Professor", "Property developer", "Psychiatrist", "Psychologist", "Publican", "Publisher", "Racing driver", "Radio presenter", "Receptionist", "Refuse collector", "Reporter", "Researcher", "Retired", "Road sweeper", "Roofer", "Sailor", "Salesperson", "Scaffolder", "School crossing warden", "School meals supervisor", "Scientist", "Sculptor", "Secretary", "Security guard", "Ship builder", "Singer", "Shoemaker", "Shop assistant", "Social worker", "Software consultant", "Soldier", "Solicitor", "Song writer", "Special constable", "Speech therapist", "Sports coach", "Sportsperson", "Stockbroker", "Street entertainer", "Student", "Surgeon", "Surveyor", "Tailor", "Tattooist", "Tax inspector", "Taxi driver", "Teacher", "Teaching assistant", "Telephonist", "Telesales person", "Television presenter", "Toilet attendant", "Tour guide", "Traffic warden", "Train driver", "Travel agent", "Typist", "Undertaker", "Unemployed", "Veterinary surgeon", "Waiting staff", "Window cleaner" ]
def fake_occupation
	$occupations[rand($occupations.length)]
end


def fake_name(main_name = nil)
    forenames = []
    surname = ""
    
    if main_name.nil?
        forenames.push( Faker::Name.first_name )
        if rand() < 0.75
            forenames.push( Faker::Name.first_name )
        end
        if rand() < 0.05
            forenames.push( Faker::Name.first_name )
        end
        surname = Faker::Name.last_name
    else # Bug: this can generate empty forenames
        changed = false
        surname = main_name["surname"]
        # No middle name
        if main_name["forenames"].length >= 2 && rand() < 0.5
            forenames.push(main_name["forenames"][0])
            changed = true
        elsif main_name["forenames"].length >= 2 && rand() < 0.5
            # Swap first and middle
            forenames.push(main_name["forenames"][1])
            forenames.push(main_name["forenames"][0])
            changed = true
        end
        
        if rand() < 0.3
            surname = Faker::Name.last_name
            changed = true
        end
        
        if changed == false || forenames.empty?
            forenames[0] = Faker::Name.first_name
        end
    end 
    {
        "forenames" => forenames,
        "surname" => surname
    }
end

def random_letter
	(rand(122-97) + 97).chr.upcase
end

def fake_address
	lines = []
	lines.push( Faker::Address.street_address )
	lines.push( Faker::Address.city )
	if rand() < 0.5
		lines.push( Faker::Address.city )
	end
	
	postcode = "#{random_letter}#{random_letter}#{Faker::Number.number(2)} #{Faker::Number.number(1)}#{random_letter}#{random_letter}"
	{
		"address_lines" => lines,
		"postcode" => postcode
	}
end

def names_match(a,b)
	a_string = a['forenames'].join(' ') + ' ' + a['surname']
	b_string = b['forenames'].join(' ') + ' ' + b['surname']
	a_string == b_string
end

def create_data
	data = Hash.new()

	# key number
	data['key_number'] = rand(1000000..9999999).to_s
	data['application_ref' ] = rand(1000000..9999999).to_s
	data['date'] = Faker::Date.backward(365)
	data['debtor_name'] = fake_name()

	data['debtor_alternative_name'] = []
	num_an = rand(0..2)
	num_an.times do |n|
		new_name = fake_name(data['debtor_name'])
		is_ok = true
		
		# Clone prevention
		if names_match(new_name, data['debtor_name'])
			is_ok = false
		end
		
		data['debtor_alternative_name'].each do |name|
			if names_match(name, new_name)
				is_ok = false
			end
		end
		if is_ok
			data['debtor_alternative_name'].push(new_name)
		end
	end


	data['gender'] = "N/A"
	data['occupation'] = fake_occupation
	data['trading_name'] = data["debtor_name"]["forenames"][0] + " " + data["debtor_name"]["surname"]

	if rand(0..20) == 0
		data['residence_withheld' ] = true
	else
		data['residence'] = [ fake_address ]
		if rand(0..6) == 0
			data['residence'] = [ fake_address ]
		end
		data['residence_withheld' ] = false
	end
	data['business_address'] = fake_address
	dob = Faker::Date.backward(365)
	year = rand(1950..1997)

	dob = Date.new(year, dob.month, dob.day)	
	data['date_of_birth'] = dob

	if rand() < 0.25
		num_ip = rand(1..10)
		while num_ip > 0
			data['investment_property'] = [ fake_address, fake_address ]
			num_ip -= 1
		end
	else
		data['investment_property'] = []
	end

	data
end

#json = JSON.pretty_generate(create_data)
#puts json

100.times do |n|
	data = create_data
	filename = data['debtor_name']['forenames'][0] + '_' +
				data['debtor_name']['surname'] + '_' +
				data['application_ref' ] + '.json'
	puts filename
	File.open("out/#{filename}", 'w') { |file| file.write(JSON.pretty_generate(data)) }
end










