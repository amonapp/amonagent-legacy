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
		report = {}
		result = requests.get(self.url)
		whitelist = ['accepts','handled','requests']

		if result.text:
			status = result.text.splitlines()
			for line in status:
				stats_line = re.match('\s*(\d+)\s+(\d+)\s+(\d+)\s*$', line)
				if stats_line:
					for i, key in enumerate(whitelist): # Enumerate start is supported only in Python 2.6+
						report[key] = int(stats_line.group(i+1))
						
				else:
					for (key,val) in re.findall('(\w+):\s*(\d+)', line):
						filtered_key = slugify(key)
						report[filtered_key] = int(val)
		
		# Calculate requests per second
		if len(report) > 0:
			total_requests = report.get('requests', 0)
			handled = report.get('handled', 0)
			
			if total_requests > 0 and handled > 0:
				requests_per_second = total_requests/handled
				if requests_per_second > 0:
					for key in whitelist:
						del report[key]
					
					report['requests_per_second'] = requests_per_second
					
		return report


plugin = AmonNginxPlugin()