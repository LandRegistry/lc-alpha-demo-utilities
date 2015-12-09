from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, Image
#from PIL import Image


def build_paragraph(text, y_co_ord):
    for rows in text:
        c.drawString(81 * mm, y_co_ord * mm, rows)
        y_co_ord -= 5
    return

c = canvas.Canvas('K17.pdf', pagesize=A4)
c.setLineWidth(0.0125 * cm)


c.rect(0.6 * cm, 0.6 * cm, 19.6 * cm, 23.3 * cm)  # Main box
c.rect(0.6 * cm, 24.8 * cm, 17.5 * cm, 0.4 * cm)  # Search particulars title
c.rect(0.6 * cm, 23.9 * cm, 17.5 * cm, 0.9 * cm)  # Search particulars details

c.rect(0.6 * cm, 26.7 * cm, 4.2 * cm, 1.1 * cm)  # Left of three
c.rect(8.3 * cm, 26.7 * cm, 4.5 * cm, 1.1 * cm)  # Center of three
c.rect(16 * cm, 26.7 * cm, 4.1 * cm, 1.1 * cm)  # Right of three

c.setFont('Times-Bold', 17)
c.drawString(6.4 * cm, 28.5 * cm, "LAND CHARGES ACT, 1972.")

c.setFont('Times-Roman', 10)
c.drawString(6.8 * cm, 28 * cm, "CERTIFICATE OF THE RESULT OF SEARCH")

c.setFont('Times-Bold', 23)
c.drawString(18.6 * cm, 28.2 * cm, "K17")

c.setFont('Times-Roman', 8)
c.drawString(0.6 * cm, 26.1 * cm, "It is hereby certified that an official search in respect of the undermentioned "
             "particulars has been made in the index to the registers which are kept pursuant to the")
c.drawString(0.6 * cm, 25.7 * cm, "Land Charges Act 1972. The result of the search is that there are")
c.rect(8.1 * cm, 25.52 * cm, 3.8 * cm, 0.45 * cm)
c.setFont('Times-Bold', 8)
c.drawString(8.2 * cm, 25.67 * cm, "NO SUBSISTING ENTRIES.")
c.setFont('Times-Roman', 8)
c.drawString(17.8 * cm, 28.6 * cm, "Form")
c.drawString(1.5 * cm, 27.5 * cm, "CERTIFICATE No.")
c.drawString(9.3 * cm, 27.5 * cm, "CERTIFICATE DATE")
c.drawString(16.6 * cm, 27.5 * cm, "PROTECTION ENDS ON")
c.drawString(7.3 * cm, 24.9 * cm, "PARTICULARS SEARCHED")
c.drawString(0.9 * cm, 24.4 * cm, "COUNTY OR")
c.drawString(1 * cm, 24 * cm, "COUNTIES")
c.line(2.8 * cm, 23.9 * cm, 2.8 * cm, 24.8 * cm)  # Line after the counties text
c.line(0.6 * cm, 23 * cm, 20.2 * cm, 23 * cm)  # Line under Name(s)
c.drawString(6.9 * cm, 23.3 * cm, "NAME(S)")

c.line(14.9 * cm, 5.9 * cm, 14.9 * cm, 23.9 * cm)  # start of period column
c.drawString(16 * cm, 23.3 * cm, "PERIOD")
c.line(18.1 * cm, 5.9 * cm, 18.1 * cm, 23.9 * cm)  # Line between period and fees
c.drawString(18.9 * cm, 23.4 * cm, "Fees")
c.drawString(19.1 * cm, 23.1 * cm, "£")

c.line(0.6 * cm, 5.9 * cm, 20.2 * cm, 5.9 * cm)  # line above applicants ref and key number
c.line(0.6 * cm, 4.6 * cm, 20.2 * cm, 4.6 * cm)  # line below applicants ref and key number
c.line(9.45 * cm, 4.6 * cm, 9.45 * cm, 5.9 * cm)  # line before key number
c.line(12.1 * cm, 0.6 * cm, 12.1 * cm, 5.9 * cm)  # line after key number
c.line(18.1 * cm, 4.6 * cm, 18.1 * cm, 5.9 * cm)  # line after £
c.drawString(3.4 * cm, 5.6 * cm, "APPLICANT'S REFERENCE")
c.drawString(9.85 * cm, 5.6 * cm, "KEY NUMBER")

c.setFont('Times-Bold', 20)
c.drawString(17.7 * cm, 5 * cm, "£")

