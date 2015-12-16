from flask import request, Response, render_template
import logging
from application import app
import jsonpickle
import json
import requests
import datetime
from elasticsearch import Elasticsearch
from application.K18_v2 import build_result
from application.K17_v2 import build_k17_result
from application.K22_v2 import build_k22_result


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/testsearch', methods=['GET'])
def search():
    return render_template('search_tests.html')


@app.route('/testresult', methods=['POST'])
def search_tests():
    elastic = Elasticsearch()
    params = {
        'min_score': 0.4,
        'query': {
            'match': {
                'text': request.form['search']
            }
        }
    }
    result = elastic.search(index='tests', doc_type='step', body=params, size=100)
    return render_template('test_results.html', data=result)


@app.route('/migration_dashboard', methods=['GET'])
def migration_dashboard():
    logging.info("migration")

    return render_template('migration.html')


@app.route('/migrate', methods=['POST'])
def migrate():
    logging.info("migration")

    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if is_date_valid(start_date) and is_date_valid(end_date):

        if request.form['submit'] == "Migrate":

            url = app.config['DB2_MIGRATOR_URL'] + '/begin?' + 'start_date=' + start_date + '&' + 'end_date=' + end_date
            response = requests.post(url)

            if response.status_code == 200:
                response_message = "Migration successfully completed for date range " + start_date + ' to ' + end_date
            elif response.status_code == 202:
                response_message = "Migration completed with errors for dates range " + start_date + ' to ' + end_date
                migrate_error = response.json()
                return render_template('migration.html', migrate_error=migrate_error, response_message=response_message)
            elif response.status_code == 404:
                response_message = "No data found for date range " + start_date + ' to ' + end_date
            else:
                error = "HTTP Error: " + str(response.status_code) + " Migration failed"
                return render_template('migration.html', error=error)

            return render_template('migration.html', response_message=response_message)

        elif request.form["submit"] == "Preview":
            # functionality not coded for alpha
            url = app.config[
                      'DB2_LEGACY_URL'] + '/land_charge?' + 'start_date=' + start_date + '&' + 'end_date=' + end_date
            response = requests.get(url)
            if response.status_code == 404:
                final_result = ""
                response_message = "No data found for date range " + start_date + ' to ' + end_date
            else:
                final_result = response.json()
                response_message = ""
            return render_template('migration.html', start_date=start_date, end_date=end_date,
                                   results=final_result, response_message=response_message)
        elif request.form["submit"] == "Halt":
            # functionality not coded for alpha
            print("halt migration")
        else:
            # functionality not coded for alpha
            print("check migration progress")
    else:

        return render_template('migration.html', start_date=start_date, end_date=end_date,
                               error="Incorrect date format, should be YYYY-MM-DD")


@app.route('/lrbu_dashboard', methods=['GET'])
def lrbu_dashboard():
    logging.info("lrbu")

    return render_template('lrbu.html')


@app.route('/lrbu_retrieve', methods=['GET'])
def lrbu_retrieve():
    logging.info("lrbu retrieve")
    # need to call legacy-db but mock response for now until this is discussed with Mina
    data = {"results": [{"debtor_name": "Harry Smith",
                         "bankrupt": "Harry Smith",
                         "title_number": "DN100",
                         "address": "131 New Road, Plymouth, PL1 1AA"},
                        {"debtor_name": "Harry Smith",
                         "bankrupt": "Harry John Smith",
                         "title_number": "DN200",
                         "address": "12 Old Road, Saltash, PL22 2AA"}
                        ]
            }
    print(data['results'][0])

    return render_template('lrbu.html', results=data)


@app.route('/start_registration', methods=['GET'])
def start_registration():
    logging.info("registration")

    return render_template('regn_debtor.html')


@app.route('/debtor', methods=['POST'])
def debtor_details():
    logging.info("address capture")
    key_no = request.form['key_no']
    reference = request.form['reference']
    application_type = request.form['application_type']
    application_date = request.form['application_date']
    forename = request.form['forename']
    surname = request.form['surname']
    alt_forename = request.form['alt_forename']
    alt_surname = request.form['alt_surname']
    dob = request.form['dob']
    gender = request.form['gender']
    occupation = request.form['occupation']
    trading = request.form['trading']

    registration = BankruptcyRegnDetails(key_no, reference, application_type, application_date, forename, surname,
                                         alt_forename, alt_surname, dob, gender, occupation, trading)

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
        county = request.form['county']
        postcode = request.form['postcode']
        address = Address(address_type, name_or_number, street, town, county, postcode)
        registration.address_list.append(address)

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
    county = request.form['county']
    postcode = request.form['postcode']
    address = Address(address_type, name_or_number, street, town, county, postcode)
    registration.address_list.append(address)
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
    registration.type = request.form['application_type']
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
    for count, item in enumerate(registration.address_list):
        item.address_type = request.form['address_type_' + str(count + 1)]
        item.name_or_number = request.form['name_or_number_' + str(count + 1)]
        item.street = request.form['street_' + str(count + 1)]
        item.town = request.form['town_' + str(count + 1)]
        item.county = request.form['county_' + str(count + 1)]
        item.postcode = request.form['postcode_' + str(count + 1)]

    status = submit_registration(format_json(registration))
    if status == "success":
        return render_template('regn_debtor.html')
    else:
        json_reg_str = jsonpickle.encode(registration)
        return render_template('regn_submission_error.html', regnDetails=registration, regDataAsJSON=json_reg_str,
                               error=status)


