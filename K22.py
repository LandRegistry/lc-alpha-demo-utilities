from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, Image
#from PIL import Image

c = canvas.Canvas('K22.pdf', pagesize=A4)
c.setLineWidth(0.0125 * cm)


c.rect(0.7 * cm, 0.8 * cm, 19.6 * cm, 24.6 * cm)  # Main box
c.line(0.7 * cm, 5.2 * cm, 20.3 * cm, 5.2 * cm)  # Line above cust address
c.line(0.7 * cm, 6.4 * cm, 20.3 * cm, 6.4 * cm)  # Line above key num, applicants ref
c.line(10.8 * cm, 6.4 * cm, 10.8 * cm, 0.8 * cm)  # Line between bottom boxes
c.line(0.7 * cm, 23.5 * cm, 20.3 * cm, 23.5 * cm)  # Line under 'Name of the estate owner'
c.line(3 * cm, 24.3 * cm, 3 * cm, 22.8 * cm)  # Weird crossing line
c.line(6.8 * cm, 25.4 * cm, 6.8 * cm, 23.5 * cm)  # Top separator
c.line(13.3 * cm, 6.4 * cm, 13.3 * cm, 5.2 * cm)  # Right of key number
c.line(18.4 * cm, 6.4 * cm, 18.4 * cm, 5.2 * cm)  # Right of £

c.rect(0.7 * cm, 25.6 * cm, 5.1 * cm, 1 * cm)  # Left of three
c.rect(7.4 * cm, 25.6 * cm, 6.3 * cm, 1 * cm)  # Center of three
c.rect(15.3 * cm, 25.6 * cm, 5 * cm, 1 * cm)  # Right of three

c.setFont('Times-Bold', 18)
c.drawString(6.4 * cm, 28.5 * cm, "LAND CHARGES ACT, 1972.")

c.setFont('Times-Roman', 11)
c.drawString(6.9 * cm, 28 * cm, "ACKNOWLEDGEMENT OF APPLICATION")

c.setFont('Times-Roman', 8)
c.drawString(0.7 * cm, 27.2 * cm, "The Chief Land Registrar acknowledges receipt of the undermentioned "
             "application to which effect has been given on the date and under the official")
c.drawString(0.7 * cm, 26.9 * cm, "reference number below.")
c.drawString(17.8 * cm, 28.6 * cm, "Form")
c.drawString(1.8 * cm, 26.2 * cm, "TYPE OF APPLICATION")
c.drawString(8.25 * cm, 26.2 * cm, "OFFICIAL REFERENCE NUMBER")
c.drawString(16.1 * cm, 26.2 * cm, "DATE OF REGISTRATION")
c.drawString(1 * cm, 24.4 * cm, "NAME OF THE ESTATE OWNER/CHARGOR")
c.drawString(3.5 * cm, 23.9 * cm, "Particulars of the entry")
c.drawString(10.7 * cm, 24.4 * cm, "PLEASE READ THE NOTES OVERLEAF")
c.drawString(2.8 * cm, 6.1 * cm, "APPLICANT'S REFERENCE")
c.drawString(11.2 * cm, 6.1 * cm, "KEY NUMBER")

c.setFont('Times-Bold', 8)
c.drawString(8.8 * cm, 24.4 * cm, "IMPORTANT")

c.setFont('Times-Bold', 24)
c.drawString(18.6 * cm, 28.2 * cm, "K22")

c.setFont('Times-Roman', 20)
c.drawString(17.9 * cm, 5.7 * cm, "£")
c.showPage()

c.setFont('Times-Bold', 15)
c.drawString(99 * mm, 266 * mm, 'NOTES')

c.setFont('Times-Roman', 12)
c.drawString(22 * mm, 243 * mm, "Particulars of")
c.drawString(22 * mm, 238 * mm, "the entry")
c.drawString(81 * mm, 243 * mm, "1.")
c.drawString(88 * mm, 243 * mm, "Please check the information printed overleaf and notify")
c.drawString(88 * mm, 238 * mm, "the Land Charges Department of any apparent")
c.drawString(88 * mm, 233 * mm, "inaccuracy.")

c.drawString(22 * mm, 217 * mm, "Name of the")
c.drawString(22 * mm, 212 * mm, "Estate owner/Chargor")
c.drawString(81 * mm, 217 * mm, "2.")
c.drawString(88 * mm, 217 * mm, "Asterisks (*) are used to identify the surname of an")
c.drawString(88 * mm, 212 * mm, "individual.")

c.drawString(22 * mm, 196 * mm, "Code numbers")
c.drawString(81 * mm, 196 * mm, "3.")
c.drawString(88 * mm, 196 * mm, "The following is an explanation of the code numbers used")
c.drawString(88 * mm, 191 * mm, "to identify information printed overleaf:-")

c.drawString(87 * mm, 181 * mm, "(1)")
c.drawString(87 * mm, 167 * mm, "(2)")
c.drawString(87 * mm, 156 * mm, "(3)")
c.drawString(87 * mm, 146 * mm, "(4)")
c.drawString(87 * mm, 135 * mm, "(5)")
c.drawString(95 * mm, 181 * mm, "Type of Entry. Official Reference Number.")
c.drawString(95 * mm, 176 * mm, "Date of Registration.")
c.drawString(95 * mm, 167 * mm, "Short description of the land.")
c.drawString(95 * mm, 156 * mm, "Parish, place or district.")
c.drawString(95 * mm, 146 * mm, "County.")
c.drawString(95 * mm, 135 * mm, "Additional information regarding the entry.")

c.drawString(22 * mm, 120 * mm, "Fees")
c.drawString(81 * mm, 120 * mm, "4.")
c.drawString(88 * mm, 120 * mm, "The fee amounts shown in this acknowledgement are")
c.drawString(88 * mm, 115 * mm, "provided for information only.")

c.drawString(22 * mm, 99 * mm, "Practice Guide 63")
c.drawString(81 * mm, 99 * mm, "5.")
c.drawString(88 * mm, 99 * mm, "Further information about procedures in the Land Charges")
c.drawString(88 * mm, 94 * mm, "Department are contained in \"Practice Guide 63\"")
c.drawString(88 * mm, 89 * mm, "obtainable on request from the address shown overleaf,")
c.drawString(88 * mm, 84 * mm, "or from the Land Registry website www.landregistry.gov.uk")



c.showPage()
# w, h = A4
# image = Image.open('data_gen/gen/Amend_1.jpeg')
# c.drawImage(ImageReader(image), 0, 0, w, h)
# c.showPage()

c.save()
