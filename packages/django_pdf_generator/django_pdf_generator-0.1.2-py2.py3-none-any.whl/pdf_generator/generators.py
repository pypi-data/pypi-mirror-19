import subprocess
import os
from django.core.validators import URLValidator
from .settings import pdf_settings
from django.http import (
	HttpResponse,
	Http404
)
from django.core.files.base import ContentFile
from .models import PdfDoc
from .utils import get_random_filename


validate_url = URLValidator(schemes=['https', 'http'])


class PDFGenerator(object):

	def __init__(self, url, paperformat='A4', zoom=1, script=pdf_settings.DEFAULT_RASTERIZE_SCRIPT,
				 temp_dir=pdf_settings.DEFAULT_TEMP_DIR):
		validate_url(url)
		self.script = script
		self.temp_dir = temp_dir
		self.url = url
		self.filename = self.__get_random_filename()
		self.filepath = self.__get_filepath()
		self.paperformat = paperformat
		self.zoom = zoom
		self.pdf_data = None
		self.__generate()
		self.__set_pdf_data()
		self.__remove_source_file()


	def __get_random_filename(self):
		name = get_random_filename(20)
		return "%s.pdf" % name


	def __get_filepath(self):
		return os.path.join(self.temp_dir, self.filename)


	def __generate(self):
		"""
		call the following command:
			phantomjs rasterize.js URL filename [paperwidth*paperheight|paperformat] [zoom]
		"""
		command = [
			pdf_settings.PHANTOMJS_BIN_PATH,
			self.script,
			self.url,
			self.filepath,
			self.paperformat,
			str(self.zoom)
		]
		return subprocess.call(command)


	def __set_pdf_data(self):
		with open(self.filepath) as pdf:
			self.pdf_data = pdf.read()


	def get_content_file(self, filename):
		return ContentFile(self.pdf_data, name=filename)


	def get_data(self):
		return self.pdf_data

	def get_http_response(self, filename):
		response = HttpResponse(self.pdf_data, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % filename
		return response


	def __remove_source_file(self):
		return subprocess.call(['rm', self.filepath])


	def save(self, filename, title='', description=''):
		file = self.get_content_file(filename)
		document = PdfDoc(
			title=title,
			description=description,
			document=file)
		document.save()
		return document


