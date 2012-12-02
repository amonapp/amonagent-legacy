import shelve

from amonagent.plugins.nginx import plugin
from amonagent.settings import settings

class TestNginxPlugin(object):

	def test_build_report(self):
		result = plugin.build_report()

		assert plugin.url

		assert 'handled' in result
		assert 'requests' in result
		assert 'reading' in result
		assert 'waiting' in result
		assert 'connections' in result

		# Check the cache values
		db = shelve.open(settings.CACHE)

		assert db.get('nginx:last_check')
		assert db.get('nginx:last_request_value')

