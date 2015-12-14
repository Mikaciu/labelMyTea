#!/usr/bin/env python3
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import qrcode


def display_rect(c):
    dims = [6.0 * cm, 7.5 * cm]
    for x in [1, 7.5, 14]:
        for y in [1, 9, 17]:
            c.rect(x * cm, y * cm, *dims, fill=0)

            # centered title
            c.drawCentredString((x + (dims[0] / cm) / 2) * cm, y * cm + dims[1] - 0.5 * cm, "Titre")

            # centered origin

            # type      duration        temperature

            # ingredients

            # qr
            img = qrcode.make('http://www.qwant.fr')
            image = ImageReader(img._img);
            c.drawImage(image, ((x + (dims[0] / cm) / 2) - 1.25) * cm, (y + 0.25) * cm, width=2.5 * cm, height=2.5 * cm)


c = canvas.Canvas('myfile.pdf', pagesize=A4)
display_rect(c)

# width, height = A4
# print(width, height)

textobject = c.beginText()
textobject.setTextOrigin(cm, 2.5 * cm)
c.drawText(textobject)

c.showPage()
c.save()
