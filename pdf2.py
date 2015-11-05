from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet

c = Canvas('test.pdf', pagesize=A4)
#c.drawString(1 * cm, 28 * cm, "This is auch text")

styles = getSampleStyleSheet()
style = styles['BodyText']

p = Paragraph('This is a paragraph of text, with many, many words in it. Not that many, actually.', style)
w, h = p.wrap(5 * cm, 800)
p.drawOn(c, 4 * cm, 15 * cm)


p = Paragraph('This is a second paragraph of text, with many, many words in it. Not that many, actually.', style)
w, h = p.wrap(5 * cm, 800)
p.drawOn(c, 4 * cm, 20 * cm)

p = Paragraph('This is a third paragraph of text, with many, many words in it. Not that many, actually.', style)
w, h = p.wrap(5 * cm, 800)
p.drawOn(c, 4 * cm, 10 * cm)

c.showPage()
c.save()
