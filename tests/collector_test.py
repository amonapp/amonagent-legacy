from amonagent.collector import system_info_collector, process_info_collector
import sys
import re

class TestSystemCheck(object):

	def test_uptime(self):
		uptime = system_info_collector.get_uptime()

		assert isinstance(uptime, str)

	def test_system_info(self):
		system_info = system_info_collector.get_system_info()

		assert 'distro' in system_info
		assert 'uptime' in system_info
		assert 'processor' in system_info
		assert 'ip_address' in system_info
		


	def test_memory(self):
		memory_dict = system_info_collector.get_memory_info()

		assert 'free_mb' in memory_dict
		assert 'total_mb' in memory_dict
		assert 'used_mb' in memory_dict
		assert 'used_percent' in memory_dict
		assert 'swap_free_mb' in memory_dict
		assert 'swap_used_mb' in memory_dict
		assert 'swap_used_percent' in memory_dict
		assert 'swap_total_mb' in memory_dict

		for v in memory_dict.values():
			assert isinstance(v, int)


	def test_disk(self):
		disk = system_info_collector.get_disk_usage()

		for k in disk:
			_dict = disk[k]

			assert 'used' in _dict
			assert 'percent' in _dict
			assert 'free' in _dict
			assert 'volume' in _dict
			assert 'total' in _dict


	def test_cpu(self):
		cpu = system_info_collector.get_cpu_utilization()

		assert 'idle' in cpu
		assert 'user' in cpu
		assert 'system' in cpu

		for v in cpu.values():
			# Could be 1.10 - 4, 10.10 - 5, 100.00 - 6
			assert len(v) == 4 or len(v) == 5 or len(v) == 6

			value_regex = re.compile(r'\d+[\.]\d+')
			assert re.match(value_regex, v)


	def test_loadavg(self):
		loadavg = system_info_collector.get_load_average()

		assert 'minute' in loadavg
		assert 'five_minutes' in loadavg
		assert 'fifteen_minutes' in loadavg
		assert 'cores' in loadavg

		assert isinstance(loadavg['cores'], int)
		assert isinstance(loadavg['minute'], str)
		assert isinstance(loadavg['five_minutes'], str)
		assert isinstance(loadavg['fifteen_minutes'], str)
		
		value_regex = re.compile(r'\d+[\.]\d+')

		assert re.match(value_regex, loadavg['minute'])
		assert re.match(value_regex, loadavg['five_minutes'])
		assert re.match(value_regex, loadavg['fifteen_minutes'])

	def test_network(self):
		network_data = system_info_collector.get_network_traffic()
	   
		value_regex = re.compile(r'\d+[\.]\d+')        
		assert isinstance(network_data, dict)
		for key, value in network_data.iteritems():
			assert key not in ['lo', 'IFACE']
			for k in value.keys():
				assert k in ['inbound', 'outbound']

			for k, v in value.items():
				assert re.match(value_regex, v)

class TestProcessCheck(object):

	def test_process_list(self):
		for process in process_info_collector.process_list():
			assert 'memory_mb' in process
			assert 'cpu' in process

