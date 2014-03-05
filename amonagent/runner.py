from amonagent.collector import system_info_collector, process_info_collector
from amonagent.plugin import discover_plugins

class Runner(object):


	def info(self):
		return system_info_collector.get_system_info()

	def system(self):

		system_info_dict = {}

		memory = system_info_collector.get_memory_info()
		cpu = system_info_collector.get_cpu_utilization()
		loadavg = system_info_collector.get_load_average()
		disk = system_info_collector.get_disk_usage()
		network = system_info_collector.get_network_traffic()
		uptime = system_info_collector.get_uptime()

		if memory != False:
			system_info_dict['memory'] = memory

		if cpu != False:
			system_info_dict['cpu'] = cpu

		if loadavg != False:
			system_info_dict['loadavg'] = loadavg

		if disk != False: 
			system_info_dict['disk'] = disk

		if network != False:
			system_info_dict['network'] = network

		if uptime != False:
			system_info_dict['uptime'] = uptime


		return system_info_dict

	def processes(self):

		process_checks = process_info_collector.process_list()

		process_info_dict = {}
		for process in process_checks:
			command = process["command"]
			command = command.replace(".", "")
			del process["command"]
			process_info_dict[command]  = process

		return process_info_dict

	def plugins(self):
		plugins_list = discover_plugins()

		plugin_result_dict = {}
		for plugin in plugins_list:
			plugin.collect()
			plugin_result_dict[plugin.name] = plugin.result

		return plugin_result_dict

runner = Runner()



