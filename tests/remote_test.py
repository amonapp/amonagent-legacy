from amonagent.backends import remote
from nose.tools import eq_
from amonagent.runner import runner
import requests

class TestRemoteSave(object):

	def test_save_system(self):
		system_info = runner.system()
		try:
			r =  requests.get(remote.connection_url())
		except:
			r = False

		# Test the API only when the web app is running
		if r != False:
			remote.save_system_stats(system_info)