@app.route('/start_search', methods=['GET'])
def start_search():
    logging.info("search")

    return render_template('search_debtor.html')


@app.route('/search', methods=['POST'])
def search_details():
    logging.info("capture search")
    forename_input = request.form['forename'] if 'forename' in request.form else ""
    surname_input = request.form['surname'] if 'surname' in request.form else ""
    complex_input = request.form['complexname'] if 'complexname' in request.form else ""
    database_input = request.form['database'] if 'database' in request.form else "reg"
    db2_reg_no_input = request.form['db2_reg_no'] if 'db2_reg_no' in request.form else ""

    #  Check Inputs
    forename, surname, complexname, db2_reg_no, error = check_inputs(forename_input, surname_input, complex_input,
                                                                     db2_reg_no_input)
    if error is True:
        return render_template('search_debtor.html', forename_error=forename, forename=forename_input,
                               surname_error=surname, surname=surname_input,
                               complex_error=complexname, complexname=complex_input,
                               db2_reg_no_error=db2_reg_no, database=database_input)

    # submit search
    get_url = ""
    post_url = ""
    if database_input == 'reg':
        if db2_reg_no_input != "":
            get_url = app.config['B2B_SEARCH_REG_URL'] + '/migrated_registration/' + db2_reg_no_input
        else:
            post_url = app.config['B2B_SEARCH_REG_URL'] + '/search'
    else:
        post_url = app.config['B2B_SEARCH_WORK_URL'] + '/search_by_name'
        db2_reg_no_input = ''

    if complex_input == "":
        data = {
            'forenames': forename_input,
            'surname': surname_input
        }
    else:
        data = {
            'forename': ' ',
            'surname': complex_input
        }

    headers = {'Content-Type': 'application/json'}

    if post_url != "":
        response = requests.post(post_url, data=json.dumps(data), headers=headers)
    else:
        response = requests.get(get_url)

    name_result = ""
    reg_no_result = ""

    if response.status_code != 404:
        if db2_reg_no_input != "":
            reg_no_result = response.json()
        else:
            name_result = response.json()

    return render_template('search_debtor.html', name_result=name_result, reg_no_result=reg_no_result,
                           forename=forename_input, surname=surname_input, complexname=complex_input,
                           db2_reg_no=db2_reg_no_input, database=database_input)