c.setFont('Times-Roman', 8)
c.drawString(12.4 * cm, 4.2 * cm, "Please address any enquries to:-")
lc_address = ["Land Registry",
              "Land Charges Department",
              "PO Box 292",
              "Plymouth",
              "PL5 9BY",
              "DX     8249 Plymouth 3",
              "TEL    0300 006 6616",
              "FAX    0300 006 6699"]
y = 3.6
for row in lc_address:
    c.drawString(12.4 * cm, y * cm, row)
    y -= 0.3

c.setFont('Times-Roman', 10)
c.drawString(12.4 * cm, 1.1 * cm, "IMPORTANT")
c.line(12.4 * cm, 1.05 * cm, 14.4 * cm, 1.05 * cm)  # underline text - haven't found code for that in reportlab!
c.setFont('Times-Bold', 9)
c.drawString(14.6 * cm, 1.1 * cm, "PLEASE")
c.drawString(12.4 * cm, 0.7 * cm, "READ THE NOTES OVERLEAF")

c.showPage()

c.setFont('Times-Bold', 14)
c.drawString(98 * mm, 273 * mm, 'NOTES')

c.setFont('Times-Roman', 12)
c.drawString(26 * mm, 255 * mm, "Effect of search")
c.drawString(71 * mm, 255 * mm, "1.")
text1 = ["This certificate has no statutory effect with regard to registered",
         "land, (see Land Charges Act 1972 s.14)."]
build_paragraph(text1, 255)

c.drawString(26 * mm, 241 * mm, "Particulars used for")
c.drawString(26 * mm, 236 * mm, "searching")
c.drawString(71 * mm, 241 * mm, "2.")
text2 = ["The applicant should ensure that the particulars of search",
         "which are printed on this certificate (e.g. names, counties) are",
         "the exact particulars of the required search, (see s.10(6) of",
         "Land Charges Act 1972)."]
build_paragraph(text2, 241)

c.drawString(26 * mm, 215 * mm, "Names")
c.drawString(71 * mm, 215 * mm, "3.")
text3 = ["Searching against names is conducted in accordance with the",
         "arrangements described in the \"Practice Guide 63\" (see 7 below).",
         "In printing names overleaf the forename(s) of an individual",
         "precede the surname. The surname is contained within",
         "asterisks(*) to assist identification. In printing the names of",
         "local and certain other authorities, plus signs(+) may be",
         "present but these are for official use only."]
build_paragraph(text3, 215)

c.drawString(26 * mm, 175 * mm, "\"Bankruptcy Only\"")
c.drawString(26 * mm, 170 * mm, "searches")
c.drawString(71 * mm, 175 * mm, "4.")
text4 = ["If this certificate relates to a search requested on the Form K16",
         "the words \"BANKRUPTCY ONLY\" are printed overleaf",
         "against the words \"COUNTY OR COUNTIES\". Any such",
         "search is limited to the entries described on Form K16."]
build_paragraph(text4, 175)

c.drawString(26 * mm, 150 * mm, "Protection period")
c.drawString(71 * mm, 150 * mm, "5.")
text5 = ["The date printed in the box overleaf entitled \"CERTIFICATE",
         "DATE\" is the date of the certificate for the purposes of s.11 of",
         "the Land Charges Act 1972. The date printed in the box",
         "entitled \"PROTECTION ENDS ON\" is the latest date for the",
         "expiry of the period of protection which is conferred by that",
         "section of the Act. This latter date is supplied for the",
         "convenience of the applicant."]
build_paragraph(text5, 150)

c.drawString(26 * mm, 109 * mm, "Fees")
c.drawString(71 * mm, 109 * mm, "6.")
text6 = ["The fee amounts shown in this certificate are provided for",
         "information only."]
build_paragraph(text6, 109)

c.drawString(26 * mm, 94 * mm, "Practice Guide 63")
c.drawString(71 * mm, 94 * mm, "7.")
text7 = ["Further information on procedures for making applications",
         "to the Land Charges Department, see the booklet \"Practice Guide 63\"",
         "obtainable on request from the address shown overleaf,",
         "or from the Land Registry website www.landregistry.gov.uk"]
build_paragraph(text7, 94)

c.drawString(26 * mm, 69 * mm, "Enquiries")
c.drawString(71 * mm, 69 * mm, "8.")
text8 = ["Any enquiries regarding this certificate should quote the'",
         "\"CERTIFICATE NUMBER\" and the \"CERTIFICATE DATE\"",
         "and should be sent to the address shown overleaf."]
build_paragraph(text8, 69)

c.showPage()
# w, h = A4
# image = Image.open('data_gen/gen/Amend_1.jpeg')
# c.drawImage(ImageReader(image), 0, 0, w, h)
# c.showPage()

c.save()

