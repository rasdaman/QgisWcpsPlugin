from __future__ import print_function

import mimetypes
import re
from base64 import b64encode

from PyQt5.QtWidgets import QMessageBox, QPushButton
from builtins import str
from builtins import object
import sys
import os
import time, datetime
import urllib.request, urllib.parse, urllib.error
import socket

global __version__
__version__ = '2.0'

global dsep
dsep = os.sep

import tempfile

global outputDir

class WCPSUtil(object):

	_timeout = 180
	socket.setdefaulttimeout(_timeout)

	def __init__(self):
		pass

	@staticmethod
	def basic_auth(username, password):
		auth_str = f"{username}:{password}".encode("utf-8")
		auth_b64 = b64encode(auth_str).decode("utf-8")
		return f"Basic {auth_b64}"

	@staticmethod
	def parse_error_from_xml(xml_str):
		"""
		Parse the error message from OWS XML returned from petascope
		"""
		error_message = re.search(r"<ows:ExceptionText>(.*?)</ows:ExceptionText>", xml_str).group(1)
		return error_message

	@staticmethod
	def get_url_response_data(url, username=None, password=None, data=None, read_as_binary=False):
		"""
		Send a request to server and get the response data from server
		"""
		# Pair of response_data and mime_type
		empty_results = (None, None)
		from .wcps_client_dialog import WCPSClientDialog

		headers = {}
		if (username is not None and password is not None
				and str(username).strip() != '' and str(password).strip() != ''):
			headers = {'Authorization': WCPSUtil.basic_auth(username=username, password=password)}

		request = urllib.request.Request(url, headers=headers, data=data)
		try:
			with urllib.request.urlopen(request) as response:
				if read_as_binary:
					result = response.read()
				else:
					result = response.read().decode('utf-8')

				return result, response.info().get_content_type()
		except Exception as ex:
			error_message = f"Server URL '{url}' is not accessible"
			if isinstance(ex, urllib.error.HTTPError):
				xml = ex.read().decode()
				reason = WCPSUtil.parse_error_from_xml(xml)
				error_message = f"{error_message}. Reason: {reason}"
			elif isinstance(ex, urllib.error.URLError):
				if hasattr(ex, "reason") and ex.reason != "":
					error_message = f"{error_message}. Reason: {ex.reason}"
			else:
				error_message = f"{error_message}. Reason: {ex}"

			if not error_message.endswith("."):
				error_message += "."

			WCPSClientDialog.warning_msg(f"{error_message} Hint: make sure server is running and provide valid rasdaman user's credentials.")
			return empty_results

	@staticmethod
	def parse_crs_to_ogc_shorthand_format(uri):
		"""
		e.g. https://www.opengis.net/def/crs-compound?1=https://www.opengis.net/def/crs/OGC/0/AnsiDate?axis-label="time"&2=https://www.opengis.net/def/crs/EPSG/0/28992
		convert to OGC format: [OGC:AnsiDate?axis-label="time"], [EPSG:28992]
		"""
		from urllib.parse import urlparse, parse_qs
		if "crs-compound" in uri:
			query = urlparse(uri).query
			params = parse_qs(query)
			parts = []
			for key in params.keys():
				crs_url = params[key][0]
				parts.append(WCPSUtil.__format_crs(crs_url))
			return ", ".join(parts)
		else:
			return WCPSUtil.__format_crs(uri)

	@staticmethod
	def __format_crs(crs_url: str) -> str:
		segments = crs_url.strip("/").split("/")
		if len(segments) >= 2:
			authority = segments[-3].upper()
			code = segments[-1]
			return f"[{authority}:{code}]"
		return "[INVALID]"

	def ProcessCoverage(self, input_params, username, password):
		global outputDir
		query = input_params['query']
		serv_url = input_params['serv_url']
		data = urllib.parse.urlencode({"query": query}).encode('utf-8')

		binary_data, mime_code = WCPSUtil.get_url_response_data(serv_url, username, password, data, True)
		if binary_data is None:
			return_arr = {}
		else:
			now = time.strftime('_%Y-%m-%dT%H:%M:%S')
			# e.g. .png
			file_extension = mimetypes.guess_extension(mime_code)
			if file_extension is None:
				file_extension = ".unknown"

			# e.g. /tmp/qgis_wcps_client_xxx/wcps_DATETIME.png
			outfile = tempfile.mkdtemp(prefix="qgis_wcps_client_") + dsep + "wcps" + now + file_extension

			with open(outfile, 'w+b') as f:
				f.write(binary_data)
				f.flush()

			return_arr = { "output_file_path": outfile,
						   "mimetype": mime_code
						 }

		return return_arr

	@staticmethod
	def is_json(string):
		import json
		try:
			json.loads(string)
			return True
		except json.JSONDecodeError:
			return False
