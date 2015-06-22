# Example Data Generation Utility
Ruby script to generate (semi-)plausible JSON fragments simulating
likely submission data for the B2B service.

##Setting Up
Requires the Faker gem:
```gem install faker --no-rdoc --no-ri```

##Usage
```ruby generate_data.rb```

It'll output 100 json files to the 'out' directory. To change this
amount, change the code!

##Examples
The 'out' directory contains some examples. Notably:

Lance_Blanda_9568000.json has a withheld residence.
Shannon_Oberbub_9162511.json is very "all options" - multiples of each
property that allows multiple objects.
