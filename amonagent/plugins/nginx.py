import requests
import re
from amonagent.utils.helpers import slugify
from amonagent.settings import settings
from amonagent.log import log

class AmonNginxPlugin(object):


	def __init__(self):
		configuration = settings.PLUGINS.get('nginx', None)
		url = configuration.get('url', None)
		
		if url is None:
			log.error('Nginx: Empty status URL in /etc/amonagent.conf:plugins:nginx')
		else:
			self.url = configuration.get('url', None)
		

	def build_report(self):
		# Report format 
		# {
		# "plugin": "nginx",
		# "graphs": [
		# 	{
		# 		"name": "Connections",
		# 		"data": {
		# 			"connections": 1, 
		# 			"reading": 0,
		# 			"writing": 0,
		# 			"waiting": 0
		# 	}},
		# 	{	
		# 		"name": "Requests per second",
		# 		"data":  {
		# 			"requests_per_second": 2
		# 	}}
		# ]
		# }
		report = {"plugin": "nginx", "graphs": []}
		temp_report = {} # Used for internal storage
		graphs = ['Requests per second', 'Connections']

		result = requests.get(self.url)
		whitelist = ['accepts','handled','requests']

		if result.text:
			status = result.text.splitlines()
			for line in status:
				stats_line = re.match('\s*(\d+)\s+(\d+)\s+(\d+)\s*$', line)
				if stats_line:
					for i, key in enumerate(whitelist): # Enumerate start is supported only in Python 2.6+
						temp_report[key] = int(stats_line.group(i+1))
						
				else:
					for (key,val) in re.findall('(\w+):\s*(\d+)', line):
						filtered_key = slugify(key)
						temp_report[filtered_key] = int(val)
		
		# Calculate requests per second
		if len(temp_report) > 0:
			total_requests = temp_report.get('requests', 0)
			handled = temp_report.get('handled', 0)
			
			if total_requests > 0 and handled > 0:
				requests_per_second = total_requests/handled
				if requests_per_second > 0:
					for key in whitelist:
						del temp_report[key]
					
					temp_report['requests_per_second'] = requests_per_second
			
		report['graphs'].append({"name": "Connections", 
			"data": {	
				"connections": temp_report['connections'],
				"reading": temp_report['reading'],
				"writing": temp_report['writing'],
				"waiting": temp_report['waiting']
			}
		})

		report['graphs'].append({"name": "Requests per second",
			"data": {
				"requests_per_second": temp_report['requests_per_second']
			}
		})	
	l
		return report


plugin = AmonNginxPlugin()