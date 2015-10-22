import requests
import sys
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, Image

if len(sys.argv) < 2:
    print('No number specified')
    exit(1)

number = sys.argv[1]
response = requests.get('http://localhost:5004/registration/' + number)
reg = json.loads(response.text)

doc_id = reg['document_id']
response = requests.get('http://localhost:5014/document/' + doc_id)
doc = json.loads(response.text)


c = canvas.Canvas('oc.pdf', pagesize=A4)
width, height = A4

for image in doc['images']:
    image_url = 'http://localhost:5014' + image
    image = ImageReader(image_url)
    c.drawImage(image, 0, 0, width, height)
    c.showPage()

c.save()


