import requests
import sys
import datetime
import re
import os
import json

settings = {
    "form": None,
    "work": "bank_regn"
}

for arg in sys.argv[1:]:
    args = arg.split("=")
    arg1 = re.sub("(..)(.*)", '\g<1>(\g<2>)', args[1])
    settings[args[0]] = arg1


override = None
if len(sys.argv) > 1:
    override = sys.argv[1]


response = requests.post("http://localhost:5014/document",
                         headers={'Content-Type': 'application/json'},
                         data="{}")
if response.status_code != 201:
    print(str(response.status_code) + " from /document")
    exit(1)
document = str(response.json()["id"])

directory = os.path.dirname(__file__)
images = ["mock_pab.jpeg", "mock_evidence.jpeg"]
for image in images:
    image_data = open(os.path.join(directory, image), 'rb').read()
    response = requests.post("http://localhost:5014/document/" + document + "/image",
                             headers={'Content-Type': 'image/jpeg'},
                             data=image_data
                             )
    if response.status_code != 201:
        print(str(response.status_code) + " from /document/" + document)
        exit(1)


if settings['form'] is None:
    response = requests.get("http://localhost:5014/document/" + document + "/image/1/formtype")
    if response.status_code != 200:
        print(str(response.status_code) + " from /document/" + document + "/image/1/formtype")
        exit(1)
    formtype = response.json()["type"]
else:
    formtype = settings['form']

# create WL item POST manual
wl_data = {
    "application_type": formtype,
    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "document_id": document,
    "work_type": settings["work"]
}
print(wl_data)
response = requests.post("http://localhost:5006/workitem",
                         headers={'Content-Type': 'application/json'},
                         data=json.dumps(wl_data))
if response.status_code != 200:
    print(str(response.status_code) + " from /workitem")
    exit(1)