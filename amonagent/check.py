from amonagent.collector import system_info_collector, process_info_collector
from amonagent.plugin import discover_plugins
import requests

OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def test_checks():
	# Distro information 

	distro = system_info_collector.get_distro()
	if len(distro) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Distro collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_cpu_info()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "CPU Info collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = system_info_collector.get_ip()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "IP address collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_uptime()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Uptime collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_memory_info()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Memory collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_disk_usage()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Disk usage collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_network_traffic()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Network traffic collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = system_info_collector.get_load_average()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Load collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	info = system_info_collector.get_cpu_utilization()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "CPU collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)

	info = process_info_collector.process_list()
	if len(info) > 0:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Process collector: {color}{message}{end}".format(color=color, message=message, end=ENDC)


	amon_api_request = requests.post('https://amon.cx/api/test')

	if amon_api_request.status_code == 200:
		message = 'OK'
		color = OKGREEN
	else:
		message = 'Fail'
		color = FAIL

	print "Amon API: {color}{message}{end}".format(color=color, message=message, end=ENDC)


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