# -*- coding: utf-8 -*-
from cStringIO import StringIO
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.rl_config import defaultPageSize
from datetime import timedelta
import os

FONT_PATH = os.path.join(settings.STATIC_ROOT, 'brucka/fonts/OpenSans-Regular.ttf')
pdfmetrics.registerFont(TTFont('OpenSans', FONT_PATH))

TABLE_STYLE = TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'OpenSans'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
])


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont('OpenSans', 9)
        page_width = defaultPageSize[0]
        self.drawRightString(page_width - 2.54*cm, 2*cm, '%d/%d' % (self._pageNumber, page_count))


def students_pdf(students):
    output = StringIO()
    doc = SimpleDocTemplate(output)
    elements = []
    data = [(u'JMBAG', u'Prezime', u'Ime', u'E-mail', u'Karta', u'Vrijeme prodaje')]
    for s in students:
        if s.ticket_or_none:
            ticket_number = s.ticket.number
            # fetch ticket creation time and strip off microseconds and timezone info (they're not needed in the output)
            ticket_creation_time = s.ticket.creation_time.replace(microsecond=0, tzinfo=None)
        else:
            ticket_creation_time = ''
            ticket_number = ''

        data.append((s.code, s.last_name, s.first_name, s.email, ticket_number, ticket_creation_time))
    table = Table(data, style=TABLE_STYLE)
    elements.append(table)
    doc.build(elements, canvasmaker=NumberedCanvas)
    return output.getvalue()
