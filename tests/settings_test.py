from amonagent.settings import settings
from nose.tools import eq_
import sys

class TestSettings(object):

	def test_settings_dict(self):
		assert settings.REMOTE['host']
		assert settings.REMOTE['port']
		
		eq_(settings.SYSTEM_CHECK_PERIOD, 2) 
		
		assert settings.SYSTEM_CHECKS
		

		system_checks = ['cpu', 'memory', 'disk', 'network', 'loadavg']

		eq_(settings.SYSTEM_CHECKS, system_checks)

		assert settings.SERVER_KEY
		assert settings.LOGFILE
		assert settings.CACHE
		assert settings.PLUGINS
