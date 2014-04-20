from amonagent.runner import runner

class TestRunner(object):

	def test_info_run(self):
		info_test = runner.info()

		assert isinstance(info_test, dict)
		assert 'processor' in info_test
		assert 'ip_address' in info_test
		assert 'distro' in info_test
		assert 'uptime' in info_test


	def test_system_run(self):
		system_test = runner.system()

		assert isinstance(system_test, dict)
		assert 'network' in system_test
		assert 'memory' in system_test
		assert 'cpu' in system_test
		assert 'disk' in system_test
		assert 'loadavg' in system_test


	def test_process_run(self):
		processes = runner.processes()
		assert isinstance(processes, dict)
		for process in processes:
			process_dict = processes[process]
			assert 'memory_mb' in process_dict
			assert 'cpu' in process_dict


