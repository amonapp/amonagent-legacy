import requests
import re
import sys

from amonagent.plugin import AmonPlugin

class NginxPlugin(AmonPlugin):
	"""Tracks basic nginx metrics via the status module
	* number of connections
	* number of requets per second

	Requires nginx to have the status option compiled.
	See http://wiki.nginx.org/HttpStubStatusModule for more details

	$ curl http://localhost/nginx_status/
	Active connections: 8
	server accepts handled requests
	 1156958 1156958 4491319
	Reading: 0 Writing: 2 Waiting: 6

	"""
	def collect(self):
		status_url =  self.config.get('status_url')

		response = requests.get(status_url)
		whitelist = ['accepts','handled','requests']
		

		if response.text:
			status = response.text.splitlines()
			for line in status:
				stats_line = re.match('\s*(\d+)\s+(\d+)\s+(\d+)\s*$', line)
				if stats_line:
					result = {}
					for i, key in enumerate(whitelist):
						key = self.normalize(key)
						value = int(stats_line.group(i+1))
						result[key] = value
						
					if len(result) > 0:
						requests_per_second = 0
						total_requests = result.get('requests', 0)
						handled = result.get('handled', 0)
			
						if total_requests > 0 and handled > 0:
							requests_per_second = total_requests/handled

							self.gauge('requests.per.second', requests_per_second)

				else:
					for (key,val) in re.findall('(\w+):\s*(\d+)', line):
						key = self.normalize(key, prefix='connections')
						self.gauge(key, int(val))
						