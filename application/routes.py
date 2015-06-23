from flask import request, Response, render_template
import logging
from application import app
import jsonpickle
import json
import requests


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/start_registration', methods=['GET'])
def start_registration():
    logging.info("registration")

    return render_template('regn_debtor.html')


@app.route('/debtor', methods=['POST'])
def debtor_details():
    logging.info("address capture")
    key_no = request.form['key_no']
    reference = request.form['reference']
    application_date = request.form['application_date']
    forename = request.form['forename']
    surname = request.form['surname']
    alt_forename = request.form['alt_forename']
    alt_surname = request.form['alt_surname']
    dob = request.form['dob']
    gender = request.form['gender']
    occupation = request.form['occupation']
    trading = request.form['trading']

    registration = BankruptcyRegnDetails(key_no, reference, application_date, forename, surname, alt_forename,
                                         alt_surname, dob, gender, occupation, trading)

    json_reg_str = jsonpickle.encode(registration)

    return render_template('regn_residence.html', regnDetails=registration, regDataAsJSON=json_reg_str)


@app.route('/residence', methods=['POST'])
def residence_address():
    logging.info("residence addresses")
    registration = jsonpickle.decode(request.form['regDataAsJSON'])
    registration.withheld = request.form['withheld']

    if registration.withheld == "false":
        address_type = "residence"
        name_or_number = request.form['name_or_number']
        street = request.form['street']
        town = request.form['town']
        postcode = request.form['postcode']
        address = Address(address_type, name_or_number, street, town, postcode)
        registration.addressList.append(address)

    add_address = request.form['add_address']

    if add_address == "yes":
        json_reg_str = jsonpickle.encode(registration)
        return render_template('regn_addresses.html', regnDetails=registration, regDataAsJSON=json_reg_str)
    else:
        status = submit_registration(format_json(registration))
        if status == "success":
            return render_template('regn_debtor.html')
        else:
            json_reg_str = jsonpickle.encode(registration)
            return render_template('regn_submission_error.html', regnDetails=registration, regDataAsJSON=json_reg_str,
                                   error=status)


@app.route('/add_address', methods=['POST'])
def additional_address():
    logging.info("additional addresses")
    registration = jsonpickle.decode(request.form['regDataAsJSON'])
    address_type = request.form['address_type']
    name_or_number = request.form['name_or_number']
    street = request.form['street']
    town = request.form['town']
    postcode = request.form['postcode']
    address = Address(address_type, name_or_number, street, town, postcode)
    registration.addressList.append(address)
    add_address = request.form['add_address']

    if add_address == "yes":
        json_reg_str = jsonpickle.encode(registration)
        return render_template('regn_addresses.html', regnDetails=registration, regDataAsJSON=json_reg_str)
    else:
        status = submit_registration(format_json(registration))
        if status == "success":
            return render_template('regn_debtor.html')
        else:
            json_reg_str = jsonpickle.encode(registration)
            return render_template('regn_submission_error.html', regnDetails=registration, regDataAsJSON=json_reg_str,
                                   error=status)


@app.route('/resubmit', methods=['POST'])
def resubmit():
    logging.info("resubmit")
    registration = jsonpickle.decode(request.form['regDataAsJSON'])
    registration.key_number = request.form['key_no']
    registration.application_ref = request.form['reference']
    registration.date = request.form['application_date']
    registration.forenames = request.form['forename']
    registration.surname = request.form['surname']
    registration.alt_forename = request.form['alt_forename']
    registration.alt_surname = request.form['alt_surname']
    registration.date_of_birth = request.form['dob']
    registration.gender = request.form['gender']
    registration.occupation = request.form['occupation']
    registration.trading_name = request.form['trading']
    registration.withheld = request.form['withheld']

    # loop through addresses and update values with those from the html form
    for count, item in enumerate(registration.addressList):
        item.address_type = request.form['address_type_' + str(count + 1)]
        item.name_or_number = request.form['name_or_number_' + str(count + 1)]
        item.street = request.form['street_' + str(count + 1)]
        item.town = request.form['town_' + str(count + 1)]
        item.postcode = request.form['postcode_' + str(count + 1)]

    status = submit_registration(format_json(registration))
    if status == "success":
        return render_template('regn_debtor.html')
    else:
        json_reg_str = jsonpickle.encode(registration)
        return render_template('regn_submission_error.html', regnDetails=registration, regDataAsJSON=json_reg_str,
                               error=status)


def submit_registration(application) -> object:
    logging.info("submit_registration")
    url = 'http://10.0.2.2:5001/register'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=application, headers=headers)
    if response.status_code != 202:
        return 'Error ' + str(response.status_code) + ' :- ' + response.text
    else:
        return "success"


def format_json(registration):
    residence_addresses = []
    business_address = []
    investment_addresses = []
    for address in registration.addressList:

        dic = {'address_lines': [address.name_or_number + " " + address.street, address.town],
               'postcode': address.postcode}

        if address.address_type == 'residence':
            residence_addresses.append(dic)
        elif address.address_type == 'business':
            business_address.append(dic)
        else:
            investment_addresses.append(dic)

    names_dic = {'forenames': [registration.forenames], 'surname': registration.surname}
    alt_name = {'forenames': [registration.alt_forename], 'surname': registration.alt_surname}
    alt_names_dic = [alt_name]

    if registration.withheld == 'false':
        withheld = False
    else:
        withheld = True

    data = {'key_number': registration.key_number,
            'application_ref': registration.application_ref,
            'date': registration.date,
            'debtor_name': names_dic,
            'debtor_alternative_name': alt_names_dic,
            'gender': registration.gender,
            'occupation': registration.occupation,
            'trading_name': registration.trading_name,
            'residence': residence_addresses,
            'residence_withheld': withheld,
            'date_of_birth': registration.date_of_birth,
            'investment_property': investment_addresses
            }
    if len(business_address) > 0:
        data['business_address'] = business_address[0]

    return json.dumps(data)


class BankruptcyRegnDetails(object):
    def __init__(self, key_no, reference, application_date, forename, surname, alt_forename, alt_surname, dob,
                 gender, occupation, trading, withheld="", address_list=[]):
        self.key_number = key_no
        self.application_ref = reference
        self.date = application_date
        self.forenames = forename
        self.surname = surname
        self.alt_forename = alt_forename
        self.alt_surname = alt_surname
        self.date_of_birth = dob
        self.gender = gender
        self.occupation = occupation
        self.trading_name = trading
        self.withheld = withheld
        self.addressList = address_list


class Address(object):
    def __init__(self, address_type, name_or_number, street, town, postcode):
        self.address_type = address_type
        self.name_or_number = name_or_number
        self.street = street
        self.town = town
        self.postcode = postcode
