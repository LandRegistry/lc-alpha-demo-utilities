from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader, Image
#from PIL import Image
from reportlab.platypus import Paragraph, Frame, BaseDocTemplate, PageTemplate
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import (black
)
from reportlab.lib.styles import getSampleStyleSheet

c = canvas.Canvas('K18.pdf', pagesize=A4)


def get_style_sheet():
    stylesheet1 = ParagraphStyle('default')

    stylesheet = (ParagraphStyle(name='DocInfo',
                                 parent=stylesheet1,
                                 fontName='Courier',
                                 fontSize=10,
                                 spaceAfter=0,
                                 spaceBefore=0
                                 )

                  )
    return stylesheet


def build_result(text):
    # output the actual result
    c.setFont('Courier', 10)
    page_no = 1
    running_fee = 0

    c.drawString(1.8 * cm, 26.95 * cm, text['certificate_no'])
    c.drawString(5.4 * cm, 27 * cm, "PAGE " + str(page_no))
    c.drawString(9.4 * cm, 26.95 * cm, text['certificate_date'])
    c.drawString(16.9 * cm, 26.95 * cm, text['protection_period'])
    c.drawString(3.4 * cm, 24.3 * cm, text['counties'])
    c.drawString(20 * cm, 24.3 * cm, str(page_no))
    c.drawString(2.2 * cm, 5 * cm, text['reference'])

    addr_y = 4
    for lines in text['address']:
        c.drawString(2.7 * cm, addr_y * cm, lines)
        addr_y -= 0.4

    res_y = 22.4
    for entries in text['result']:
        c.drawString(1.1 * cm, res_y * cm, entries['name_searched'])
        c.drawString(15.6 * cm, res_y * cm, entries['period'])
        c.drawString(18.8 * cm, res_y * cm, "{0:.2f}".format(entries['fee']))
        running_fee += entries['fee']
        res_y -= 0.8
        for results in entries['result']:
            if res_y < 20:
                page_no += 1
                c.drawString(4.2 * cm, 6.5 * cm, "CONTINUED ON PAGE " + str(page_no))
                c.drawString(12.4 * cm, 5 * cm, "FEES CARRIED FORWARD")
                c.drawString(10.1 * cm, 5 * cm, text['key_number'])
                c.drawString(18.8 * cm, 5 * cm, "{0:.2f}".format(running_fee))
                c.setFont('Courier-Bold', 10)
                c.line(18.3 * cm, 3 * cm, 18.3 * cm, 3.8 * cm)  # first OMR mark
                c.line(19.1 * cm, 3 * cm, 19.1 * cm, 3.8 * cm)  # second OMR mark
                c.setFont('Courier', 12)
                build_template()
                c.setFont('Courier', 10)
                c.drawString(1.8 * cm, 26.95 * cm, text['certificate_no'])
                c.drawString(5.4 * cm, 27 * cm, "PAGE " + str(page_no))
                c.drawString(9.4 * cm, 26.95 * cm, text['certificate_date'])
                c.drawString(16.9 * cm, 26.95 * cm, text['protection_period'])
                c.drawString(3.4 * cm, 24.3 * cm, text['counties'])
                c.drawString(20 * cm, 24.3 * cm, str(page_no))
                c.drawString(2.2 * cm, 5 * cm, text['reference'])

                addr_y = 4
                for lines in text['address']:
                    c.drawString(2.7 * cm, addr_y * cm, lines)
                    addr_y -= 0.4

                c.drawString(1.1 * cm, 22.4 * cm, "CONTINUED FROM PAGE " + str(page_no - 1))
                c.drawString(12.3 * cm, 22.4 * cm, "FEES BROUGHT FORWARD")
                c.drawString(18.8 * cm, 22.4 * cm, "{0:.2f}".format(running_fee))
                res_y = 21.6

            c.drawString(2.1 * cm, (res_y + 0.1) * cm, results['code'])
            p = Paragraph(results['particulars'], get_style_sheet())
            w, h = p.wrap(10 * cm, 100 * cm)
            z = (h/3)/10
            if z > 0.4:
                res_y -= (z - 0.4)
            p.drawOn(c, 3.2 * cm, res_y * cm)
            res_y -= 0.4
        res_y -= 1

    c.drawString(10.1 * cm, 5 * cm, text['key_number'])
    c.drawString(12.9 * cm, 5 * cm, text['fee_description'])
    c.drawString(18.8 * cm, 5 * cm, "{0:.2f}".format(text['total_fee']))
    c.setFont('Courier-Bold', 12)
    c.line(17.8 * cm, 3 * cm, 17.8 * cm, 3.8 * cm)  # first OMR mark for final page
    c.line(18.6 * cm, 3 * cm, 18.6 * cm, 3.8 * cm)  # second OMR mark for final page
    c.line(19.1 * cm, 3 * cm, 19.1 * cm, 3.8 * cm)  # third OMR mark for final page
    c.setFont('Courier', 10)
    build_template()
    return 'done'


