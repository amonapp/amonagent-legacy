from amonagent.modules.processes import processes_data_collector
from amonagent.modules.core import (
	get_uptime,
	get_memory_info,
	get_cpu_utilization,
	get_load_average,
	disk_check,
	get_network_traffic,
	get_ip_address,
	get_cpu_info,
	get_system_uuid
)
from amonagent.modules.containers import container_data_collector
from amonagent.modules.distro import get_distro
from amonagent.modules.plugins import discover_plugins

import logging
log = logging.getLogger(__name__)

class Runner(object):


	def __init__(self):
		self.plugins_list = discover_plugins()


	def info(self):
		system_info_dict = {
			'processor': get_cpu_info(),
			'ip_address': get_ip_address(),
			'distro': get_distro(),
			'uptime': get_uptime(),
			'unique_id': get_system_uuid(),
		}

		return system_info_dict

	def system(self):
		system_data_dict = {
			'memory': get_memory_info(),
			'cpu': get_cpu_utilization(),
			'disk': disk_check.check(),
			'network': get_network_traffic(),
			'loadavg': get_load_average(),
			'unique_id': get_system_uuid()
		}


		return system_data_dict

	def containers(self):
		return container_data_collector.collect()


	def processes(self):
		return processes_data_collector.collect()
		

	def plugins(self):
		plugin_result_dict = {}
		for plugin in self.plugins_list:

			# Don't stop the agent if the plugin data cannot be collected
			try:
				plugin.collect()
				plugin_result_dict[plugin.name] = plugin.result
			except:
				log.exception("Can't collect data for plugin: {0}".format(plugin.name))
				return False

		return plugin_result_dict

runner = Runner()