@app.route('/test_print', methods=['GET'])
def test_print():
    # ----build the K18 result----
    text = {
        "certificate_no": "G0442342",
        "certificate_date": "07 DEC 2015",
        "protection_period": "30 DEC 2015",
        "counties": "DEVON",
        "result": [
            make_result("WILLIAM JOHN  * JONES *", "1963-1988", 1.00,
                        [{"code": "NO SUBSISTING ENTRY", "particulars": ""}]),
            make_result("MAGGIE  * JONES *",
                        "1957-1988", 1.00,
                        [{"code": "(1)", "particulars": "P.A.(B)  NO.  31134  DATED 13 MAY 2012"},
                         {"code": "(5)", "particulars": "CAMBRIDGE COUNTY COURT NO 99 OF 2012"},
                         {"code": "(6)",
                          "particulars": "(N/A) AKA MARGARET KILN AKA MARGARET MASTERS RETIRED AND VERY HAPPY ABOUT IT"},
                         {"code": "(7)", "particulars": "4 LODGE COURT PLYMOUTH PL7 7HH DEVON"}]
                        )
            ],
        "reference": "MY REF",
        "address": ["MR R BARKS",
                    "123 NEW STREET",
                    "PLYMOUTH",
                    "DEVON",
                    "PL1 1AA"],
        "key_number": "2244095",
        "fee_description": "AMOUNT DEBITED",
        "total_fee": 2.00,
        "mail_type": 'DX'
    }

    build_result(text)

    # ----Build the K17 result----
    text_k17 = {
        "certificate_no": "G0423342",
        "certificate_date": "07 DEC 2015",
        "protection_period": "30 DEC 2015",
        "counties": "DEVON",
        "result": [
            make_result("RICHARD MARKS  * JOHNS *", "2015-2015", 1.00),
            make_result("THOMAS GERRY  * MARKS *", "2015-2015", 1.00),
            make_result("MARY LIZZY WENDY  * MARKS *", "1975-2015", 1.00),
            make_result("DAVID FREDDY  * MARKS *", "1975-1978", 1.00),
            make_result("SAINT TONY'S UNIVERSITY COLLEGE LAMPETER", "1988-1989", 1.00),
            make_result("THE PRINCIPAL TUTORS AND PROFESSORS OF SAINT TONY'S COLLEGE LAMPETER", "1966-1975", 1.00)
        ],
        "reference": "MY REF",
        "address": ["MR R BARKS",
                    "123 NEW STREET",
                    "PLYMOUTH",
                    "DEVON",
                    "PL1 1AA"],
        "key_number": "-------",
        "fee_description": "AMOUNT PREPAID",
        "total_fee": 6.00,
        "mail_type": 'RM'
    }

    build_k17_result(text_k17)

    # ----Build the K22 result----
    text_k22 = {
        "application_type": "NEW REGISTRATION",
        "official_ref": "PA/5555/15",
        "registration_date": "09 SEP 2015",
        "result": [
            make_result("JEFF  * JONES *",
                        None, None,
                        [{"code": "(1)", "particulars": "P.A.(B)  NO.  5555  DATED 09 SEP 2015"},
                         {"code": "(4)", "particulars": "BANKRUPTCY"},
                         {"code": "(5)",
                          "particulars": "PLYMOUTH COUNTY COURT NOT DEVON COUNTY COURT NO 7777 OF 2015"}]
                        )
        ],
        "reference": "My reference is",
        "address": ["MR R BARKS",
                    "123 NEW STREET, REALLY LONG PLACE",
                    "PLYMOUTH",
                    "DEVON",
                    "PL1 1AA"],
        "key_number": "2244095",
        "fee_description": "AMOUNT DEBITED",
        "total_fee": 1.00,
        "mail_type": 'RM'
    }

    build_k22_result(text_k22)

    return Response(status=200, mimetype='application/json')


def make_result(name_searched, period=None, fee=None, result=None):
    my_dict = {
        "name_searched": name_searched,
        "period": period,
        "fee": fee,
        "result": result
    }
    return my_dict


def submit_registration(application) -> object:
    logging.info("submit_registration")
    url = app.config['B2B_REGISTER_URL'] + '/register'
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
    for address in registration.address_list:

        dic = {'address_lines': [address.name_or_number + " " + address.street, address.town],
               'county': address.county, 'postcode': address.postcode}

        if address.address_type == 'residence':
            residence_addresses.append(dic)
        elif address.address_type == 'business':
            business_address.append(dic)
        else:
            investment_addresses.append(dic)

    names_dic = {'forenames': [registration.forenames], 'surname': registration.surname}
    alt_name = {'forenames': [registration.alt_forename], 'surname': registration.alt_surname}
    debtor_names_array = [names_dic]
    if len(alt_name['forenames'][0]) > 0 or alt_name['surname'] != '':
        debtor_names_array.append(alt_name)

    if registration.withheld == 'false':
        withheld = False
    else:
        withheld = True

    data = {'key_number': registration.key_number,
            'application_type': registration.type,
            'application_ref': registration.application_ref,
            'application_date': registration.date,
            'debtor_names': debtor_names_array,
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
    def __init__(self, key_no, reference, application_type, application_date, forename, surname, alt_forename,
                 alt_surname, dob, gender, occupation, trading, withheld="", address_list=[]):
        self.key_number = key_no
        self.application_ref = reference
        self.type = application_type
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
        self.address_list = address_list


class Address(object):
    def __init__(self, address_type, name_or_number, street, town, county, postcode):
        self.address_type = address_type
        self.name_or_number = name_or_number
        self.street = street
        self.town = town
        self.county = county
        self.postcode = postcode


def is_date_valid(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def check_inputs(forename_input, surname_input, complex_input, db2_reg_no_input):
    if forename_input == "" and surname_input == "" and complex_input == "" and db2_reg_no_input == "":
        logging.info("incomplete")
        forename = 'Missing forename'
        surname = 'Missing surname'
        complexname = 'Missing complex name'
        db2_reg_no = 'Missing registration number'
        return forename, surname, complexname, db2_reg_no, True
    elif forename_input == "" and complex_input == "" and db2_reg_no_input == "":
        forename = 'Missing forename'
        surname = ' '
        complexname = ' '
        db2_reg_no = ' '
        return forename, surname, complexname, db2_reg_no, True
    elif surname_input == "" and complex_input == "" and db2_reg_no_input == "":
        forename = ' '
        surname = 'Missing surname '
        complexname = ' '
        db2_reg_no = ' '
        return forename, surname, complexname, db2_reg_no, True
    else:
        forename = ' '
        surname = ' '
        complexname = ' '
        db2_reg_no = ' '
        return forename, surname, complexname, db2_reg_no, False