def build_template():
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
    c.drawString(18.6 * cm, 28.2 * cm, "K18")

    c.setFont('Times-Roman', 8)
    c.drawString(0.6 * cm, 26.1 * cm, "It is hereby certified that an official search in respect of the undermentioned "
                 "particulars has been made in the index to the registers which are kept pursuant to the")
    c.drawString(0.6 * cm, 25.7 * cm, "Land Charges Act 1972. The result of the search is shown below.")
    c.drawString(17.8 * cm, 28.6 * cm, "Form")
    c.drawString(1.5 * cm, 27.5 * cm, "CERTIFICATE No.")
    c.drawString(9.3 * cm, 27.5 * cm, "CERTIFICATE DATE")
    c.drawString(16.6 * cm, 27.5 * cm, "PROTECTION ENDS ON")
    c.drawString(7.3 * cm, 24.9 * cm, "PARTICULARS SEARCHED")
    c.drawString(0.9 * cm, 24.4 * cm, "COUNTY OR")
    c.drawString(1 * cm, 24 * cm, "COUNTIES")
    c.line(2.8 * cm, 23.9 * cm, 2.8 * cm, 24.8 * cm)  # Line after the counties text
    c.drawString(0.8 * cm, 23.2 * cm, "NAME(S)")
    c.drawString(2.1 * cm, 23.5 * cm, ":")
    c.drawString(2.1 * cm, 23.2 * cm, ":")
    c.drawString(2.1 * cm, 22.9 * cm, ": Particulars of Charge")

    c.line(14.9 * cm, 5.9 * cm, 14.9 * cm, 23.9 * cm)  # start of period column
    c.drawString(16 * cm, 23.3 * cm, "PERIOD")
    c.line(18.1 * cm, 5.9 * cm, 18.1 * cm, 23.9 * cm)  # Line between period and fees
    c.drawString(18.9 * cm, 23.4 * cm, "Fees")
    c.drawString(19.1 * cm, 23 * cm, "£")

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
    c.drawString(12.4 * cm, 4.2 * cm, "Please address any enquiries to:-")
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
    c.drawString(98 * mm, 280 * mm, 'NOTES')

    c.setFont('Times-Roman', 10)
    c.drawString(21 * mm, 267 * mm, "Effect of search")
    c.drawString(70 * mm, 267 * mm, "1.")
    text1 = ["This certificate has no statutory effect with regard to registered land, (see",
             "Land Charges Act 1972 s.14)."]
    build_paragraph(text1, 267)

    c.drawString(21 * mm, 256 * mm, "Particulars used for")
    c.drawString(21 * mm, 251 * mm, "searching")
    c.drawString(70 * mm, 256 * mm, "2.")
    text2 = ["The applicant should ensure that the particulars of search which are printed",
             "on this certificate (e.g. names, counties) are the exact particulars of the",
             "required search, (see s.10(6) of Land Charges Act 1972)."]
    build_paragraph(text2, 256)

    c.drawString(21 * mm, 240 * mm, "Names")
    c.drawString(70 * mm, 240 * mm, "3.")
    text3 = ["Searching against names is conducted in accordance with the arrangements",
             "described in the \"Practice Guide 63\" (see 8 below). In printing names overleaf",
             "the forename(s) of an individual precede the surname. The surname is",
             "contained within asterisks(*) to assist identification. Where a search reveals",
             "an entry the chargor's name is printed exactly as it is recorded in the index. In",
             "printing the names of local and certain other authorities, plus signs (+) may",
             "be present but these are for official use only."]
    build_paragraph(text3, 240)

    c.drawString(21 * mm, 207 * mm, "Charge particulars")
    c.drawString(70 * mm, 207 * mm, "4.")
    c.drawString(80 * mm, 207 * mm, "The information taken from the index is identified overleaf by code numbers,")
    c.drawString(80 * mm, 203 * mm, "as follows:-")
    c.drawString(86 * mm, 197 * mm, "(1)  Type of entry. Official reference number. Date of registration.")
    c.drawString(86 * mm, 192 * mm, "(2)  Short description of the land.")
    c.drawString(86 * mm, 187 * mm, "(3)  Parish, place or district.")
    c.drawString(86 * mm, 182 * mm, "(4)  County.")
    c.drawString(86 * mm, 177 * mm, "(5)  Additional information regarding the entry (e.g. \"Priority")
    c.drawString(92 * mm, 172 * mm, "Notice only\" or \"Pursuant to Priority Notice No. ...\").")
    c.drawString(86 * mm, 167 * mm, "(6)  The title, trade or profession of the chargor.")
    c.drawString(86 * mm, 162 * mm, "(7)  Chargor's address.")

    c.drawString(21 * mm, 155 * mm, "\"Bankruptcy Only\"")
    c.drawString(21 * mm, 151 * mm, "searches")
    c.drawString(70 * mm, 155 * mm, "5.")
    text5 = ["If this certificate relates to a search requested on the Form K16 the words",
             "\"BANKRUPTCY ONLY\" are printed overleaf against the words \"COUNTY",
             "OR COUNTIES\". Any such search is limited to the entries described on",
             "Form K16. Other entries in the register of pending actions or the register of",
             "writs and orders may be revealed. Bankruptcy entries can be distinguished",
             "from these by the suffix (B)."]
    build_paragraph(text5, 155)

    c.drawString(21 * mm, 126 * mm, "Protection period")
    c.drawString(70 * mm, 126 * mm, "6.")
    text6 = ["The date printed in the box overleaf entitled \"CERTIFICATE DATE\" is the",
             "date of the certificate for the purposes of s.11 of the Land Charges Act 1972.",
             "The date printed in the box entitled \"PROTECTION ENDS ON\" is the latest",
             "date for the expiry of the period of protection which is conferred by that",
             "section of the Act. This latter date is supplied for the convenience of the",
             "applicant."]
    build_paragraph(text6, 126)

    c.drawString(21 * mm, 96 * mm, "Fees")
    c.drawString(70 * mm, 96 * mm, "7.")
    c.drawString(80 * mm, 96 * mm, "The fee amounts shown in this certificate are provided for information only.")

    c.drawString(21 * mm, 87 * mm, "Practice Guide 63")
    c.drawString(70 * mm, 87 * mm, "8.")
    text8 = ["For further information on procedures for making applications to the Land",
             "Charges Department, see the Land Charges \"Practice Guide 63\"",
             "obtainable on request from the address shown overleaf, or from",
             "the Land Registry website www.landregistry.gov.uk"]
    build_paragraph(text8, 87)

    c.drawString(21 * mm, 67 * mm, "Enquiries")
    c.drawString(70 * mm, 67 * mm, "9.")
    text9 = ["Any enquiries regarding this certificate should quote the \"CERTIFICATE",
             "NUMBER\" and the \"CERTIFICATE DATE\" and should be sent to the",
             "address shown overleaf."]
    build_paragraph(text9, 67)

    c.showPage()
    # w, h = A4
    # image = Image.open('data_gen/gen/Amend_1.jpeg')
    # c.drawImage(ImageReader(image), 0, 0, w, h)
    # c.showPage()

    c.save()

    return


def build_paragraph(text, y_co_ord):
    for rows in text:
        c.drawString(80 * mm, y_co_ord * mm, rows)
        y_co_ord -= 4
    return

