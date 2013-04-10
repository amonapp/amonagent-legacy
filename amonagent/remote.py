try:
	import json
except ImportError:
	import simplejson as json
import requests 
from amonagent.exceptions import ConnectionException
from amonagent.settings import settings
from amonagent.log import log

class Remote(object):

	def __init__(self):
		self.server_key = settings.SERVER_KEY
		self.port = None
		self.host = None

	def connection_host(self):
		local_hosts = ['127.0.0.1', 'localhost']
		hostaddr =  settings.REMOTE['host']

		if hostaddr in local_hosts:
			hostaddr =  "http://{0}".format(hostaddr)

		# Add http if its a numeric ip address
		if not hostaddr.startswith('http'):
			hostaddr =  "http://{0}".format(hostaddr)
		
		# Cleanup any slashes at the end of the url
		hostaddr.rstrip('/')

		return hostaddr

	def connection_port(self):
		return settings.REMOTE['port']

	def connection_url(self):
		return "{0}:{1}".format(self.connection_host(), self.connection_port())

	headers = {"Content-type": "application/json"}

	errors = {'connection': 'Could not establish connection to the Amon API.\
			Please ensure that the web application is running'}

	def to_json(self, data):
		return json.dumps(data)

	def _post(self, url, data, headers=None):

		headers = headers if headers else self.headers

		r = requests.post(url, data, headers=headers)

		if r.status_code != 200:
			raise ConnectionException(self.errors['connection'])
		else:
			return True

	def save_system_stats(self, data):
		url = "{0}/api/system/{1}".format(self.connection_url(), self.server_key)
		data = self.to_json(data)

		return self._post(url, data)

	def save_process_stats(self, data):
		url = "{0}/api/processes/{1}".format(self.connection_url(), self.server_key)
		log.info(url)
		data = self.to_json(data)

		return self._post(url, data)

	def save_distribution_info(self, data):
		url = "{0}/api/distro/{1}".format(self.connection_url(), self.server_key)
		data = self.to_json(data)

		return self._post(url, data)


remote = Remote()

