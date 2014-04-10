from amonagent.settings import settings
from nose.tools import eq_
import sys

class TestSettings(object):

	def test_settings_dict(self):
		
		assert settings.HOST
		assert settings.SYSTEM_CHECK_PERIOD
		assert settings.LOGGING_MAX_BYTES
		assert settings.PIDFILE
		assert settings.SERVER_KEY
		assert settings.LOGFILE
