from amonagent.modules.processes import processes_data_collector
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
from amonagent.modules.distro import get_distro
from amonagent.plugin import discover_plugins

class Runner(object):


	def info(self):
		system_info_dict = {
			'processor': get_cpu_info(),
			'ip_address': get_ip_address(),
			'distro': get_distro(),
			'uptime': get_uptime()
		}

		return system_info_dict

	def system(self):
		system_data_dict = {
			'memory': get_memory_info(),
			'cpu': get_cpu_utilization(),
			'disk': get_disk_usage(),
			'network': get_network_traffic(),
			'loadavg': get_load_average()
		}


		return system_data_dict

	def processes(self):
		return processes_data_collector.collect()
		

	def plugins(self):
		plugins_list = discover_plugins()

		plugin_result_dict = {}
		for plugin in plugins_list:
			plugin.collect()
			plugin_result_dict[plugin.name] = plugin.result

		return plugin_result_dict

runner = Runner()



