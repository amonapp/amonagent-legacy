from amonagent.modules.processes import processes_data_collector

class TestProcessCheck(object):

	def test_processes_data(self):
		result = processes_data_collector.collect()

		for key, value in result.items():
			assert 'memory_mb' in value
			assert 'cpu' in value
			assert 'kb_write' in value
			assert 'kb_read' in value