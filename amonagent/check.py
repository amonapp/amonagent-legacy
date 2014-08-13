import requests

from amonagent.modules.core import (
	get_uptime,
	get_memory_info,
	get_cpu_utilization,
	get_load_average,
	get_disk_usage,
	get_network_traffic,
	get_ip_address,
	get_cpu_info
)
from amonagent.modules.processes import processes_data_collector
from amonagent.modules.distro import get_distro
from amonagent.plugin import discover_plugins
from amonagent.settings import settings


OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def test_checks():
	# Distro information 

	distro = get_distro()
	if len(distro) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Distro collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_cpu_info()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "CPU Info collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = get_ip_address()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "IP address collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_uptime()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Uptime collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_memory_info()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Memory collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_disk_usage()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Disk usage collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_network_traffic()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Network traffic collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = get_load_average()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Load collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = get_cpu_utilization()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "CPU collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = processes_data_collector.collect()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Process collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)



	url = "https://amon.cx/api/test/{0}".format(settings.SERVER_KEY)
	response = requests.post(url)

	if response.status_code == 200:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail. Please check that you have a valid server key in /etc/amon-agent.conf'
		color = FAIL

	print "Sending data to {0}".format(url)
	print "{color}{message}{end}".format(color=color, message=message, end=ENDC)


def test_plugins():
	print "Enabled plugins: "
	

	enabled_plugis =  discover_plugins()
	for plugin in enabled_plugis:
		print '------------------'
		print "  {color}{plugin}{end}".format(color=OKBLUE, plugin=plugin.name.title(), end=ENDC)
		print '------------------'
		error = True
		
		try:
			data = plugin.collect()
			error = False
		except Exception, e:
			raise e

		if error == False:
			message = 'OK'
			color = OKGREEN
		else:
			message = 'Fail'
			color = FAIL

	
		print "Check: {color}{message}{end}".format(color=color, message=message, end=ENDC)
		print plugin.result