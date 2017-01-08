from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import cm

from datetime import datetime


# http://code.activestate.com/recipes/576832/
class NumberedCanvas(canvas.Canvas):

	def __init__(self, *args, **kwargs):
		canvas.Canvas.__init__(self, *args, **kwargs)
		self._saved_page_states = []

	def showPage(self):
		self._saved_page_states.append(dict(self.__dict__))
		self._startPage()

	def save(self):
		num_pages = len(self._saved_page_states)
		for state in self._saved_page_states:
			self.__dict__.update(state)
			self.draw_page_number(num_pages)
			canvas.Canvas.showPage(self)
		canvas.Canvas.save(self)

	def draw_page_number(self, page_count):
		self.setFont("Helvetica", 8)
		self.drawRightString(15*cm, 1*cm, "Página %d de %d" % (self._pageNumber, page_count))


class DocumentBuilder:

	def __init__(self, buffer):
		self._page_h = letter[0]
		self._page_w = letter[1]
		self._styles = getSampleStyleSheet()
		self._font = 'Helvetica'
		self._doc = None
		self._company = ''
		self._title = ''
		self._logo_path = ''
		self._buffer = buffer
		self._elements = []

	def _header(self, canvas, doc):
		canvas.saveState()
		canvas.setFont(self._font, 8)

		header = Paragraph(self._company+'<br/>'+self._title+'<br/>'+datetime.now().strftime("%d/%m/%Y %H:%M:%S"), self._styles['Normal'])
		w, h = header.wrap(doc.width, doc.topMargin)
		header.drawOn(canvas, self._page_w-doc.rightMargin-header.minWidth(), self._page_h-70)

		logo = Image(self._logo_path, width=100, height=51)
		logo.drawOn(canvas, 20, self._page_h-80)

		canvas.restoreState()

	def build(self):
		self._doc = SimpleDocTemplate(self._buffer, pagesize=landscape(letter))
		self._doc.topMargin = 3.5*cm
		self._doc.bottomMargin = 2*cm
		self._doc.build(self._elements, canvasmaker=NumberedCanvas, onFirstPage=self._header, onLaterPages=self._header)

	def travel_list(self, info, travels):
		self._company = "Transportes Darwin"
		self._title = "Listado de Viajes"
		self._logo_path = "static/resources/img/logo-darwin-mini.png"

		data = [('Viaje', 'Grupo', 'Bus', 'Empresa', 'Conductor', 'Itinerario', 'Fecha', 'Hora', 'Notas')]
		for travel in travels:
			row = (str(travel.pk).zfill(4), Paragraph(travel.group.__str__(), self._styles["BodyText"]))
			if travel.bus:
				row += (travel.bus.plate, Paragraph(travel.bus.company.__str__(), self._styles["BodyText"]))
			else:
				row += ("-----", "-----")
			if travel.driver:
				row += (Paragraph(travel.driver.__str__(), self._styles["BodyText"]),)
			else:
				row += ("-----",)
			row += (Paragraph(travel.itinerary.__str__(), self._styles["BodyText"]),)
			row += (travel.date.strftime("%d/%m/%Y"),)
			if travel.time:
				row += (travel.time.strftime("%H:%M"),)
			else:
				row += ("--:--",)
			row += (Paragraph(travel.notes, self._styles["BodyText"]),)

			data.append(row)

		info_table = Table(info)
		info_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))

		data_table = Table(data, colWidths=(None, 3*cm, None, None, None, 5*cm, None, 1*cm, 6*cm), repeatRows=1)
		data_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
										('FONTSIZE', (0, 0), (-1, -1), 9),
										('LINEABOVE', (0,0), (-1,0), 1, colors.black),
										('LINEBELOW', (0,0), (-1,0), 1, colors.black),
										('ALIGN', (0,0), (-1,0), 'CENTER'),
										('ALIGN', (0,1), (1,-1), 'RIGHT'),
										('ALIGN', (1,1), (4,-1), 'CENTER'),
										('ALIGN', (-2,1), (-1,-1), 'RIGHT'),
										('VALIGN', (0,0), (-1, -1), 'TOP'),
										]))

		space = Spacer(width=0, height=cm)

		self._elements.append(info_table)
		self._elements.append(space)
		self._elements.append(data_table)

		self.build()

		pdf = self._buffer.getvalue()
		self._buffer.close()
		return pdf
