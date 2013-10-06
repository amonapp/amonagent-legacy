import requests
from amonagent.utils.helpers import slugify

class AmonApachePlugin(object):


	# TODO
	# Configuration file
	def __init__(self):
		pass


	def build_report(self):
		report = {}
		result = requests.get("http://www.apache.org/server-status?auto")

		ignore_list = ['Scoreboard']
		white_list = ['reqpersec','busyworkers','idleworkers','bytespersec']
		
		status = result.text.splitlines()
		for line in status:
			key, value = line.split(':')

			if key not in ignore_list:
				key = slugify(key)
				if key in white_list:
					report[key] = float(value)
		
		return report