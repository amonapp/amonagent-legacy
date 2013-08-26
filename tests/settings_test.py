from amonagent.settings import settings
from nose.tools import eq_
import sys

class TestSettings(object):

	def test_settings_dict(self):

		if settings.REMOTE['port'] != None:
			assert settings.REMOTE['port']
		
		assert settings.REMOTE['host']
		eq_(settings.SYSTEM_CHECK_PERIOD, 5) 
		
		assert settings.SYSTEM_CHECKS
		

		system_checks = ['cpu', 'memory', 'disk', 'network', 'loadavg']

		eq_(settings.SYSTEM_CHECKS, system_checks)

		assert settings.SERVER_KEY
		assert settings.LOGFILE
