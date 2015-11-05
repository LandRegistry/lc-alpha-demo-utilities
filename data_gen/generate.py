from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import os
import json
import subprocess
import requests
import random
import calendar
import string


NUM_KEYHOLDERS = 10
NUM_PABS = 25
NUM_INS_PABS = 10
NUM_PABS_REGISTERED = 10
NUM_WOBS = 25
NUM_WOBS_REGISTERED = 10
NUM_INS_WOBS = 10
NUM_CANCELLATIONS = 6
NUM_AMENDMENTS = 6
NUM_SEARCHES = 6

work_items = ""
registrations = ""
documents = ""
keyholders_string = ""


def generate_full_search(data):
    base = Image.open('images/blank_full_search.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    for y in range(0, len(data['search'])):
        search = data['search'][y]
        draw.text((480, 641 + (y * 88)), search['forename'], font=font, fill=(0, 0, 0, 255))
        draw.text((480, 683 + (y * 88)), search['surname'], font=font, fill=(0, 0, 0, 255))
        draw.text((1207, 665 + (y * 88)), search['from'], font=font, fill=(0, 0, 0, 255))
        draw.text((1325, 665 + (y * 88)), search['to'], font=font, fill=(0, 0, 0, 255))

    draw.text((126, 1558), str(data['key_number']), font=font, fill=(0, 0, 0, 255))
    draw.text((146, 1915), str(data['reference']), font=font, fill=(0, 0, 0, 255))
    draw.text((389, 1559), str(data['cust_name']), font=font, fill=(0, 0, 0, 255))
    draw.text((389, 1621), str(data['cust_addr']), font=font, fill=(0, 0, 0, 255))
    draw.text((556, 1891), str(data['date']), font=font, fill=(0, 0, 0, 255))

    draw.text((456, 1171), str(data['county']), font=font, fill=(0, 0, 0, 255))
    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/WOB_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/WOB_{}.jpeg".format(file_no)
    out.save(filename)
    return filename


def generate_banks_search(data):
    base = Image.open('images/blank_banks_search.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    for y in range(0, len(data['search'])):
        search = data['search'][y]
        draw.text((434, 900 + (y * 88)), search['forename'], font=font, fill=(0, 0, 0, 255))
        draw.text((434, 944 + (y * 88)), search['surname'], font=font, fill=(0, 0, 0, 255))

    draw.text((126, 1517), str(data['key_number']), font=font, fill=(0, 0, 0, 255))
    draw.text((151, 1908), str(data['reference']), font=font, fill=(0, 0, 0, 255))
    draw.text((389, 1527), str(data['cust_name']), font=font, fill=(0, 0, 0, 255))
    draw.text((389, 1581), str(data['cust_addr']), font=font, fill=(0, 0, 0, 255))
    draw.text((570, 1884), str(data['date']), font=font, fill=(0, 0, 0, 255))
    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/WOB_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/WOB_{}.jpeg".format(file_no)
    out.save(filename)
    return filename


def generate_search_image(data):
    print( data)
    if data["application_type"] == "Full Search":
        return generate_full_search(data)
    else:
        return generate_banks_search(data)


def address_string(address):
    return "\n".join(address["address_lines"]) + "\n" + address["county"] + "\n" + \
           address["postcode"]


def generate_amendment_image(data):
    base = Image.open('images/blank_amend_with_cont.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    draw.text((368, 148), data['action'], font=font, fill=(0, 0, 0, 255))
    draw.text((608, 288), data['reg_date'], font=font, fill=(0, 0, 0, 255))
    draw.text((464, 476), data['forename'], font=font, fill=(0, 0, 0, 255))
    draw.text((464, 524), data['surname'], font=font, fill=(0, 0, 0, 255))
    draw.text((778, 572), "X", font=font, fill=(0, 0, 0, 255))

    draw.text((446, 606), data["occupation"], font=font_small, fill=(0, 0, 0, 255))
    for y in range(0, len(data["aliases"])):
        draw.text((476, 636 + (y * 25)), data["aliases"][y], font=font, fill=(0, 0, 0, 255))
    draw.text((460, 754), data["trading"], font=font, fill=(0, 0, 0, 255))

    for x in range(0, 7):
        draw.text((360 + (x * 64), 1162), str(data["key_no"])[x], font=font, fill=(0, 0, 0, 255))

    addr_list = data["exist_addresses"]
    addr_list.append(data["addl_address"])
    draw.text((356, 928), address_string(addr_list[0]), font=font_small, fill=(0, 0, 0, 255))

    if len(addr_list) >= 2:
        draw.text((576, 928), address_string(addr_list[1]), font=font_small, fill=(0, 0, 0, 255))

    draw.text((744, 1342), data["wob_no"], font=font, fill=(0, 0, 0, 255))
    draw.text((426, 1394), data["pab_no"], font=font, fill=(0, 0, 0, 255))
    draw.text((446, 1424), data['reg_date'], font=font, fill=(0, 0, 0, 255))
    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/Amend_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/Amend_{}.jpeg".format(file_no)
    out.save(filename)
    filenames = [filename]

    if len(addr_list) >= 3:
        base = Image.open('images/blank_amend_with_cont_2.jpg').convert('RGBA')
        text = Image.new('RGBA', base.size, (255, 255, 255, 0))
        font = ImageFont.truetype('FreeMonoBold.ttf', 24)
        draw = ImageDraw.Draw(text)
        draw.text((168, 174), address_string(addr_list[2]), font=font, fill=(0, 0, 0, 255))
        if len(addr_list) >= 4:
            draw.text((168, 370), address_string(addr_list[3]), font=font, fill=(0, 0, 0, 255))
        if len(addr_list) >= 5:
            draw.text((168, 574), address_string(addr_list[3]), font=font, fill=(0, 0, 0, 255))
        out = Image.alpha_composite(base, text)
        file_no = 1
        while os.path.isfile("gen/AmendCont_{}.jpeg".format(file_no)):
            file_no += 1

        filename = "gen/AmendCont_{}.jpeg".format(file_no)
        out.save(filename)
        filenames.append(filename)

    return filenames


def generate_cancel_image(data):
    base = Image.open('images/blank_cancellation.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    draw.text((642, 1072), data['class'], font=font, fill=(0, 0, 0, 255))
    draw.text((784, 1181), str(data['reg_no']), font=font, fill=(0, 0, 0, 255))
    draw.text((976, 1191), data['date_of_reg'], font=font, fill=(0, 0, 0, 255))
    draw.text((540, 1318), data['forenames'], font=font, fill=(0, 0, 0, 255))
    draw.text((540, 1359), data['surname'], font=font, fill=(0, 0, 0, 255))
    draw.text((152, 1425), str(data['key_no']), font=font_small, fill=(0, 0, 0, 255))
    draw.text((142, 1462), ", ".join(data['conv_name']), font=font, fill=(0, 0, 0, 255))

    address = "\n".join(data["conv_addr"]["address_lines"]) + "\n" + \
              data["conv_addr"]["county"] + "\n" + data["conv_addr"]["postcode"]
    draw.text((370, 1450), address, font=font_small, fill=(0, 0, 0, 255))
    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/CancForm_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/CancForm_{}.jpeg".format(file_no)
    out.save(filename)
    return filename


def generate_cancel_evidence_image(data):
    base = Image.open('images/blank_cancellation_evidence.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))
    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    draw.text((533, 55), "In the County Court at " + data['court'], font=font, fill=(0, 0, 0, 255))
    draw.text((674, 137), data['ref'], font=font_small, fill=(0, 0, 0, 255))
    draw.text((674, 182), data['forenames'] + " " + data["surname"], font=font_small, fill=(0, 0, 0, 255))
    draw.text((120, 327), "Deputy District Judge " + data['judge'], font=font_small, fill=(0, 0, 0, 255))

    draw.text((285, 563), data['applicant'], font=font_small, fill=(0, 0, 0, 255))
    draw.text((90, 428), data['applicant'], font=font_small, fill=(0, 0, 0, 255))
    draw.text((90, 460), "\n".join(data['appl_address']["address_lines"]), font=font_small, fill=(0, 0, 0, 255))
    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/CancEvid_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/CancEvid_{}.jpeg".format(file_no)
    out.save(filename)
    return filename


def generate_wob_image(data):
    keyno_x = [576, 633, 690, 744, 798, 858, 915]

    base = Image.open('images/blank_WOB.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))

    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    draw.text((657, 176), data['legal_body'], font=font, fill=(0, 0, 0, 255))
    draw.text((819, 176), data['legal_body_ref'], font=font, fill=(0, 0, 0, 255))
    name = ' '.join(data['debtor_name']['forenames']) + ' ' + data['debtor_name']['surname']
    draw.text((476, 220), name, font=font, fill=(0, 0, 0, 255))
    draw.text((553, 370), ' '.join(data['debtor_name']['forenames']), font=font, fill=(0, 0, 0, 255))
    draw.text((553, 400), data['debtor_name']['surname'], font=font, fill=(0, 0, 0, 255))
    draw.text((767, 474), 'X', font=font, fill=(0, 0, 0, 255))
    draw.text((449, 555), data['occupation'], font=font, fill=(0, 0, 0, 255))
    if data['trading_name'] != "":
        draw.text((449, 555), "Trading as " + data['trading_name'], font=font, fill=(0, 0, 0, 255))

    if 'business_address' in data:
        address = ', '.join(data['business_address']['address_lines']) + ', ' + \
                  data['business_address']['county'] + ', ' + data['business_address']['postcode']
        draw.text((441, 779), address, font=font_small, fill=(0, 0, 0, 255))

    for x in range(0, 7):
        draw.text((keyno_x[x], 1057), data['key_number'][x], font=font, fill=(0, 0, 0, 255))

    draw.text((589, 1115), data['legal_body'], font=font_small, fill=(0, 0, 0, 255))
    draw.text((473, 1152), data['legal_body_ref'], font=font_small, fill=(0, 0, 0, 255))
    draw.text((681, 1372), data['date'], font=font, fill=(0, 0, 0, 255))

    out = Image.alpha_composite(base, text)
    file_no = 1
    while os.path.isfile("gen/WOB_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/WOB_{}.jpeg".format(file_no)
    out.save(filename)
    return filename
# TODO: Option to base a WOB on a created PAB


def generate_pab_image(data):
    address_y = [739, 784, 821]
    business_y = [856, 896, 931, 971]
    keyno_x = [476, 510, 552, 589, 627, 669, 708]

    base = Image.open('images/blank_PAB.jpg').convert('RGBA')
    text = Image.new('RGBA', base.size, (255, 255, 255, 0))

    font = ImageFont.truetype('FreeMonoBold.ttf', 24)
    font_small = ImageFont.truetype('FreeMonoBold.ttf', 16)
    draw = ImageDraw.Draw(text)

    draw.text((317, 471), ' '.join(data['debtor_name']['forenames']), font=font, fill=(0, 0, 0, 255))
    draw.text((831, 416), 'X', font=font, fill=(0, 0, 0, 255))
    draw.text((325, 538), data['debtor_name']['surname'], font=font, fill=(0, 0, 0, 255))
    draw.text((325, 605), data['occupation'], font=font, fill=(0, 0, 0, 255))
    draw.text((328, 1111), data['legal_body'], font=font, fill=(0, 0, 0, 255))
    draw.text((371, 1157), data['legal_body_ref'], font=font, fill=(0, 0, 0, 255))

    ay = 0
    for address in data['residence']:
        addr = ', '.join(address['address_lines']) + ', ' + address['county'] + ', ' + address['postcode']
        draw.text((346, address_y[ay]), addr, font=font_small, fill=(0, 0, 0, 255))
        ay += 1

    by = 0
    if 'business_address' in data:
        address = ', '.join(data['business_address']['address_lines']) + ', ' + \
                  data['business_address']['county'] + ', ' + data['business_address']['postcode']
        draw.text((346, business_y[by]), address, font=font_small, fill=(0, 0, 0, 255))
        by += 1

    for x in range(0, 7):
        draw.text((keyno_x[x], 1033), data['key_number'][x], font=font, fill=(0, 0, 0, 255))

    out = Image.alpha_composite(base, text)

    file_no = 1
    while os.path.isfile("gen/PAB_{}.jpeg".format(file_no)):
        file_no += 1

    filename = "gen/PAB_{}.jpeg".format(file_no)
    out.save(filename)
    return filename


# TODO: allow multiple business addresses

def execute(command):
    out = subprocess.check_output(command)
    return out.decode('utf-8')


def generate_ref():
    ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


def generate_keyholders():
    global keyholders_string
    for i in range(0, NUM_KEYHOLDERS):
        if i == 0:
            num = 1234567 # at least one should be easy to remember
        else:
            num = random.randrange(1000000, 9999999)
        data = {
            "number": num,
            "account_code": "C",
            "name": [conveyancers.pop(0)],
            "address": addresses.pop(0),
        }
        key_holders.append(data)
        keyholders_string += json.dumps(data) + ',\n'
        requests.post("http://localhost:5007/keyholder", data=json.dumps(data),
                      headers={'Content-Type': 'application/json'})


def create_document(images):

    response = requests.post("http://localhost:5014/document", data="{}", headers={'Content-Type': 'application/json'})
    data = json.loads(response.text)
    document_id = data['id']

    document_data = {
        'id': document_id,
        'metadata': {},
        'image_paths': []
    }

    i = 0
    for image in images:
        i += 1
        file = open(image, 'rb')
        resp = requests.post("http://localhost:5014/document/" + str(document_id) + "/image",
                             data=file, headers={'Content-Type': 'image/jpeg'})
        print('Upload image: {} - {}'.format(image, str(resp.status_code)))

    return document_id


def register(data):
    global registrations
    data['legal_body_ref']
    resp = requests.post("http://localhost:5004/registration", data=json.dumps(data),
                         headers={'Content-Type': 'application/json'})
    new_data = json.loads(resp.text)
    registrations += json.dumps(data) + ',\n'

    print('Create registration: ' + str(resp.status_code))
    return new_data["new_registrations"][0]


def add_to_worklist(data, work_type):
    global work_items
    work_data = {
        "application_type": data["application_type"],
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "document_id": data["document_id"],
        "work_type": work_type
    }
    resp = requests.post("http://localhost:5006/workitem", data=json.dumps(work_data),
                         headers={'Content-Type': 'application/json'})
    work_items += json.dumps(work_data) + ',\n'
    print('Create workitem: ' + str(resp.status_code))


def random_date(after=None, max_year=2015):
    if after is None:
        after = datetime(2010, 1, 1)

    year = random.randrange(after.year, max_year + 1)
    if year == after.year:
        month = random.randrange(after.month, 13)
    else:
        month = random.randrange(1, 13)

    if year == after.year and month == after.month:
        day = random.randrange(after.day + 1, 1 + calendar.monthrange(year, month)[1])
    else:
        day = random.randrange(1, 1 + calendar.monthrange(year, month)[1])

    return datetime(year, month, day)


def create_registration(reg_type, max_year=2015):
    num_res = random.randrange(1, 7) - 3
    if num_res < 1:
        num_res = 1

    residence = []
    for x in range(0, num_res):
        residence.append(addresses.pop(0))

    name_object = names.pop(0)
    alias = []
    if random.randrange(0, 2) == 0:
        alias.append(name_object[1])
    if random.randrange(0, 2) == 0:
        alias.append(name_object[2])

    county = residence[0]['county']
    date = random_date(None, max_year)
    data = {
        "key_number": str(random.choice(key_holders)["number"]), "application_type": reg_type,
        "application_ref": "RF" + str(random.randrange(100000, 999999)),
        "date": date.strftime('%Y-%m-%d'), "occupation": occupations.pop(0),
        "date_of_birth": None, "residence_withheld": False, "residence": residence,
        "investment_property": [],  # "business_address": None,
        "debtor_name": name_object[0],
        "debtor_alternative_name": alias, "trading_name": "", "document_id": 0,
        "legal_body_ref": str(random.randrange(100, 999)) + " of " + str(date.year), "legal_body": county
    }

    if random.randrange(0, 3) == 0:
        data['investment_property'] = [addresses.pop(0)]

    if random.randrange(0, 3) == 0:
        data['business_address'] = addresses.pop(0)

    if random.randrange(0, 2) == 0:
        data['trading_name'] = company_names.pop(0)
    return data


def generate_pabs():
    to_register = NUM_PABS_REGISTERED
    ins_counter = 0
    result = []
    for i in range(0, NUM_PABS):
        data = create_registration("PA(B)")

        if ins_counter > NUM_INS_PABS:
            file = generate_pab_image(data)
            data['legal_body'] += " County Court"
            doc_id = create_document([file])
            data['document_id'] = doc_id

            if to_register > 0:
                register(data)
                result.append(data)
                to_register -= 1
            else:
                add_to_worklist(data, "bank_regn")
        else:
            print(data['application_type'])
            data['legal_body'] = 'Insolvency Service'
            data['document_id'] = None
            register(data)
            result.append(data)
        ins_counter += 1
    return result


def generate_wobs():
    to_register = NUM_WOBS_REGISTERED
    ins_counter = 0
    result = []
    for i in range(0, NUM_WOBS):
        data = create_registration("WO(B)")

        if ins_counter > NUM_INS_WOBS:
            file = generate_wob_image(data)
            data['legal_body'] += " County Court"
            doc_id = create_document([file])
            data['document_id'] = doc_id

            if to_register > 0:
                register(data)
                result.append(data)
                to_register -= 1
            else:
                add_to_worklist(data, "bank_regn")
        else:
            print(data['application_type'])
            data['legal_body'] = 'Insolvency Service'
            data['document_id'] = None
            register(data)
            result.append(data)
        ins_counter += 1
    return result


def generate_cancellations():
    # Generate a PAB or WOB and capture it's registration date and number and other details
    # Create a cancellation image and an evidence image
    # Make document, worklist item
    for i in range(0, NUM_CANCELLATIONS):
        data = create_registration("WO(B)", 2013)  # TODO: also PABs
        file = generate_wob_image(data)
        doc_id = create_document([file])
        data['legal_body'] += " County Court"
        data['document_id'] = doc_id
        reg_no = register(data)

        kh = random.choice(key_holders)

        name = names.pop(0)[0]
        cancel_data = {
            "forenames": " ".join(data["debtor_name"]["forenames"]),
            "surname": data['debtor_name']['surname'],
            "reg_no": reg_no,
            "class": "wob",
            "date_of_reg": data["date"],
            "key_no": kh["number"],
            "conv_name": kh["name"],
            "conv_addr": kh["address"],
            "judge": name["forenames"][0] + " " + name['surname'],
            "ref": data["legal_body_ref"],
            "court": data["legal_body"],
            "applicant": company_names.pop(0),
            "appl_address": addresses.pop(0)
        }
        images = [None, None]
        images[0] = generate_cancel_image(cancel_data)
        images[1] = generate_cancel_evidence_image(cancel_data)
        canc_doc = create_document(images)
        add_to_worklist({
            "application_type": "WO(B)",
            "document_id": canc_doc,
        }, "cancel")


def generate_amendments():
    # address added/amended
    # name amendment/alias removal
    for i in range(0, NUM_AMENDMENTS):
        # Generate a WOB
        # and a PAB dated a few days earlier
        # Generate amendment data, linked to PAB & WOB
        data = create_registration("WO(B)", 2014)
        file = generate_wob_image(data)
        doc_id = create_document([file])
        data['legal_body'] += " County Court"
        data['document_id'] = doc_id
        wob_reg_no = register(data)

        date = datetime.strptime(data["date"], '%Y-%m-%d')
        data["date"] = (date - timedelta(days=15)).strftime('%Y-%m-%d')
        data["application_type"] = "PA(B)"
        file = generate_pab_image(data)
        doc_id = create_document([file])
        data['document_id'] = doc_id
        pab_reg_no = register(data)

        # must have existing addresses...
        alias = []
        for name in data["debtor_alternative_name"]:
            alias.append(" ".join(name["forenames"]) + " " + name["surname"])

        kh = random.choice(key_holders)
        amend_data = {
            "wob_no": str(wob_reg_no),
            "pab_no": str(pab_reg_no),
            "action": "Address added/amended",
            "exist_addresses": data["residence"],
            "addl_address": addresses.pop(0),
            "forename": " ".join(data["debtor_name"]["forenames"]),
            "surname": data["debtor_name"]["surname"],
            "aliases": alias,
            "occupation": data["occupation"],
            "trading": data["trading_name"],
            "key_no": kh["number"],
            "court": data["legal_body"],
            "reference": data["legal_body_ref"],
            "reg_date": date.strftime('%Y-%m-%d')
        }
        images = generate_amendment_image(amend_data)
        amend_doc = create_document(images)
        add_to_worklist({
            "application_type": "WO(B)",
            "document_id": amend_doc,
        }, "amend")


def generate_searches():
    for i in range(0, NUM_SEARCHES):
        cust = random.choice(key_holders)
        data = {
            "key_number": cust["number"],
            "cust_name": " ".join(cust["name"]),
            "cust_addr": address_string(cust["address"]),
            "date": random_date(datetime(2015, 1, 1)).strftime('%Y-%m-%d'),
            "reference": generate_ref,
            "search": []
        }

        if random.randrange(0, 2) == 0:
            data['application_type'] = 'Full Search'
            if random.randrange(0, 3) == 0:
                data['county'] = 'All'
                data['former_county'] = ''
            else:
                data['county'] = ''
                for k in range(0, random.randrange(1, 10)):
                    data['county'] = data['county'] + ', ' + counties.pop(0)

        else:
            data['application_type'] = 'Search'

        # TODO Have a chance to include a name or alias from records
        num = random.randrange(1, 7)
        for j in range(1, num):
            if random.randrange(0,3) == 0:
                reg = random.choice(records)
                namelist = [reg['debtor_name']] + reg['debtor_alternative_name']
                name = [random.choice(namelist)]
            else:
                name = names.pop(0)
            search = {
                "forename": " ".join(name[0]["forenames"]),
                "surname": name[0]['surname']
            }
            if data['application_type'] == 'Full Search':
                if random.randrange(0, 5) == 0:
                    start = random.randrange(1900, 1999)
                    search['from'] = str(start)
                    search['to'] = str(random.randrange(start + 1, 2016))
                else:
                    search['from'] = '1925'
                    search['to'] = '2015'
            data['search'].append(search)
        file = generate_search_image(data)
        doc_id = create_document([file])
        data['document_id'] = doc_id
        add_to_worklist(data, "search")


names = json.loads(execute(['ruby', 'generate.rb', 'names', '1000']))
addresses = json.loads(execute(['ruby', 'generate.rb', 'addresses', '1000']))
occupations = json.loads(execute(['ruby', 'generate.rb', 'occupations', '1000']))
company_names = json.loads(execute(['ruby', 'generate.rb', 'businesses', '1000']))
counties = json.loads(execute(['ruby', 'generate.rb', 'counties', '100']))
conveyancers = json.loads(execute(['ruby', 'generate.rb', 'conveyancers', str(NUM_KEYHOLDERS)]))
key_holders = []

generate_keyholders()
records = generate_pabs()
records += generate_wobs()
generate_cancellations()
generate_amendments()
generate_searches()

wfile = open('workitems.txt', 'w')
rfile = open('registrations.txt', 'w')
kfile = open('keyholders.txt', 'w')
wfile.write(work_items)
rfile.write(registrations)
kfile.write(keyholders_string)


# f = open('myfile','w')
# f.write('hi there\n') # python will convert \n to os.linesep
# f.close()work_items = ""
# registrations = ""
# documents = ""
# keyholders_string = ""