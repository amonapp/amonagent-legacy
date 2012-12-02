from amonagent.plugins.apache import plugin
from amonagent.settings import settings

class TestApachePlugin(object):

	def test_build_report(self):
		result = plugin.build_report()

		assert plugin.url

		assert 'uptime' in result
		assert 'idleworkers' in result
		assert 'total-accesses' in result
		assert 'reqpersec' in result
		assert 'busyworkers' in result
		assert 'total-kbytes' in result
		assert 'bytespersec' in result
		assert 'cpuload' in result
		assert 'bytesperreq' in result
