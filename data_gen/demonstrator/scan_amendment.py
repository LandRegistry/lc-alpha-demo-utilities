#!/usr/bin/env python

import requests
import json
from datetime import datetime


response = requests.post("http://localhost:5014/document", data="{}", headers={'Content-Type': 'application/json'})
print("Create document: " + str(response.status_code))
data = json.loads(response.text)
document_id = data['id']

document_data = {
    'id': document_id,
    'metadata': {},
    'image_paths': []
}

i = 0
for image in ['Amend.jpeg', 'AmendCont.jpeg']:
    i += 1
    file = open(image, 'rb')
    resp = requests.post("http://localhost:5014/document/" + str(document_id) + "/image",
                         data=file, headers={'Content-Type': 'image/jpeg'})
    print("Upload Scan: " + str(response.status_code))


work_data = {
    "application_type": "WO(B)",
    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "document_id": document_id,
    "work_type": "amend"
}
resp = requests.post("http://localhost:5006/workitem", data=json.dumps(work_data),
                     headers={'Content-Type': 'application/json'})
print("Lodge Work Item: " + str(response.status_code))
