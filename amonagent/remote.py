try:
	import json
except ImportError:
	import simplejson as json
import requests 

from amonagent.settings import settings


class ConnectionException(Exception):
	" Raised when the Amon Web interface is not responding"


class Remote(object):

	def __init__(self):
		self.server_key = settings.SERVER_KEY
		self.host = settings.HOST


	headers = {"Content-type": "application/json"}
	errors = {'connection': 'Could not establish connection to the Amon API.'}

	def to_json(self, data):
		return json.dumps(data)

	def _post(self, url, data, headers=None):

		headers = headers if headers else self.headers

		
		r = requests.post(url, data, headers=headers, timeout=10, stream=False)
		if r.status_code != 200:
			raise ConnectionException(self.errors['connection'])

		return True

	def save_system_info(self, data):
		url = "{0}/api/info/{1}".format(self.host, self.server_key)
		data = self.to_json(data)

		return self._post(url, data)



	def save_system_stats(self, data):
		url = "{0}/api/system/{1}".format(self.host, self.server_key)
		data = self.to_json(data)

		return self._post(url, data)


remote = Remote()

